import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "senior-game-architect"
    / "scripts"
    / "project_audit.py"
)
SPEC = importlib.util.spec_from_file_location("project_audit", MODULE_PATH)
project_audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = project_audit
assert SPEC.loader is not None
SPEC.loader.exec_module(project_audit)


class ProjectAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_clean_project_has_no_findings(self):
        self.write("game.py", "def update(state):\n    return state\n")
        report = project_audit.audit(self.root)
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["summary"]["warnings"], 0)
        self.assertEqual(report["summary"]["scannedFiles"], 1)

    def test_detects_complete_merge_conflict(self):
        self.write(
            "game.ts",
            "const speed = 1;\n<<<<<<< HEAD\nconst speed = 2;\n=======\nconst speed = 3;\n>>>>>>> branch\n",
        )
        report = project_audit.audit(self.root)
        self.assertEqual(report["summary"]["errors"], 3)
        self.assertTrue(all(item["code"] == "merge-conflict" for item in report["findings"]))

    def test_detects_unfinished_paths_as_warnings(self):
        self.write("game.gd", "# TODO balancear\nfunc attack():\n    pass # NotImplementedError\n")
        report = project_audit.audit(self.root)
        codes = {item["code"] for item in report["findings"]}
        self.assertEqual(codes, {"unfinished-marker", "not-implemented"})
        self.assertEqual(report["summary"]["errors"], 0)
        self.assertEqual(report["summary"]["warnings"], 2)

    def test_secret_value_is_not_written_to_json(self):
        secret = "AKIA" + ("A" * 16)
        output = self.root / "report.json"
        self.write("config.py", f'API_KEY = "{secret}"\n')
        with contextlib.redirect_stdout(io.StringIO()):
            exit_code = project_audit.main([str(self.root), "--output", str(output)])
        self.assertEqual(exit_code, 1)
        report_text = output.read_text(encoding="utf-8")
        self.assertNotIn(secret, report_text)
        self.assertIn("aws-access-key", report_text)

    def test_ignored_directories_are_not_scanned(self):
        self.write("node_modules/pkg/index.js", "<<<<<<< HEAD\n>>>>>>> branch\n")
        self.write("src/game.js", "export const ready = true;\n")
        report = project_audit.audit(self.root)
        self.assertEqual(report["summary"]["scannedFiles"], 1)
        self.assertEqual(report["summary"]["errors"], 0)

    def test_strict_mode_turns_warnings_into_failure(self):
        self.write("game.py", "# TODO probar colisión\n")
        with contextlib.redirect_stdout(io.StringIO()):
            normal = project_audit.main([str(self.root)])
            strict = project_audit.main([str(self.root), "--strict"])
        self.assertEqual(normal, 0)
        self.assertEqual(strict, 1)

    def test_missing_project_is_a_usage_error(self):
        with contextlib.redirect_stderr(io.StringIO()):
            exit_code = project_audit.main([str(self.root / "missing")])
        self.assertEqual(exit_code, 2)


if __name__ == "__main__":
    unittest.main()
