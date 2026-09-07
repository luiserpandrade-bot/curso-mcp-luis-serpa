"""Data models, enums, and domain exceptions for temperature converter."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Union


# --- Domain Exceptions ---

class TemperatureError(ValueError):
    """Base domain exception for temperature converter errors."""
    pass


class AbsoluteZeroError(TemperatureError):
    """Raised when a temperature is below physical absolute zero."""
    pass


class InvalidUnitError(TemperatureError):
    """Raised when an unrecognized temperature unit is provided."""
    pass


class InvalidInputError(TemperatureError):
    """Raised when temperature numeric input is invalid (non-numeric, NaN, or Inf)."""
    pass


# --- Enums and Models ---

class TemperatureUnit(Enum):
    """Supported temperature measurement units."""
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"

    @property
    def symbol(self) -> str:
        """Canonical single-letter symbol."""
        return self.value

    @classmethod
    def from_str(cls, value: Union[str, TemperatureUnit]) -> TemperatureUnit:
        """Parse unit from string or existing enum instance.
        
        Supports full names, abbreviations, degrees symbols, and case-insensitivity.
        """
        if isinstance(value, cls):
            return value

        if not isinstance(value, str):
            raise InvalidUnitError(f"Unit must be a string or TemperatureUnit, got {type(value).__name__}")

        normalized = value.strip().lower().replace("°", "").replace("deg", "")
        alias_map = {
            "c": cls.CELSIUS,
            "celsius": cls.CELSIUS,
            "célsius": cls.CELSIUS,
            "f": cls.FAHRENHEIT,
            "fahrenheit": cls.FAHRENHEIT,
            "k": cls.KELVIN,
            "kelvin": cls.KELVIN,
        }

        if normalized in alias_map:
            return alias_map[normalized]

        raise InvalidUnitError(
            f"Unrecognized temperature unit '{value}'. Supported units: C, F, K."
        )


# Physical lower bounds (absolute zero)
ABSOLUTE_ZERO_BOUNDS: dict[TemperatureUnit, float] = {
    TemperatureUnit.KELVIN: 0.0,
    TemperatureUnit.CELSIUS: -273.15,
    TemperatureUnit.FAHRENHEIT: -459.67,
}


@dataclass(frozen=True)
class Temperature:
    """Immutable representation of a temperature measurement."""
    value: float
    unit: TemperatureUnit

    def __post_init__(self) -> None:
        # Validate unit
        if not isinstance(self.unit, TemperatureUnit):
            object.__setattr__(self, "unit", TemperatureUnit.from_str(self.unit))

        # Validate numeric value
        try:
            val = float(self.value)
        except (ValueError, TypeError) as err:
            raise InvalidInputError(f"Invalid numeric temperature value: {self.value}") from err

        if not math.isfinite(val):
            raise InvalidInputError(f"Temperature value must be finite, got: {val}")

        object.__setattr__(self, "value", val)

        # Enforce absolute zero physical bound
        min_bound = ABSOLUTE_ZERO_BOUNDS[self.unit]
        # Round comparison to 4 decimals to avoid micro precision float anomalies at exact bound
        if round(self.value, 4) < min_bound:
            raise AbsoluteZeroError(
                f"Temperature {self.value:.2f} {self.unit.symbol} is below absolute zero "
                f"({min_bound:.2f} {self.unit.symbol})."
            )


@dataclass(frozen=True)
class ConversionResult:
    """Represents the outcome of a temperature conversion."""
    source: Temperature
    target_unit: TemperatureUnit
    value: float
    formatted: str

    def __init__(self, source: Temperature, target_unit: TemperatureUnit, value: float) -> None:
        target_unit_enum = TemperatureUnit.from_str(target_unit)
        rounded_val = round(float(value), 2)
        # Avoid -0.00
        if rounded_val == 0.0:
            rounded_val = 0.0

        object.__setattr__(self, "source", source)
        object.__setattr__(self, "target_unit", target_unit_enum)
        object.__setattr__(self, "value", rounded_val)
        object.__setattr__(self, "formatted", f"{rounded_val:.2f} {target_unit_enum.symbol}")
