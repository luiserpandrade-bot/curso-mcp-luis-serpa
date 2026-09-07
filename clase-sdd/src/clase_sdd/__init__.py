"""Clase SDD - Temperature Converter Package."""

from .converter import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    celsius_to_kelvin,
    kelvin_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_to_fahrenheit,
    convert_temperature,
)

__all__ = [
    "celsius_to_fahrenheit",
    "fahrenheit_to_celsius",
    "celsius_to_kelvin",
    "kelvin_to_celsius",
    "fahrenheit_to_kelvin",
    "kelvin_to_fahrenheit",
    "convert_temperature",
]


import sys


def main() -> None:
    args = sys.argv[1:]
    if len(args) == 3:
        try:
            val = float(args[0])
            src = args[1]
            dst = args[2]
            result = convert_temperature(val, src, dst)
            print(result)
            return
        except ValueError as err:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)
    elif len(args) > 0 and args[0] in ("-h", "--help"):
        print("Uso: convertidor-temperatura <valor> <unidad_origen> <unidad_destino>")
        print("Ejemplo: convertidor-temperatura 100 C F")
        print("Unidades soportadas: C (Celsius), F (Fahrenheit), K (Kelvin)")
        return
    elif len(args) > 0:
        print("Argumentos incorrectos.", file=sys.stderr)
        print("Uso: convertidor-temperatura <valor> <unidad_origen> <unidad_destino>", file=sys.stderr)
        print("Ejemplo: convertidor-temperatura 100 C F", file=sys.stderr)
        sys.exit(1)

    print("=== Conversor de Temperatura (Clase SDD) ===")
    print("Uso: convertidor-temperatura <valor> <unidad_origen> <unidad_destino>")
    print("Ejemplo: convertidor-temperatura 100 C F\n")
    print("Ejemplos de conversión:")
    print(f"  100 °C -> {convert_temperature(100, 'C', 'F')} °F")
    print(f"  212 °F -> {convert_temperature(212, 'F', 'C')} °C")
    print(f"    0 °C -> {convert_temperature(0, 'C', 'K')} K")
    print(f"  300 K  -> {convert_temperature(300, 'K', 'C')} °C")
    print(f"  100 °F -> {convert_temperature(100, 'F', 'C')} °C (redondeado a 2 decimales)")
    try:
        convert_temperature(-5, "K", "C")
    except ValueError as err:
        print(f"  Validación K < 0: Rechazada correctamente ({err})")
