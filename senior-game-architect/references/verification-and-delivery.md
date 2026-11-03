# Verificación, playtest y entrega

## Evidencia requerida

La intensidad depende del cambio, pero toda afirmación de funcionamiento necesita ejecución real. Conservar comandos, resultados y evidencia durante el trabajo; entregar solo un resumen útil, no archivos de proceso salvo que se pidan.

## Pirámide proporcional

1. **Reglas puras**: puntuación, daño, cooldowns, progresión, economía, colisiones lógicas, seeds y migraciones.
2. **Integración**: input → simulación → estado → UI/audio; guardado/carga; red y recuperación de errores.
3. **Runtime**: build de producción o ejecutable real, sin errores inesperados ni recursos ausentes.
4. **Playtest**: una persona o automatización recorre el loop y las acciones prometidas.
5. **Rendimiento y compatibilidad**: escena máxima, dispositivos objetivo, resize, foco, pausa y reconexión cuando apliquen.

Añadir una prueba de regresión para cada defecto corregido cuando exista infraestructura razonable. No convertir pruebas frágiles de píxeles en sustituto de probar reglas.

## Matriz mínima de juego completo

| Área | Comprobación |
|---|---|
| Inicio | Carga fría, objetivo comprensible y acción de empezar. |
| Controles | Cada tecla/botón/gesto, foco, remapeo si existe y prevención de acciones del navegador. |
| Core loop | Acción, consecuencia, progreso y condición final observables. |
| Pausa | Simulación y audio según diseño; reanudación sin salto temporal. |
| Resultado | Victoria/derrota/puntuación correctas y sin doble activación. |
| Reinicio | Estado limpio, sin listeners, entidades, timers o audio duplicados. |
| UI | Todos los controles funcionan; no hay texto cortado ni elementos inaccesibles. |
| Persistencia | Guardar, recargar, versión antigua, datos corruptos y reset cuando aplique. |
| Red | Éxito, error, timeout, duplicado, offline y read-back cuando aplique. |
| Audio | Desbloqueo por gesto, mute persistente y ausencia de solapamientos infinitos. |
| Adaptación | Resoluciones/orientación objetivo, DPR, teclado/touch/gamepad según alcance. |
| Accesibilidad | Contraste, legibilidad, reducción de movimiento/flashes y alternativas razonables. |

## Verificación visual

Renderizar y observar los estados clave: inicio, primeros segundos, escena más cargada y resultado. Revisar encuadre, jerarquía, clipping, z-order, animación, feedback y consistencia. Corregir el defecto más importante atribuyéndolo a una causa concreta, volver a renderizar y comprobar la corrección. No afirmar que se vio una captura que no se abrió.

## Verificación técnica

- Ejecutar build, typecheck, lint y tests con sus comandos reales; no modificar scripts para ocultar fallos.
- Probar el artefacto servido/ejecutado como lo recibirá el usuario, no solo el servidor de desarrollo.
- Exigir cero errores de consola inesperados, 404 de assets y promesas rechazadas sin manejar.
- Medir frame time y contadores en la escena más exigente; anotar hardware, versión y configuración.
- Probar cold start y reinicio repetido para detectar estado residual.
- Revisar diff final, secretos, licencias, dependencias y archivos generados.

## Auditoría estática complementaria

Ejecutar:

```bash
python3 scripts/project_audit.py /ruta/al/proyecto --output /ruta/audit.json
```

Interpretar hallazgos antes de actuar: un `TODO` puede ser intencional y un patrón de secreto puede ser falso positivo. No borrar automáticamente código marcado. El script no prueba jugabilidad, seguridad ni rendimiento.

## Criterios de bloqueo

No entregar como terminado si existe cualquiera de estos problemas en el alcance prometido:

- build o arranque roto;
- core loop incompleto o reinicio defectuoso;
- botones/controles sin función;
- excepciones, recursos ausentes o corrupción de estado;
- mock o almacenamiento local presentado como servicio real;
- prueba reportada sin haberse ejecutado;
- secreto expuesto o asset sin derechos de uso;
- rendimiento incompatible con la plataforma objetivo.

## Entrega honesta

Incluir comandos de ejecución, controles, cambios principales y pruebas ejecutadas. Enumerar limitaciones y pasos manuales. Si algo no pudo verificarse, escribir «no verificado» con la causa y el siguiente paso; no suavizarlo como éxito. Eliminar artefactos temporales y no crear informes extensos salvo solicitud.
