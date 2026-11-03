# Ingeniería y arquitectura de juegos

## Elegir tecnología por restricciones

Evaluar plataforma, 2D/3D, equipo, assets, red, persistencia, rendimiento, distribución y mantenimiento. Mantener el stack existente salvo que una limitación demostrada justifique migración. Para un prototipo, preferir el motor/framework que permita verificar el loop antes con menor complejidad operativa.

Comprobar documentación oficial y compatibilidad real de versiones. Fijar dependencias con lockfile; evitar paquetes abandonados, CDNs impredecibles y código propio para problemas ya resueltos por bibliotecas mantenidas.

## Arquitectura mínima suficiente

Separar conceptos, no multiplicar carpetas:

- **simulación/reglas**: estado y transiciones independientes de render cuando sea viable;
- **input**: intenciones del jugador, mapeo y foco;
- **presentación**: render, animación, audio, UI y feedback;
- **contenido/configuración**: parámetros y datos versionables;
- **infraestructura**: persistencia, red, telemetría y plataforma;
- **pruebas**: reglas puras, integración y smoke tests de runtime.

Usar máquina de estados explícita para inicio, juego, pausa, resultado y reinicio. Impedir actualizaciones de simulación durante pausa y estados residuales tras reiniciar. Mantener una única fuente de verdad para estado crítico.

## Simulación y determinismo

- Usar timestep fijo cuando física, colisiones o reproducibilidad lo requieran; separar acumulación de simulación e interpolación visual.
- Acotar delta tras cambio de pestaña o suspensión para evitar saltos y espirales de muerte.
- Centralizar RNG detrás de una semilla para pruebas, replays o desafíos compartidos.
- Evitar depender de orden de iteración no garantizado.
- Probar límites: velocidades extremas, colisiones simultáneas, empates, puntuación máxima, pausa durante transición y reinicio repetido.

## Rendimiento por presupuesto

Definir el objetivo antes de optimizar: dispositivos, resolución, FPS/frame time, memoria, entidades, draw calls, red y tamaño de descarga. Medir primero y atacar el cuello de botella observado.

Patrones habituales:

- pooling para objetos frecuentes cuando la creación/destrucción aparece en perfiles;
- instancing, batching, atlas, culling y niveles de detalle según motor;
- evitar allocaciones, consultas de red y escaneos innecesarios en hot loops;
- limitar partículas, luces, overdraw, física y audio concurrente;
- pausar trabajo invisible y liberar listeners, texturas, buffers, timers y nodos al desmontar;
- degradar calidad sin perder legibilidad ni reglas equivalentes.

No prometer 60/120 FPS por sensación: informar dispositivo, escena, duración y percentiles cuando se midan.

## Persistencia, backend y economía

- Versionar saves, validar datos al cargar, ofrecer recuperación/reset y probar migraciones.
- Declarar que almacenamiento local pertenece a ese navegador/dispositivo; no llamarlo nube.
- Usar backend real para cuentas, sincronización, clasificaciones compartidas o economía competitiva.
- Autorizar en servidor, validar inputs y no confiar puntuaciones, precios o inventario al cliente.
- Hacer operaciones de escritura idempotentes cuando un reintento pueda duplicar recompensas.
- Mantener modo offline explícito y no perder el loop por un fallo remoto.

## Modificaciones y refactors

1. Obtener línea base verde o registrar fallos preexistentes.
2. Reproducir el comportamiento y delimitar el blast radius.
3. Escribir una prueba de regresión cuando sea razonable.
4. Aplicar el cambio mínimo que corrige la causa.
5. Ejecutar pruebas cercanas y luego las globales.
6. Revisar diff, archivos generados, assets y compatibilidad.
7. No mezclar formato masivo, renombrados y cambios de comportamiento sin necesidad.

## Seguridad y calidad del código

Validar entradas externas, rutas, URLs y contenido generado por usuarios. Escapar UI, parametrizar consultas y evitar secretos en cliente. Mantener dependencias y assets con licencia compatible. Revisar controles de acceso y rate limiting en servicios públicos.

Preferir código claro, funciones con responsabilidad única y tipos en fronteras. Añadir comentarios solo para invariantes o razones no obvias. No introducir patrones complejos por anticipado ni borrar funciones existentes para simplificar artificialmente el trabajo.
