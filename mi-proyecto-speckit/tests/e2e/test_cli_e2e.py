"""Tests end-to-end: el programa completo como lo usaria una persona real.

Lanza el proceso via subprocess y verifica stdout y codigo de salida.
Nunca llama funciones internas directamente.

Derivado de specs/001-temperature-converter/spec.md, seccion "Acceptance Scenarios".
"""

import subprocess
import sys

import pytest


def correr(*argumentos):
    """Invoca el programa completo como proceso aparte."""
    return subprocess.run(
        [sys.executable, "-m", "temperature_converter.cli", *argumentos],
        capture_output=True,
        text=True,
    )


class TestUsoNormal:
    @pytest.mark.parametrize(
        "argumentos, esperado",
        [
            (("25", "C", "F"), "77.00 F"),
            (("-40", "C", "F"), "-40.00 F"),
            (("25", "C", "K"), "298.15 K"),
            (("0", "K", "F"), "-459.67 F"),
        ],
    )
    def test_conversion_desde_la_terminal(self, argumentos, esperado):
        proceso = correr(*argumentos)
        assert proceso.returncode == 0
        assert proceso.stdout.strip() == esperado


class TestUsoIncorrecto:
    def test_entrada_no_numerica(self):
        proceso = correr("abc", "C", "F")
        assert proceso.returncode == 1
        assert "Error" in proceso.stdout

    def test_bajo_cero_absoluto(self):
        proceso = correr("-300", "C", "F")
        assert proceso.returncode == 1
        assert "Error" in proceso.stdout

    def test_sin_argumentos(self):
        proceso = correr()
        assert proceso.returncode == 1
        assert "Uso:" in proceso.stdout
