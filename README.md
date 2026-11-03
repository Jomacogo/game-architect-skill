# Senior Game Architect

Skill en español para convertir un agente de IA en un colaborador de ingeniería y desarrollo de juegos con disciplina senior: analiza el proyecto, contrasta decisiones, usa MCP sin inventar capacidades, construye un vertical slice, prueba el juego real y entrega con evidencia.

> Una skill no garantiza viralidad ni sustituye criterio humano, servidores MCP, credenciales, motores o herramientas de prueba. Enseña un proceso riguroso para crear juegos con potencial de difusión y calidad verificable.

## Qué incluye

- Flujo completo: reconocimiento → investigación → diseño → vertical slice → implementación → verificación → entrega.
- Protocolo MCP: descubrimiento real, validación de esquemas, mínimos privilegios, read-back y fallbacks honestos.
- Investigación de tendencias con fuentes fechadas, sin prometer viralidad ni copiar propiedad intelectual.
- Arquitectura, determinismo, persistencia, backend, seguridad y rendimiento.
- Matrices de QA, playtest, controles, estados, reinicio, audio, red y compatibilidad.
- Auditor estático en Python, sin dependencias externas, para conflictos de Git, trabajo pendiente y posibles secretos.

## Instalación con un enlace de GitHub

Requisito: **Node.js 22.20 o superior** para usar la [CLI abierta `skills`](https://github.com/vercel-labs/skills). Revisa el contenido de una skill antes de instalarla: sus instrucciones y scripts se ejecutan con los permisos que concedas a tu agente.

```bash
npx skills add https://github.com/Jomacogo/game-architect-skill --skill senior-game-architect -g -y
```

- `-g`: disponible para todos tus proyectos; omítelo para instalarla solo en el proyecto actual.
- `-y`: acepta las confirmaciones; omítelo si prefieres elegir agente y alcance interactivamente.
- La CLI detecta agentes compatibles. Para elegir uno o varios, añade por ejemplo `-a claude-code` o `-a codex`.

Comprobar qué detecta el repositorio sin instalar:

```bash
npx skills add https://github.com/Jomacogo/game-architect-skill --list
```

## Instalación manual

### Claude Code, uso personal

```bash
git clone https://github.com/Jomacogo/game-architect-skill.git
mkdir -p ~/.claude/skills
cp -R TU_REPOSITORIO/senior-game-architect ~/.claude/skills/
```

Para un solo proyecto, copia la misma carpeta a `.claude/skills/senior-game-architect` dentro del repositorio del proyecto.

### Cualquier agente compatible con Agent Skills

Copia la carpeta completa `senior-game-architect/` —incluidos `SKILL.md`, `references/` y `scripts/`— en el directorio de skills que indique la documentación de tu agente. No copies solo `SKILL.md`: perderías los protocolos y el auditor.

Si tu agente permite importar paquetes, utiliza el archivo `senior-game-architect.skill` que acompaña esta entrega.

## Cómo utilizarla

Normalmente se activa al pedir crear, modificar, depurar u optimizar un juego. En clientes con invocación explícita, prueba:

```text
/senior-game-architect Crea un juego web 2D de sesiones de tres minutos. Investiga primero tendencias recientes, elige una sola hipótesis de compartición, construye el core loop completo y verifica controles, pausa, reinicio y rendimiento.
```

Otras peticiones útiles:

```text
Audita este proyecto como un senior. Reproduce el error, encuentra la causa raíz y no cambies arquitectura sin evidencia.
```

```text
Añade una clasificación online usando solo herramientas MCP disponibles. Valida esquemas y permisos, verifica la escritura con read-back y no finjas el backend si falta acceso.
```

## MCP

Esta skill **no instala servidores MCP ni incluye credenciales**. Configura los servidores en tu agente y concede solo los permisos necesarios. La skill obliga a descubrir herramientas reales, validar entradas, comprobar efectos y reportar autenticación, permisos o timeouts como fallos.

## Auditor local

```bash
python3 senior-game-architect/scripts/project_audit.py /ruta/al/juego --output auditoria.json
```

Devuelve código `1` si encuentra errores. Para que también fallen los avisos:

```bash
python3 senior-game-architect/scripts/project_audit.py /ruta/al/juego --strict
```

Es una comprobación complementaria: no demuestra que el juego compile, sea seguro o resulte divertido.

## Subir este contenido a GitHub

Desde la carpeta extraída del repositorio:

```bash
git init
git add .
git commit -m "feat: add senior game architect skill"
git branch -M main
git remote add origin https://github.com/Jomacogo/game-architect-skill.git
git push -u origin main
```

Crea antes un repositorio vacío en GitHub con ese nombre. Después, la instalación queda disponible mediante su enlace.

## Estructura

```text
senior-game-architect-repo/
├── senior-game-architect/
│   ├── SKILL.md
│   ├── references/
│   │   ├── engineering-and-architecture.md
│   │   ├── mcp-discipline.md
│   │   ├── trend-and-design.md
│   │   └── verification-and-delivery.md
│   └── scripts/
│       └── project_audit.py
├── tests/
│   └── test_project_audit.py
├── .github/workflows/validate.yml
├── LICENSE
└── README.md
```

## Desarrollo y validación

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile senior-game-architect/scripts/project_audit.py
```

Licencia: MIT. Revisa las licencias de cualquier asset, motor o dependencia que añadas a tus juegos.
