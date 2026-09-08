# Hallazgos de seguridad

Proyecto: `mi-proyecto-speckit` (convertidor de temperatura)
Generado siguiendo la skill `qa-security` (`.agents/skills/qa-security/SKILL.md`).
Alcance: secretos expuestos, validación de entradas y manejo de excepciones.

| Caso | Lo que se encontró | Corrección sugerida |
|---|---|---|
| 🔑 Secreto expuesto | Sin hallazgos. No hay claves, contraseñas ni tokens escritos en `src/temperature_converter/`. El proyecto no consume servicios externos todavía. | Ninguna corrección necesaria. Mantener el patrón `.env.example` + `.env` ignorado para cuando el proyecto sí necesite credenciales. |
| 🧪 Validación de entradas | **Hallazgo real.** `converter.py` acepta `nan` e `inf` como temperaturas válidas: `convert(float("nan"), "C", "F")` devuelve `nan F` sin error, y `float("inf")` devuelve `inf F`. La comparación `val < -273.15` es falsa para ambos, así que la barrera del cero absoluto no los detiene. Lo notable es que `models.py` **sí** los rechaza (`math.isfinite` en `Temperature.__post_init__`, con `InvalidInputError`), pero `converter.py` nunca instancia `Temperature`: reimplementó la validación por su cuenta y la dejó más débil. La protección existe en el proyecto y está muerta. Además, `cli.py` propaga al usuario el mensaje interno de Python (`could not convert string to float: 'abc'`) en lugar de uno redactado, lo que incumple parcialmente FR-007. | Que `convert_temperature` construya un `Temperature(val, from_unit)` y deje que `models.py` valide, en lugar de duplicar la lógica. Alternativa mínima: agregar `if not math.isfinite(val): raise ValueError(...)` antes de las comparaciones de cero absoluto. Para FR-007, capturar el `ValueError` de `float()` por separado y emitir un mensaje propio del tipo "El valor debe ser un número". |
| 🚪 Manejo de excepciones | No hay `except:` genérico ni `except: pass` en el proyecto. Pero `converter.py` (líneas 4-13) tiene una cadena anidada de `except ImportError` que, si ambos imports fallan, define en silencio **una clase `TemperatureUnit` propia**. Si eso ocurriera, las comparaciones contra `models.TemperatureUnit` fallarían sin error visible, porque serían enums distintos con los mismos valores. Es un fallback silencioso que enmascara un problema de instalación en vez de reportarlo. Aparte, `cli.py` captura un único `except ValueError` que mezcla dos causas distintas: formato de entrada inválido y violación de reglas físicas del dominio. | Eliminar el fallback de `converter.py` y dejar el import directo: si el paquete no está instalado, es preferible que falle ruidosamente. En `cli.py`, distinguir las excepciones de dominio de `models.py` (`AbsoluteZeroError`, `InvalidUnitError`, `InvalidInputError`) del `ValueError` de `float()`, para dar mensajes distintos según la causa. |

## Acciones de higiene aplicadas

Verificado con git como fuente de verdad, no leyendo `.gitignore` a ojo:

- `.env.example` — presente en la raíz del proyecto. No fue necesario crearlo.
- `.env` — no existe en el proyecto. No hay riesgo de secreto trackeado ni de que se cuele en un commit.
- `.gitignore` — ya contiene la línea `.env` (junto a `.venv/`), de modo que la regla estará activa desde el momento en que aparezca un `.env` real.
- Sin hallazgo crítico: no hay ningún `.env` bajo control de versiones, así que no hay secretos en el historial de git.

Ninguna corrección de higiene fue necesaria: el patrón ya estaba en orden.

## Nota sobre el alcance

Siguiendo el paso 8 de la skill, **no se corrigió el código de negocio**. Las dos filas con hallazgo
real quedan diagnosticadas, no reparadas: repararlas es responsabilidad de quien mantiene el código,
no del agente de seguridad. La única acción tomada por cuenta propia era la higiene de
`.env.example` / `.gitignore`, y resultó innecesaria.
