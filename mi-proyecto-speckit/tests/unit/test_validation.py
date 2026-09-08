"""Tests unitarios de validacion y casos borde.

Derivado de specs/001-temperature-converter/spec.md:
User Story 4, seccion "Edge Cases" y FR-004 / FR-005 / FR-006 / FR-007 / FR-008.
"""

import pytest

from temperature_converter.converter import convert


class TestAbsoluteZeroRejection:
    """User Story 4 - FR-005 y FR-006."""

    def test_kelvin_below_zero_is_rejected(self):
        with pytest.raises(ValueError):
            convert(-1.0, "K", "C")

    def test_celsius_below_absolute_zero_is_rejected(self):
        with pytest.raises(ValueError):
            convert(-274.0, "C", "F")

    def test_fahrenheit_below_absolute_zero_is_rejected(self):
        with pytest.raises(ValueError):
            convert(-460.0, "F", "C")

    def test_error_message_is_descriptive(self):
        """FR-007: el mensaje debe explicar el motivo, no ser generico."""
        with pytest.raises(ValueError) as exc:
            convert(-1.0, "K", "C")
        assert "0 K" in str(exc.value) or "absoluto" in str(exc.value).lower()

    def test_invalid_unit_is_rejected(self):
        """FR-007: unidad no soportada tambien debe rechazarse."""
        with pytest.raises(ValueError):
            convert(25.0, "C", "Rankine")


class TestEdgeCases:
    """Seccion "Edge Cases" de la spec."""

    def test_absolute_zero_boundary_is_accepted(self):
        """0.00 K debe dar -273.15 C y -459.67 F, no ser rechazado."""
        assert convert(0.0, "K", "C").value == pytest.approx(-273.15, abs=0.01)
        assert convert(0.0, "K", "F").value == pytest.approx(-459.67, abs=0.01)

    def test_rounding_precision(self):
        """100 F son 37.777... C y deben redondearse a 37.78."""
        assert convert(100.0, "F", "C").value == 37.78

    def test_extreme_high_temperature(self):
        """Superficie del sol (~5778 K) sin anomalias de truncamiento."""
        assert convert(5778.0, "K", "C").value == pytest.approx(5504.85, abs=0.01)
        assert convert(5778.0, "K", "F").value == pytest.approx(9940.73, abs=0.01)

    def test_no_negative_zero(self):
        """-17.78 C da -0.004 F: no debe mostrarse como -0.00."""
        assert convert(-17.78, "C", "F").formatted == "0.00 F"


class TestFormattingRequirements:
    """FR-004 y FR-008."""

    @pytest.mark.parametrize(
        "value, origen, destino, esperado",
        [
            (0.0, "C", "F", "32.00 F"),
            (100.0, "C", "F", "212.00 F"),
            (25.0, "C", "K", "298.15 K"),
            (32.0, "F", "K", "273.15 K"),
        ],
    )
    def test_formatted_always_has_two_decimals(self, value, origen, destino, esperado):
        """FR-004: todo resultado se formatea a exactamente 2 decimales."""
        assert convert(value, origen, destino).formatted == esperado

    def test_identity_conversion_kelvin(self):
        """FR-008: identidad tambien en Kelvin."""
        assert convert(300.5, "K", "K").formatted == "300.50 K"
