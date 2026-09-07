import pytest
from clase_sdd.converter import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    celsius_to_kelvin,
    kelvin_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_to_fahrenheit,
    convert_temperature,
)


class TestCelsiusFahrenheit:
    """Criterio: Convierte correctamente de Celsius a Fahrenheit y viceversa."""

    def test_celsius_to_fahrenheit_standard(self):
        assert celsius_to_fahrenheit(0) == 32.0
        assert celsius_to_fahrenheit(100) == 212.0
        assert celsius_to_fahrenheit(37) == 98.6
        assert celsius_to_fahrenheit(-40) == -40.0

    def test_fahrenheit_to_celsius_standard(self):
        assert fahrenheit_to_celsius(32) == 0.0
        assert fahrenheit_to_celsius(212) == 100.0
        assert fahrenheit_to_celsius(98.6) == 37.0
        assert fahrenheit_to_celsius(-40) == -40.0


class TestCelsiusKelvin:
    """Criterio: Convierte correctamente de Celsius a Kelvin y viceversa."""

    def test_celsius_to_kelvin_standard(self):
        assert celsius_to_kelvin(0) == 273.15
        assert celsius_to_kelvin(100) == 373.15
        assert celsius_to_kelvin(-273.15) == 0.0

    def test_kelvin_to_celsius_standard(self):
        assert kelvin_to_celsius(273.15) == 0.0
        assert kelvin_to_celsius(373.15) == 100.0
        assert kelvin_to_celsius(0) == -273.15


class TestDecimalRounding:
    """Criterio: Redondea el resultado a 2 decimales."""

    def test_rounding_to_two_decimals(self):
        # 1 Celsius to Fahrenheit is 33.8
        # 33 Celsius to Fahrenheit is 91.4
        # 35.556 C to F
        result = celsius_to_fahrenheit(35.555)
        assert result == 96.00

        # Fahrenheit to Celsius with recurring decimals: 100 F = 37.777... C -> 37.78 C
        result_c = fahrenheit_to_celsius(100)
        assert result_c == 37.78

        # Kelvin to Celsius rounding
        assert kelvin_to_celsius(300.5555) == 27.41


class TestRejectNegativeKelvin:
    """Criterio: Rechaza una temperatura en Kelvin menor a 0."""

    def test_reject_negative_kelvin_directly(self):
        with pytest.raises(ValueError, match="menor a 0 K"):
            kelvin_to_celsius(-1)

        with pytest.raises(ValueError, match="menor a 0 K"):
            kelvin_to_fahrenheit(-0.01)

    def test_reject_temperature_below_absolute_zero(self):
        # -273.16 C is below 0 K
        with pytest.raises(ValueError, match="menor a 0 K"):
            celsius_to_kelvin(-273.16)

        with pytest.raises(ValueError, match="menor a 0 K"):
            celsius_to_fahrenheit(-275)

        # Below absolute zero in Fahrenheit (-459.67 F = 0 K)
        with pytest.raises(ValueError, match="menor a 0 K"):
            fahrenheit_to_kelvin(-460)


class TestConvertTemperatureFunction:
    """Pruebas de la función unificada convert_temperature."""

    def test_convert_valid_units(self):
        assert convert_temperature(100, "C", "F") == 212.0
        assert convert_temperature(212, "F", "C") == 100.0
        assert convert_temperature(0, "C", "K") == 273.15
        assert convert_temperature(273.15, "K", "C") == 0.0
        assert convert_temperature(32, "F", "K") == 273.15
        assert convert_temperature(273.15, "K", "F") == 32.0

    def test_same_unit(self):
        assert convert_temperature(25.556, "C", "C") == 25.56
        assert convert_temperature(100.1, "F", "F") == 100.10

    def test_same_unit_rejects_negative_kelvin(self):
        with pytest.raises(ValueError, match="menor a 0 K"):
            convert_temperature(-1, "K", "K")

    def test_case_insensitivity_and_full_names(self):
        assert convert_temperature(100, "celsius", "fahrenheit") == 212.0
        assert convert_temperature(0, "Celsius", "Kelvin") == 273.15

    def test_invalid_unit_raises_error(self):
        with pytest.raises(ValueError, match="Unidad desconocida"):
            convert_temperature(100, "Rankine", "C")

    def test_convert_temperature_negative_kelvin_rejection(self):
        with pytest.raises(ValueError, match="menor a 0 K"):
            convert_temperature(-5, "K", "C")
