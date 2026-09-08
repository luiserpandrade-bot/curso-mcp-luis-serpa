# Resultados — Bloque 3.B (Spec Kit)

Proyecto: conversor de temperatura (`mi-proyecto-speckit`)
Generado con el flujo `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement`,
describiendo el mismo proyecto del Bloque 3.A.

## Casos de prueba

Se aplicaron exactamente los mismos tres casos del Bloque 3.A.

| Tipo de caso | Comando | Salida obtenida | Veredicto |
|---|---|---|---|
| Caso normal | `uv run convertidor-temperatura 25 C F` | `77.0` | ✅ Correcto (con observación) |
| Caso borde de la spec | `uv run convertidor-temperatura abc C F` | `Error: could not convert string to float: 'abc'` | ✅ Correcto (con observación) |
| Caso no contemplado | `uv run convertidor-temperatura 100 F K` | `310.93` | ⚠️ Funciona, fuera del alcance de la spec |

## Observaciones

**Las salidas son idénticas a las del Bloque 3.A en los tres casos.** No hay una sola diferencia en
los valores ni en los mensajes: mismo `77.0` sin el segundo decimal, mismo mensaje de error tomado
literalmente de Python, mismo `310.93` para una conversión que la spec nunca pidió. Partiendo de la
misma idea de proyecto, los dos caminos convergieron en el mismo comportamiento observable.

**El mensaje de ayuda es menos informativo que el de la versión a mano.** La versión del Bloque 3.A
imprime la sintaxis, un ejemplo de uso y la lista de unidades soportadas con su nombre completo. La
versión de Spec Kit imprime únicamente la sintaxis. Es una inversión de lo esperado: el flujo
automatizado produjo la interfaz de usuario más pobre de las dos.

**La diferencia real está en la estructura, no en el programa.** El Bloque 3.A resolvió con un módulo
plano (`clase_sdd:main`), mientras que Spec Kit organizó el código como un paquete con separación de
responsabilidades, exponiendo la línea de comandos en `temperature_converter.cli:main`. A eso se
suman los artefactos intermedios que el flujo dejó en `specs/` (`spec.md`, `plan.md`, `tasks.md`),
que no existen en el Bloque 3.A.

## Conclusión del bloque

Para un proyecto de este tamaño, Spec Kit no produjo un programa mejor: produjo el mismo programa con
más andamiaje alrededor. Los dos cumplimientos parciales detectados en el Bloque 3.A —el formato de
salida y el mensaje de error— se repitieron aquí sin corregirse, lo que sugiere que ninguno de los
dos caminos compensa lo que la spec no dice. El valor diferencial de Spec Kit no apareció en el
resultado ejecutable, sino en la trazabilidad: quedó registrado por escrito qué se pidió, cómo se
planificó y en qué tareas se descompuso.
