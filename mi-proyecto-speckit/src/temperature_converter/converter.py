from dataclasses import dataclass
from enum import Enum

try:
    from temperature_converter.models import TemperatureUnit
except ImportError:
    try:
        from temperature_converter.models import Unit as TemperatureUnit
    except ImportError:
        class TemperatureUnit(Enum):
            CELSIUS = "C"
            FAHRENHEIT = "F"
            KELVIN = "K"

@dataclass
class TemperatureResult:
    value: float
    target_unit: TemperatureUnit

    @property
    def formatted(self) -> str:
        # Formato esperado: "32.00 F"
        val = 0.0 if abs(self.value) == 0.0 else self.value
        return f"{val:.2f} {self.target_unit.value}"

    def __str__(self) -> str:
        return str(self.value)

def convert_temperature(val: float, from_unit, to_unit) -> TemperatureResult:
    from_str = from_unit.value if hasattr(from_unit, "value") else str(from_unit)
    to_str = to_unit.value if hasattr(to_unit, "value") else str(to_unit)

    # Limpiar espacios y símbolos de grado extra
    from_u = from_str.strip().lower()
    to_u = to_str.strip().lower()

    # Mapeo completo de unidades y alias (incluyendo °c, °f, °k)
    unit_map = {
        "c": TemperatureUnit.CELSIUS, 
        "°c": TemperatureUnit.CELSIUS,
        "celsius": TemperatureUnit.CELSIUS,
        "f": TemperatureUnit.FAHRENHEIT, 
        "°f": TemperatureUnit.FAHRENHEIT,
        "fahrenheit": TemperatureUnit.FAHRENHEIT,
        "k": TemperatureUnit.KELVIN, 
        "°k": TemperatureUnit.KELVIN,
        "kelvin": TemperatureUnit.KELVIN
    }

    if from_u not in unit_map or to_u not in unit_map:
        raise ValueError("Unidad de temperatura no válida.")

    f_enum = unit_map[from_u]
    t_enum = unit_map[to_u]

    val = float(val)

    # Validaciones de Cero Absoluto
    if f_enum == TemperatureUnit.KELVIN and val < 0:
        raise ValueError(f"Temperatura no válida: {val:.2f} K es menor a 0 K (cero absoluto).")
    if f_enum == TemperatureUnit.CELSIUS and val < -273.15:
        raise ValueError("Temperatura inferior al cero absoluto.")
    if f_enum == TemperatureUnit.FAHRENHEIT and val < -459.67:
        raise ValueError("Temperatura inferior al cero absoluto.")

    if f_enum == t_enum:
        return TemperatureResult(round(val, 2), t_enum)

    # Conversión a Celsius
    if f_enum == TemperatureUnit.CELSIUS:
        celsius = val
    elif f_enum == TemperatureUnit.FAHRENHEIT:
        celsius = (val - 32) * 5 / 9
    elif f_enum == TemperatureUnit.KELVIN:
        celsius = val - 273.15

    # Conversión desde Celsius a destino
    if t_enum == TemperatureUnit.CELSIUS:
        res = celsius
    elif t_enum == TemperatureUnit.FAHRENHEIT:
        res = (celsius * 9 / 5) + 32
    elif t_enum == TemperatureUnit.KELVIN:
        res = celsius + 273.15

    return TemperatureResult(round(res, 2), t_enum)

convert = convert_temperature