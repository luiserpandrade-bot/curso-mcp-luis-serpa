# Resultados — Bloque 3.A (Spec escrita a mano)

Proyecto: conversor de temperatura (`clase-sdd`)
Implementado a partir de `spec_manual.md`.

## Casos de prueba

| Tipo de caso | Comando | Salida obtenida | Veredicto |
|---|---|---|---|
| Caso normal | `uv run convertidor-temperatura 25 C F` | `77.0` | ✅ Correcto (con observación) |
| Caso borde de la spec | `uv run convertidor-temperatura abc C F` | `Error: could not convert string to float: 'abc'` | ✅ Correcto (con observación) |
| Caso no contemplado | `uv run convertidor-temperatura 100 F K` | `310.93` | ⚠️ Funciona, fuera del alcance de la spec |

## Observaciones

**Caso normal.** El valor es correcto (25 °C = 77 °F). Sin embargo, el criterio de aceptación
"Redondea el resultado a 2 decimales" se cumple solo a medias: el número se redondea, pero se
imprime como `77.0` y no como `77.00`. La spec decía *redondear*, no *formatear la salida*, y el
agente resolvió únicamente lo que estaba escrito.

**Caso borde.** No se produjo una excepción sin control: el error está capturado, se muestra con el
prefijo `Error:` y el proceso termina con código de salida distinto de cero. El criterio "error
claro, no una excepción sin control" se cumple en lo esencial. La reserva es que el texto mostrado
es el mensaje interno de Python (`could not convert string to float`), no un mensaje redactado para
el usuario final. La spec pedía un error "claro" sin definir qué significa claro, y esa ambigüedad
se reflejó en el resultado.

**Caso no contemplado.** La spec solo mencionaba las conversiones Celsius↔Fahrenheit y
Celsius↔Kelvin. La conversión Fahrenheit→Kelvin nunca se pidió, pero funciona y el resultado es
exacto (100 °F = 310.93 K). El agente generalizó por su cuenta a las seis conversiones posibles
entre las tres unidades, en lugar de implementar literalmente las cuatro que estaban escritas.

## Conclusión del bloque

Los tres criterios verificables se cumplieron, pero los dos cumplimientos parciales apuntan a la
misma causa: la spec fue precisa en la lógica de conversión y vaga en el formato de salida y en la
presentación de errores. Donde la spec fue explícita, el resultado fue exacto. Donde fue ambigua o
guardó silencio, el agente tomó la decisión por su cuenta, unas veces quedándose corto (formato) y
otras ampliando el alcance (conversiones no pedidas).
