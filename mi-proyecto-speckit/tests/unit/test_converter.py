"""Tests for temperature converter core algorithms and dispatcher."""

import pytest
from temperature_converter.converter import convert
from temperature_converter.models import TemperatureUnit


class TestCelsiusFahrenheitConversion:
    """Tests for User Story 1: Bidirectional Celsius <-> Fahrenheit conversions."""

    @pytest.mark.parametrize(
        "celsius, expected_fahrenheit",
        [
            (0.0, 32.0),
            (100.0, 212.0),
            (-40.0, -40.0),
            (37.0, 98.6),
            (25.0, 77.0),
            (-17.78, 0.0),
        ],
    )
    def test_celsius_to_fahrenheit(self, celsius: float, expected_fahrenheit: float) -> None:
        result = convert(celsius, "C", "F")
        assert result.value == pytest.approx(expected_fahrenheit, abs=0.01)
        assert result.target_unit == TemperatureUnit.FAHRENHEIT
        assert result.formatted == f"{expected_fahrenheit:.2f} F"

    @pytest.mark.parametrize(
        "fahrenheit, expected_celsius",
        [
            (32.0, 0.0),
            (212.0, 100.0),
            (-40.0, -40.0),
            (98.6, 37.0),
            (77.0, 25.0),
            (0.0, -17.78),
        ],
    )
    def test_fahrenheit_to_celsius(self, fahrenheit: float, expected_celsius: float) -> None:
        result = convert(fahrenheit, "F", "C")
        assert result.value == pytest.approx(expected_celsius, abs=0.01)
        assert result.target_unit == TemperatureUnit.CELSIUS
        assert result.formatted == f"{expected_celsius:.2f} C"

    def test_celsius_fahrenheit_case_insensitive_aliases(self) -> None:
        assert convert(100, "celsius", "fahrenheit").value == 212.00
        assert convert(212, "FAHRENHEIT", "CELSIUS").value == 100.00
        assert convert(0, "°C", "°F").value == 32.00

    def test_identity_conversions(self) -> None:
        assert convert(25.5, "C", "C").value == 25.50
        assert convert(75.25, "F", "F").value == 75.25
