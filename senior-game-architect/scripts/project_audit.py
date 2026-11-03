#!/usr/bin/env python3
"""Auditoría estática, segura y sin dependencias para proyectos de juegos.

No modifica el proyecto ni ejecuta su código. Los hallazgos son señales para
revisar, no una prueba de seguridad, jugabilidad o ausencia de defectos.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".vscode", ".agents", ".claude",
    "node_modules", "dist", "build", "out", "coverage", ".next", ".nuxt",
    ".cache", ".turbo", ".venv", "venv", "__pycache__", "Library", "Temp",
    "obj", "DerivedData", ".godot", ".import",
}

TEXT_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".css", ".gd", ".glsl", ".go", ".h",
    ".hpp", ".html", ".java", ".js", ".json", ".jsx", ".lua", ".md",
    ".php", ".py", ".rb", ".rs", ".sh", ".sql", ".svelte", ".toml",
    ".ts", ".tsx", ".txt", ".vue", ".xml", ".yaml", ".yml", ".zsh",
}

TEXT_FILENAMES = {".env", ".env.example", ".env.local", "Dockerfile", "Makefile"}
MAX_FILE_BYTES = 1_000_000

PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|XXX|PLACEHOLDER)\b", re.IGNORECASE)
NOT_IMPLEMENTED_RE = re.compile(
    r"NotImplementedError|NotImplementedException|\bunimplemented!\s*\(|\btodo!\s*\("
    r"|throw\s+new\s+(?:Error|Exception)\s*\(\s*['\"][^'\"]*not\s+implemented",
    re.IGNORECASE,
)
SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|secret|access[_-]?token|auth[_-]?token|password|private[_-]?key)\b"
    r"\s*[:=]\s*['\"]([^'\"\r\n]{8,})['\"]"
)
SAFE_SECRET_VALUES_RE = re.compile(
    r"(?i)^(?:changeme|change_me|example|sample|dummy|test|false|none|null|undefined|"
    r"your[_-]?(?:api[_-]?key|secret|token|password)|x+|\*+|\$\{[^}]+\}|"
    r"\{\{[^}]+\}\}|<[^>]+>)$"
)
HIGH_CONFIDENCE_SECRETS = (
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int
    message: str


def is_text_candidate(path: Path) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_EXTENSIONS


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in IGNORED_DIRS for part in relative.parts[:-1]):
            continue
        if is_text_candidate(path):
            yield path


def scan_file(path: Path, root: Path) -> tuple[list[Finding], bool]:
    relative = path.relative_to(root).as_posix()
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return [], True
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [], True
    except OSError:
        return [], True

    findings: list[Finding] = []
    lines = text.splitlines()
    has_conflict = any(line.startswith("<<<<<<<") for line in lines) and any(
        line.startswith(">>>>>>>") for line in lines
    )

    for number, line in enumerate(lines, start=1):
        if line.startswith(("<<<<<<<", ">>>>>>>")):
            findings.append(Finding(
                "error", "merge-conflict", relative, number,
                "Marcador de conflicto de Git; resolverlo antes de entregar.",
            ))
        elif has_conflict and line.startswith("======="):
            findings.append(Finding(
                "error", "merge-conflict", relative, number,
                "Separador de conflicto de Git; resolverlo antes de entregar.",
            ))

        if PLACEHOLDER_RE.search(line):
            findings.append(Finding(
                "warning", "unfinished-marker", relative, number,
                "Marcador de trabajo pendiente; confirmar si pertenece al alcance entregado.",
            ))

        if NOT_IMPLEMENTED_RE.search(line):
            findings.append(Finding(
                "warning", "not-implemented", relative, number,
                "Posible ruta sin implementar; comprobar si es alcanzable.",
            ))

        for code, pattern in HIGH_CONFIDENCE_SECRETS:
            if pattern.search(line):
                findings.append(Finding(
                    "error", code, relative, number,
                    "Posible secreto real; retirarlo, rotarlo y revisar el historial. Valor omitido.",
                ))

        match = SECRET_ASSIGNMENT_RE.search(line)
        if match and not SAFE_SECRET_VALUES_RE.match(match.group(1).strip()):
            findings.append(Finding(
                "warning", "hardcoded-secret", relative, number,
                "Posible credencial literal; verificar y usar un gestor de secretos. Valor omitido.",
            ))

    return findings, False


def audit(root: Path) -> dict:
    findings: list[Finding] = []
    scanned = 0
    skipped = 0
    for path in iter_files(root):
        file_findings, was_skipped = scan_file(path, root)
        findings.extend(file_findings)
        if was_skipped:
            skipped += 1
        else:
            scanned += 1

    ordered = sorted(findings, key=lambda item: (item.path, item.line, item.code))
    errors = sum(item.severity == "error" for item in ordered)
    warnings = sum(item.severity == "warning" for item in ordered)
    return {
        "schemaVersion": 1,
        "root": str(root.resolve()),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "scannedFiles": scanned,
            "skippedFiles": skipped,
            "errors": errors,
            "warnings": warnings,
        },
        "findings": [asdict(item) for item in ordered],
        "limitations": (
            "Auditoría estática por patrones. No sustituye build, tests, playtest, "
            "análisis de seguridad, revisión de licencias ni medición de rendimiento."
        ),
    }


def print_report(report: dict) -> None:
    summary = report["summary"]
    print(
        f"Archivos: {summary['scannedFiles']} analizados, "
        f"{summary['skippedFiles']} omitidos | "
        f"Errores: {summary['errors']} | Avisos: {summary['warnings']}"
    )
    for item in report["findings"]:
        print(
            f"{item['severity'].upper()} {item['path']}:{item['line']} "
            f"[{item['code']}] {item['message']}"
        )
    if not report["findings"]:
        print("Sin hallazgos por patrones. Esto no demuestra que el proyecto esté terminado.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audita marcadores pendientes, conflictos y posibles secretos sin modificar archivos."
    )
    parser.add_argument("project", type=Path, help="Ruta de la carpeta del proyecto")
    parser.add_argument("--output", type=Path, help="Guardar el informe JSON en esta ruta")
    parser.add_argument(
        "--strict", action="store_true",
        help="Devolver código 1 también cuando solo existan avisos",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.project.expanduser().resolve()
    if not root.is_dir():
        print(f"Error: no existe la carpeta del proyecto: {root}", file=sys.stderr)
        return 2

    report = audit(root)
    print_report(report)

    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Informe JSON: {output}")

    summary = report["summary"]
    if summary["errors"] or (args.strict and summary["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
