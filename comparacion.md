# Comparación — Spec a mano vs. Spec Kit

Sesión 4 · Programación de Backend y MCP en Python para IA Generativa

Ambos bloques implementaron el mismo proyecto: un conversor de temperatura entre Celsius,
Fahrenheit y Kelvin.

## Los 3 casos de prueba, lado a lado

| Caso | Comando | Spec a mano (`clase-sdd`) | Spec Kit (`mi-proyecto-speckit`) |
|---|---|---|---|
| Caso normal | `25 C F` | `77.0` | `77.0` |
| Caso borde de la spec | `abc C F` | `Error: could not convert string to float: 'abc'` | `Error: could not convert string to float: 'abc'` |
| Caso no contemplado | `100 F K` | `310.93` | `310.93` |

Las salidas fueron idénticas en los tres casos, sin una sola diferencia en valores ni en mensajes.

## Tabla comparativa

| Aspecto | Spec a mano | Spec Kit |
|---|---|---|
| ¿Cubrió los mismos casos borde? | Sí. El error se captura y el proceso termina con código distinto de cero, aunque el mensaje es el texto interno de Python. | Sí, con el mismo comportamiento exacto. Ninguno de los dos mejoró lo que la spec dejó ambiguo. |
| ¿Qué generó Spec Kit que yo no había escrito? | Un `spec_manual.md` con 3 secciones (objetivo, 4 criterios, 3 casos borde) y un módulo plano. | 9 documentos en `specs/001-temperature-converter/`: además de `spec.md`, `plan.md` y `tasks.md`, añadió `research.md`, `data-model.md`, `quickstart.md`, un checklist de requisitos y dos contratos de interfaz (CLI y API de Python). Separó el código en tres capas (`models.py`, `converter.py`, `cli.py`) y escribió **14 pruebas automáticas** que nunca pedí. |
| ¿Qué se sintió más rápido de arrancar? | Más rápido. Tres secciones escritas a mano y una sola orden al agente bastaron para tener el programa funcionando. | Más lento de arrancar: instalación de `specify-cli` y cuatro comandos encadenados antes de ver la primera línea de código. |
| ¿Cuál me generó más confianza en el resultado? | Menos confianza: el programa funciona, pero no hay nada que lo verifique más allá de mis 3 pruebas manuales. | Más confianza, y por una razón concreta: las 14 pruebas pasan y quedan como red de seguridad. La trazabilidad escrita (qué se pidió, cómo se planificó, en qué tareas se descompuso) permite revisar decisiones que en el otro bloque quedaron implícitas. |

## Hallazgos

**El programa resultante fue el mismo; lo que cambió fue todo lo que quedó alrededor.** Para un
proyecto de este tamaño, Spec Kit no produjo mejor código: produjo el mismo código con estructura,
documentación y pruebas.

**Una inversión de lo esperado: el mensaje de ayuda del flujo automatizado es peor.** La versión a
mano imprime la sintaxis, un ejemplo de uso y la lista de unidades soportadas con su nombre completo.
La de Spec Kit imprime solo la sintaxis.

**Ninguno de los dos caminos compensa lo que la spec no dice.** Los dos cumplimientos parciales del
Bloque 3.A se repitieron intactos en el Bloque 3.B: `77.0` en lugar de `77.00`, porque escribí
"redondea a 2 decimales" y no "formatea la salida con 2 decimales"; y un mensaje de error crudo,
porque escribí "error claro" sin definir qué significa claro. Más proceso no arregló una spec vaga.

**Los dos ampliaron el alcance por su cuenta.** La spec solo pedía las conversiones Celsius↔Fahrenheit
y Celsius↔Kelvin. Ambas implementaciones resolvieron también Fahrenheit→Kelvin, generalizando a las
seis conversiones posibles.

## Cierre

> La próxima vez que tenga un proyecto de tamaño pequeño, elegiría spec a mano porque el resultado
> ejecutable fue idéntico y llegué a él en una fracción del tiempo. Reservaría Spec Kit para
> proyectos medianos o grandes, donde las 14 pruebas automáticas y la trazabilidad escrita dejan de
> ser andamiaje sobrante y pasan a ser lo que sostiene el proyecto cuando ya no me acuerdo de por qué
> tomé cada decisión.
