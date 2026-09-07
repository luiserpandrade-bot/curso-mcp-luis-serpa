"""Temperature converter module.

Converts temperature values between Celsius, Fahrenheit, and Kelvin
according to the acceptance criteria in spec_manual.md.
"""

from typing import Literal

Unit = Literal["C", "F", "K", "celsius", "fahrenheit", "kelvin"]


def _validate_kelvin(kelvin_value: float) -> None:
    """Validate that temperature in Kelvin is not below absolute zero (0 K)."""
    if kelvin_value < 0:
        raise ValueError(
            f"Temperatura no válida: {kelvin_value:.2f} K es menor a 0 K (cero absoluto)."
        )


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit, rounded to 2 decimal places."""
    kelvin = celsius + 273.15
    _validate_kelvin(kelvin)
    fahrenheit = (celsius * 9.0 / 5.0) + 32.0
    return round(fahrenheit, 2)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius, rounded to 2 decimal places."""
    celsius = (fahrenheit - 32.0) * 5.0 / 9.0
    kelvin = celsius + 273.15
    _validate_kelvin(kelvin)
    return round(celsius, 2)


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin, rounded to 2 decimal places."""
    kelvin = celsius + 273.15
    _validate_kelvin(kelvin)
    return round(kelvin, 2)


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius, rounded to 2 decimal places."""
    _validate_kelvin(kelvin)
    celsius = kelvin - 273.15
    return round(celsius, 2)


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convert Fahrenheit to Kelvin, rounded to 2 decimal places."""
    celsius = (fahrenheit - 32.0) * 5.0 / 9.0
    kelvin = celsius + 273.15
    _validate_kelvin(kelvin)
    return round(kelvin, 2)


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit, rounded to 2 decimal places."""
    _validate_kelvin(kelvin)
    celsius = kelvin - 273.15
    fahrenheit = (celsius * 9.0 / 5.0) + 32.0
    return round(fahrenheit, 2)


def _normalize_unit(unit: str) -> str:
    cleaned = unit.strip().upper()
    if cleaned in ("C", "CELSIUS"):
        return "C"
    if cleaned in ("F", "FAHRENHEIT"):
        return "F"
    if cleaned in ("K", "KELVIN"):
        return "K"
    raise ValueError(f"Unidad desconocida: '{unit}'. Use 'C', 'F' o 'K'.")


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a temperature value between Celsius ('C'), Fahrenheit ('F'), and Kelvin ('K').

    Args:
        value: The numerical temperature to convert.
        from_unit: Source scale ('C', 'F', or 'K').
        to_unit: Target scale ('C', 'F', or 'K').

    Returns:
        The converted temperature rounded to 2 decimal places.

    Raises:
        ValueError: If a temperature below 0 K is provided or unit is unsupported.
    """
    src = _normalize_unit(from_unit)
    dst = _normalize_unit(to_unit)

    if src == "K":
        _validate_kelvin(value)
    elif src == "C":
        _validate_kelvin(value + 273.15)
    elif src == "F":
        _validate_kelvin((value - 32.0) * 5.0 / 9.0 + 273.15)

    if src == dst:
        return round(float(value), 2)

    converters = {
        ("C", "F"): celsius_to_fahrenheit,
        ("F", "C"): fahrenheit_to_celsius,
        ("C", "K"): celsius_to_kelvin,
        ("K", "C"): kelvin_to_celsius,
        ("F", "K"): fahrenheit_to_kelvin,
        ("K", "F"): kelvin_to_fahrenheit,
    }

    converter = converters.get((src, dst))
    if converter is None:
        raise ValueError(f"Conversión no soportada de {from_unit} a {to_unit}")

    return converter(value)
