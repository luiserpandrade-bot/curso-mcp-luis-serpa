"""Tests unitarios de las conversiones con Kelvin.

Derivado de specs/001-temperature-converter/spec.md:
User Story 2 (Celsius <-> Kelvin) y User Story 3 (Fahrenheit <-> Kelvin).
"""

import pytest

from temperature_converter.converter import convert
from temperature_converter.models import TemperatureUnit


class TestCelsiusKelvinConversion:
    """User Story 2 - Acceptance Scenarios 1 a 4."""

    @pytest.mark.parametrize(
        "celsius, expected_kelvin",
        [
            (0.0, 273.15),
            (25.0, 298.15),
            (100.0, 373.15),
            (-273.15, 0.0),
        ],
    )
    def test_celsius_to_kelvin(self, celsius, expected_kelvin):
        result = convert(celsius, "C", "K")
        assert result.value == pytest.approx(expected_kelvin, abs=0.01)
        assert result.target_unit == TemperatureUnit.KELVIN

    @pytest.mark.parametrize(
        "kelvin, expected_celsius",
        [
            (273.15, 0.0),
            (373.15, 100.0),
            (298.15, 25.0),
        ],
    )
    def test_kelvin_to_celsius(self, kelvin, expected_celsius):
        result = convert(kelvin, "K", "C")
        assert result.value == pytest.approx(expected_celsius, abs=0.01)
        assert result.target_unit == TemperatureUnit.CELSIUS


class TestFahrenheitKelvinConversion:
    """User Story 3 - Acceptance Scenarios 1 a 4."""

    @pytest.mark.parametrize(
        "fahrenheit, expected_kelvin",
        [
            (32.0, 273.15),
            (212.0, 373.15),
        ],
    )
    def test_fahrenheit_to_kelvin(self, fahrenheit, expected_kelvin):
        assert convert(fahrenheit, "F", "K").value == pytest.approx(expected_kelvin, abs=0.01)

    @pytest.mark.parametrize(
        "kelvin, expected_fahrenheit",
        [
            (0.0, -459.67),
            (459.67, 367.74),
        ],
    )
    def test_kelvin_to_fahrenheit(self, kelvin, expected_fahrenheit):
        assert convert(kelvin, "K", "F").value == pytest.approx(expected_fahrenheit, abs=0.01)
