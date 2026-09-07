# Resultados de Pruebas - Parte 3A

## Caso de Prueba 1: Conversión Estándar Celsius a Fahrenheit
- **Comando:** `uv run convertidor-temperatura 100 c F`
- **Resultado Esperado:** 212.0
- **Resultado Obtenido:** 212.0
- **Estado:** PASA

---

## Caso de Prueba 2: Misma Unidad de Origen y Destino
- **Comando:** `uv run convertidor-temperatura 100 c c`
- **Resultado Esperado:** 100.0
- **Resultado Obtenido:** 100.0
- **Estado:** PASA

---

## Caso de Prueba 3: Manejo de Entradas Inválidas (No numéricas)
- **Comando:** `uv run convertidor-temperatura 12s c f`
- **Resultado Esperado:** Mensaje de error indicando valor no válido.
- **Resultado Obtenido:** Error: could not convert string to float: '12s'
- **Estado:** PASA