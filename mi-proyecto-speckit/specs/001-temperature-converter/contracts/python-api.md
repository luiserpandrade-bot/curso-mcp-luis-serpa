# Interface Contract: Python Library API

**Module**: `temperature_converter`  
**Feature**: Temperature Unit Converter (`001-temperature-converter`)  
**Target Consumers**: Internal modules, external scripts, automated test suites  

---

## 1. Public Functions

### 1.1 `convert(value: float | int | str, from_unit: str | TemperatureUnit, to_unit: str | TemperatureUnit) -> ConversionResult`

Primary entry point for temperature conversion.

- **Parameters**:
  - `value`: Numerical temperature value to convert (can be float, int, or numeric string).
  - `from_unit`: Source scale (`"C"`, `"F"`, `"K"`, `"celsius"`, etc., or `TemperatureUnit` enum member).
  - `to_unit`: Target scale (`"C"`, `"F"`, `"K"`, `"celsius"`, etc., or `TemperatureUnit` enum member).
- **Returns**: `ConversionResult` containing:
  - `value`: `float` rounded to 2 decimal places.
  - `target_unit`: `TemperatureUnit`.
  - `source`: Original `Temperature`.
  - `formatted`: `str` with 2 decimal places (e.g., `"212.00 F"`).
- **Raises**:
  - `AbsoluteZeroError`: If input value is below absolute zero ($0\text{ K}$, $-273.15\text{ }^\circ\text{C}$, $-459.67\text{ }^\circ\text{F}$).
  - `InvalidUnitError`: If `from_unit` or `to_unit` cannot be resolved to a valid `TemperatureUnit`.
  - `InvalidInputError`: If `value` is not a valid finite number.

---

### 1.2 Convenience Shortcuts

- `celsius_to_fahrenheit(c: float) -> float`: Returns converted value rounded to 2 decimal places.
- `fahrenheit_to_celsius(f: float) -> float`: Returns converted value rounded to 2 decimal places.
- `celsius_to_kelvin(c: float) -> float`: Returns converted value rounded to 2 decimal places.
- `kelvin_to_celsius(k: float) -> float`: Returns converted value rounded to 2 decimal places.
- `fahrenheit_to_kelvin(f: float) -> float`: Returns converted value rounded to 2 decimal places.
- `kelvin_to_fahrenheit(k: float) -> float`: Returns converted value rounded to 2 decimal places.

All convenience functions enforce the `AbsoluteZeroError` validation.

---

## 2. Type Signatures

```python
from enum import Enum
from dataclasses import dataclass
from typing import Union

class TemperatureUnit(Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"

    @classmethod
    def from_str(cls, s: str) -> "TemperatureUnit": ...

@dataclass(frozen=True)
class Temperature:
    value: float
    unit: TemperatureUnit

@dataclass(frozen=True)
class ConversionResult:
    source: Temperature
    target_unit: TemperatureUnit
    value: float
    formatted: str

def convert(
    value: Union[float, int, str],
    from_unit: Union[str, TemperatureUnit],
    to_unit: Union[str, TemperatureUnit]
) -> ConversionResult: ...
```
