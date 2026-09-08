"""Tests de integracion EN MEMORIA: la CLI conectada con la logica de conversion.

Llama directamente a temperature_converter.cli.main() con sys.argv parcheado,
sin lanzar el programa como proceso aparte (eso es responsabilidad de tests/e2e/).

Derivado de specs/001-temperature-converter/spec.md, seccion "Acceptance Scenarios".
"""

import sys

import pytest

from temperature_converter.cli import main


def ejecutar(monkeypatch, capsys, *argumentos):
    """Corre la CLI en memoria y devuelve (stdout, codigo_de_salida)."""
    monkeypatch.setattr(sys, "argv", ["convertidor-temperatura", *argumentos])
    codigo = 0
    try:
        main()
    except SystemExit as exc:
        codigo = exc.code
    return capsys.readouterr().out.strip(), codigo


class TestConversionesValidas:
    """La CLI entrega el resultado de la logica de negocio con el formato de la spec."""

    @pytest.mark.parametrize(
        "argumentos, esperado",
        [
            (("25", "C", "F"), "77.00 F"),
            (("0", "C", "F"), "32.00 F"),
            (("100", "C", "F"), "212.00 F"),
            (("0", "C", "K"), "273.15 K"),
            (("212", "F", "K"), "373.15 K"),
            (("100", "F", "K"), "310.93 K"),
        ],
    )
    def test_salida_con_dos_decimales(self, monkeypatch, capsys, argumentos, esperado):
        """FR-004 / SC-002: la salida visible debe tener exactamente 2 decimales."""
        salida, codigo = ejecutar(monkeypatch, capsys, *argumentos)
        assert codigo == 0
        assert salida == esperado


class TestErroresPropagados:
    """Los errores de la capa de negocio llegan al usuario con codigo de salida != 0."""

    def test_valor_no_numerico(self, monkeypatch, capsys):
        salida, codigo = ejecutar(monkeypatch, capsys, "abc", "C", "F")
        assert codigo == 1
        assert salida.startswith("Error:")

    def test_kelvin_negativo(self, monkeypatch, capsys):
        """FR-005 propagado hasta la CLI."""
        salida, codigo = ejecutar(monkeypatch, capsys, "-1", "K", "C")
        assert codigo == 1
        assert salida.startswith("Error:")

    def test_faltan_argumentos(self, monkeypatch, capsys):
        salida, codigo = ejecutar(monkeypatch, capsys, "25")
        assert codigo == 1
        assert "Uso:" in salida
