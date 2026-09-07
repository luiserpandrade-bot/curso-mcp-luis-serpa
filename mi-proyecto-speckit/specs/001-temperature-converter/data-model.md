# Data Model: Temperature Unit Converter

**Feature**: Temperature Unit Converter (`001-temperature-converter`)  
**Date**: 2026-09-07  
**Status**: Completed  

---

## 1. Entities & Value Objects

### 1.1 `TemperatureUnit` (Enum)

Represents supported temperature measurement scales.

| Identifier | Canonical Symbol | Valid Aliases (Case-Insensitive) |
|------------|------------------|----------------------------------|
| `CELSIUS`    | `C`              | `c`, `celsius`, `célsius`        |
| `FAHRENHEIT` | `F`              | `f`, `fahrenheit`                |
| `KELVIN`     | `K`              | `k`, `kelvin`                    |

**Methods / Properties**:
- `from_str(value: str) -> TemperatureUnit`: Parses case-insensitive strings/symbols or raises `InvalidUnitError`.
- `symbol: str`: Returns canonical single-character symbol (`C`, `F`, `K`).

---

### 1.2 `Temperature` (Value Object / Dataclass)

Represents an immutable temperature measurement with validation against physical laws.

| Field Name | Type              | Description                                             | Constraints                               |
|------------|-------------------|---------------------------------------------------------|-------------------------------------------|
| `value`    | `float`           | The scalar numeric magnitude of temperature             | Must be finite (not NaN or Inf)           |
| `unit`     | `TemperatureUnit` | The measurement scale                                   | Must be a member of `TemperatureUnit`     |

**Validation Rules**:
- **Absolute Zero Lower Bound**:
  - If `unit == TemperatureUnit.KELVIN`: `value >= 0.0`
  - If `unit == TemperatureUnit.CELSIUS`: `value >= -273.15`
  - If `unit == TemperatureUnit.FAHRENHEIT`: `value >= -459.67`
- Violation raises `AbsoluteZeroError(f"Temperature {value} {unit.symbol} is below absolute zero.")`

---

### 1.3 `ConversionResult` (Value Object / Dataclass)

Represents the computed outcome of a conversion operation.

| Field Name     | Type              | Description                                          | Constraints                               |
|----------------|-------------------|------------------------------------------------------|-------------------------------------------|
| `source`       | `Temperature`     | The original input temperature measurement           | Valid `Temperature` object               |
| `target_unit`  | `TemperatureUnit` | The desired destination scale                        | Valid `TemperatureUnit`                   |
| `value`        | `float`           | The converted numerical value                        | Rounded strictly to 2 decimal places      |
| `formatted`    | `str`             | Human-readable string representation (e.g. `32.00 F`)| Formatted with exactly 2 decimal places   |

---

## 2. Conversion Relationship Matrix & Formulas

All transformations use exact scientific definitions:

```mermaid
graph LR
    C[Celsius] <-->|F = C * 9/5 + 32<br/>C = (F - 32) * 5/9| F[Fahrenheit]
    C <-->|K = C + 273.15<br/>C = K - 273.15| K[Kelvin]
    F <-->|Direct or via Celsius| K
```

| From Unit | To Unit | Mathematical Formula |
|-----------|---------|----------------------|
| `CELSIUS` | `FAHRENHEIT` | $F = (C \times \frac{9}{5}) + 32$ |
| `FAHRENHEIT` | `CELSIUS` | $C = (F - 32) \times \frac{5}{9}$ |
| `CELSIUS` | `KELVIN` | $K = C + 273.15$ |
| `KELVIN` | `CELSIUS` | $C = K - 273.15$ |
| `FAHRENHEIT` | `KELVIN` | $K = (F - 32) \times \frac{5}{9} + 273.15$ |
| `KELVIN` | `FAHRENHEIT` | $F = (K - 273.15) \times \frac{9}{5} + 32$ |
| Unit $X$ | Same Unit $X$ | Identity: $X = X$ (rounded to 2 decimal places) |

---

## 3. Exception Hierarchy

```text
Exception
└── ValueError
    ├── TemperatureError (Base domain exception)
    │   ├── AbsoluteZeroError (Violates physical absolute zero lower bound)
    │   └── InvalidUnitError (Unrecognized unit identifier)
    └── InvalidInputError (Non-numeric temperature value or missing argument)
```
