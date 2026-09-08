"""Crea la estructura de QA de la Sesión 5: 7 skills, 3 agentes y el hook.

Uso (desde la raíz de mi-proyecto-speckit):
    uv run python setup_qa.py

No sobrescribe nada fuera de .agents/. Si un archivo ya existe, lo reemplaza.
"""

from pathlib import Path

ARCHIVOS = {}

# ---------------------------------------------------------------- SKILLS

ARCHIVOS[".agents/skills/qa-unit/SKILL.md"] = '''---
name: qa-unit
description: Audita los tests unitarios existentes contra specs/*/spec.md (Acceptance Scenarios, Edge Cases, Functional Requirements) y agrega solo lo que falta, sin improvisar qué probar ni duplicar lo ya cubierto.
---
# Instrucciones
1. Lee `specs/*/spec.md` — secciones "Acceptance Scenarios", "Edge Cases" y "Functional Requirements" (revisa también `## Clarifications` si existe: ahí suelen vivir los requisitos agregados después de la implementación original). Si no existe ningún `specs/*/spec.md`, DETENTE y pide que se corra Spec Kit primero — no inventes criterios propios.
2. Si existe `tests/unit/`, revisa los tests que ya hay ahí antes de escribir nada.
3. Para cada escenario, caso borde o FR que corresponda a una función aislada: si ya hay un test que lo cubre, repórtalo como "ya cubierto en `<archivo>`" y no lo dupliques. Si no está cubierto, agrégalo con un assert real — dentro del archivo de `tests/unit/` que corresponda por tema, o en uno nuevo si no encaja en ninguno.
4. No agregues tests para casos que no estén en la spec — si crees que falta algo importante, sugiérelo al final, no lo generes por tu cuenta.
5. Corre `uv run pytest tests/unit/ -v` y reporta cuántos pasaron, cuántos fallaron, y cuántos tests eran nuevos.
'''

ARCHIVOS[".agents/skills/qa-integration/SKILL.md"] = '''---
name: qa-integration
description: Audita el test de integración EN MEMORIA (sin subprocess) existente contra specs/*/spec.md y agrega solo lo que falta, sin improvisar el flujo a probar ni duplicar lo ya cubierto.
---
# Instrucciones
1. Lee `specs/*/spec.md`, sección "Acceptance Scenarios" — identifica los escenarios que requieren que 2+ módulos de tu propio código se conecten (ej. tu CLI llamando a tu lógica de negocio). Si no existe ningún `specs/*/spec.md`, DETENTE y pide que se corra Spec Kit primero.
2. Si existe `tests/integration/`, revisa qué flujo ya prueba antes de escribir nada. Si algún archivo ahí usa `subprocess` para lanzar el programa completo, NO es integración — es un test e2e mal clasificado. No lo toques ni lo dupliques: repórtalo, la skill `qa-e2e` se encarga de reubicarlo.
3. Si el escenario ya está cubierto por un test real en memoria, repórtalo como "ya cubierto en `<archivo>`" y no lo dupliques.
4. Si falta, agrega un test **en memoria** (llama directamente a las funciones que conectan tus módulos, sin lanzar el programa como proceso aparte) en el archivo existente o en uno nuevo dentro de `tests/integration/`.
5. Corre `uv run pytest tests/integration/ -v` y reporta el resultado.
'''

ARCHIVOS[".agents/skills/qa-e2e/SKILL.md"] = '''---
name: qa-e2e
description: Audita los tests end-to-end existentes (proceso completo, vía subprocess) contra specs/*/spec.md y agrega solo lo que falta, sin improvisar el flujo ni duplicar lo ya cubierto.
---
# Instrucciones
1. Lee `specs/*/spec.md`, sección "Acceptance Scenarios" — identifica los escenarios que describen el uso real de punta a punta, como lo usaría la persona que opera el programa. Si no existe ningún `specs/*/spec.md`, DETENTE y pide que se corra Spec Kit primero.
2. Revisa `tests/e2e/` (créala si no existe). Además, revisa si `tests/integration/` tiene algún archivo que en realidad use `subprocess` para lanzar el programa completo — si lo encuentras, muévelo a `tests/e2e/` con `git mv` (no lo reescribas, solo reubícalo) y avisa que lo hiciste.
3. Para cada escenario que no esté cubierto, agrega un test e2e nuevo: invoca el programa completo como lo haría un usuario real (vía `subprocess`, verificando stdout y código de salida), nunca llamando a una función interna directamente.
4. Corre `uv run pytest tests/e2e/ -v` y reporta el resultado.
'''

ARCHIVOS[".agents/skills/qa-coverage/SKILL.md"] = '''---
name: qa-coverage
description: Ejecuta y resume el reporte de cobertura de tests del proyecto, señalando líneas sin probar.
---
# Instrucciones
1. Corre `uv run pytest --cov=src --cov-report=term-missing` (ajusta `src` si tu código no vive bajo esa carpeta).
2. Resume: porcentaje total, y qué líneas "Missing" son casos borde olvidados vs. código no usado.
3. No agregues tests automáticamente — solo diagnostica.
'''

ARCHIVOS[".agents/skills/qa-security/SKILL.md"] = '''---
name: qa-security
description: Revisa el proyecto en busca de secretos expuestos, validación de entradas insuficiente y manejo de excepciones riesgoso.
---
# Instrucciones
1. Busca claves/contraseñas escritas directamente en el código.
2. Revisa validación de entradas (tipo, formato, longitud, rango).
3. Busca `except:` genérico o `except: pass`.
4. Reporta en esta tabla:

| Caso | Lo que se encontró | Corrección sugerida |
|---|---|---|
| 🔑 Secreto expuesto | [hallazgo o "sin hallazgos"] | [sugerencia] |
| 🧪 Validación de entradas | [hallazgo o "sin hallazgos"] | [sugerencia] |
| 🚪 Manejo de excepciones | [hallazgo o "sin hallazgos"] | [sugerencia] |

5. Sin importar si encontraste un secreto quemado en código o no, asegúrate de que exista el patrón correcto para manejarlos en el futuro. **No confíes en leer `.gitignore` como texto — verifica con git directamente**, porque el archivo puede decir cualquier cosa sin que git realmente lo respete, o puede perder una línea entre una corrida y otra sin que se note a simple vista:
   - Si no existe `.env.example`, créalo (con las claves esperadas del proyecto, **sin valores reales** — solo el nombre).
   - Si existe `.env`, corre `git check-ignore -q .env`. Si el código de salida no es 0, `.env` NO está ignorado de verdad — agrega la línea a `.gitignore` y vuelve a verificar, no des por hecho que quedó bien solo por haberla escrito.
   - Si existe `.env`, corre también `git ls-files --error-unmatch .env`. Si el código de salida es 0, `.env` ya está trackeado por git — esto es mucho más grave que solo faltar en `.gitignore`: el secreto puede ya estar en el historial. Repórtalo como hallazgo crítico aparte, no lo mezcles con "sin hallazgos".
   - Si sí encontraste un secreto quemado, la corrección sugerida en la tabla debe ser explícita: moverlo a una variable de entorno leída con `os.environ.get(...)` (o `python-dotenv`), nunca dejarlo como valor literal en el código.
6. Debajo de la tabla (no dentro — la tabla se queda en exactamente 3 filas), agrega una sección `## Acciones de higiene aplicadas` listando cada cosa que hiciste en el punto 5 (ej. "Agregué `.env` a `.gitignore`, no estaba ignorado") o "Ninguna, ya estaba en orden" si no hiciste nada. Una corrección real que no se reporta es tan mala como si no se hubiera hecho.
7. Guarda la tabla completa MÁS la sección de acciones en `hallazgos-seguridad.md` (sobrescribiendo si ya existe) — no te quedes solo con mostrarlo en el chat, el archivo es el entregable.
8. No corrijas el código de negocio automáticamente — la única acción que sí tomas por tu cuenta es la del punto 5 (higiene de `.env.example`/`.gitignore`), el resto solo lo diagnosticas.
'''

ARCHIVOS[".agents/skills/qa-report/SKILL.md"] = '''---
name: qa-report
description: Ejecuta el script de reporte de calidad y genera reporte-qa.html.
---
# Instrucciones
1. Corre: `uv run python .agents/skills/qa-report/generar_reporte.py`
2. Abre `reporte-qa.html` y reporta solo el veredicto final y un resumen de una línea.
3. Si "REQUIERE CORRECCIÓN", lista los 2-3 problemas más importantes.
'''

ARCHIVOS[".agents/skills/qa-orchestrate/SKILL.md"] = '''---
name: qa-orchestrate
description: Ejecuta el flujo completo de calidad invocando en orden a tester-agent, security-agent y report-agent, sin pedir confirmación entre cada uno.
---
# Instrucciones
1. Verifica que exista `specs/*/spec.md`. Si falta, detente y pide que se corra Spec Kit primero.
2. Invoca al agente tester-agent (su propia tarea vive en su `agent.md`). Espera a que termine por completo.
3. Invoca al agente security-agent (su propia tarea vive en su `agent.md`). Espera a que termine por completo.
4. Invoca al agente report-agent (su propia tarea vive en su `agent.md`).
5. Presenta al usuario el veredicto final, con un resumen de 1 línea de qué hizo cada agente en el camino.

No pidas confirmación entre fase y fase — este es un flujo automático de punta a punta. Si `agy` te pide aprobar el permiso de invocación de cada agente, apruébalo y sigue.
'''

# ------------------------------------------------- SCRIPT DEL REPORTE

ARCHIVOS[".agents/skills/qa-report/generar_reporte.py"] = '''"""Genera reporte-qa.html combinando resultados de tests, cobertura y una
revisión de seguridad simple. Es Python puro: no usa IA para redactar el
reporte, solo para invocar esta skill."""

import json
import re
import subprocess
from pathlib import Path

UMBRAL_COBERTURA = 50.0  # % mínimo para aprobar
PATRONES_SECRETOS = [
    r"(?i)(api[_-]?key|secret|password|token)\\s*=\\s*[\'\\"][^\'\\"]{6,}[\'\\"]",
]


def correr_tests():
    subprocess.run(
        [
            "uv", "run", "pytest",
            "--json-report", "--json-report-file=.report.json",
            "--cov=src", "--cov-report=json:.coverage.json",
            "-q",
        ],
        capture_output=True,
    )
    reporte = json.loads(Path(".report.json").read_text()) if Path(".report.json").exists() else {}
    cobertura = json.loads(Path(".coverage.json").read_text()) if Path(".coverage.json").exists() else {}
    resumen = reporte.get("summary", {})
    total_pct = cobertura.get("totals", {}).get("percent_covered", 0.0)
    return {
        "pasaron": resumen.get("passed", 0),
        "fallaron": resumen.get("failed", 0),
        "cobertura_pct": round(total_pct, 1),
    }


def buscar_secretos():
    hallazgos = []
    for archivo in Path("src").rglob("*.py"):
        texto = archivo.read_text(errors="ignore")
        for patron in PATRONES_SECRETOS:
            for m in re.finditer(patron, texto):
                hallazgos.append(f"{archivo}: {m.group(0)}")
    return hallazgos


def revisar_higiene_secretos():
    """No confía en leer .gitignore como texto — usa git como fuente de verdad,
    porque un .gitignore puede decir cualquier cosa sin que git realmente lo respete
    (o puede perder una línea sin que se note a simple vista)."""
    tiene_env_example = Path(".env.example").exists()
    env_existe = Path(".env").exists()

    env_tracked = False
    if env_existe:
        r = subprocess.run(["git", "ls-files", "--error-unmatch", ".env"], capture_output=True)
        env_tracked = r.returncode == 0

    if env_existe:
        r = subprocess.run(["git", "check-ignore", "-q", ".env"], capture_output=True)
        env_ignorado = r.returncode == 0
    elif Path(".gitignore").exists():
        # todavía no hay .env, pero igual conviene que la regla ya exista para cuando aparezca
        env_ignorado = ".env" in Path(".gitignore").read_text()
    else:
        env_ignorado = False

    return {
        "env_example": tiene_env_example,
        "env_existe": env_existe,
        "env_tracked": env_tracked,
        "gitignore_ok": env_ignorado,
    }


def construir_html(tests, secretos, higiene):
    # env_tracked es la peor señal: el secreto puede ya estar en el historial de git,
    # no alcanza con arreglar .gitignore a futuro.
    higiene_ok = higiene["env_example"] and higiene["gitignore_ok"] and not higiene["env_tracked"]
    aprobado = (
        tests["fallaron"] == 0
        and tests["cobertura_pct"] >= UMBRAL_COBERTURA
        and not secretos
        and higiene_ok
    )
    veredicto = "APROBADO" if aprobado else "REQUIERE CORRECCIÓN"
    color = "#1a7f37" if aprobado else "#c0341d"
    filas_secretos = "".join(f"<li>{h}</li>" for h in secretos) or "<li>Sin hallazgos</li>"

    if higiene["env_tracked"]:
        higiene_msg = "🔴 CRÍTICO: .env está trackeado por git — el secreto puede ya estar en el historial. No alcanza con arreglar .gitignore, hay que sacarlo del historial."
    elif higiene["env_existe"] and not higiene["gitignore_ok"]:
        higiene_msg = "🟡 .env existe y NO está ignorado — riesgo de que se cuele en el próximo commit."
    elif not higiene["env_example"]:
        higiene_msg = "🟡 Falta .env.example."
    else:
        higiene_msg = "✅ En orden."

    html = f"""<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Reporte QA</title>
<style>body{{font-family:sans-serif;margin:2rem}}h1{{color:{color}}}</style></head>
<body>
<h1>{veredicto}</h1>
<h2>Tests</h2>
<p>Pasaron: {tests[\'pasaron\']} · Fallaron: {tests[\'fallaron\']}</p>
<h2>Cobertura</h2>
<p>{tests[\'cobertura_pct\']}% (umbral: {UMBRAL_COBERTURA}%)</p>
<h2>Secretos expuestos</h2>
<ul>{filas_secretos}</ul>
<h2>Higiene de secretos</h2>
<p>.env.example: {"✅" if higiene["env_example"] else "❌ falta"} · .env ignorado por git: {"✅" if higiene["gitignore_ok"] else "❌"} · .env trackeado: {"🔴 SÍ" if higiene["env_tracked"] else "✅ no"}</p>
<p>{higiene_msg}</p>
</body></html>"""
    Path("reporte-qa.html").write_text(html, encoding="utf-8")
    print(veredicto)


if __name__ == "__main__":
    resultados_tests = correr_tests()
    hallazgos_secretos = buscar_secretos()
    higiene_secretos = revisar_higiene_secretos()
    construir_html(resultados_tests, hallazgos_secretos, higiene_secretos)
'''

# ---------------------------------------------------------------- AGENTES

ARCHIVOS[".agents/agents/tester-agent/agent.md"] = '''---
name: tester-agent
description: Especialista en calidad funcional. Úsalo para generar o correr tests unitarios, de integración, end-to-end, y medir cobertura.
subagent: true
---
# Tester Agent

Eres el Tester-Agent. Tu única responsabilidad es la calidad funcional del código:
que existan tests en las tres capas (unitaria, integración en memoria, end-to-end), que pasen, y que la cobertura sea razonable.

Nunca improvises qué probar. Siempre exige que exista `specs/*/spec.md` antes de generar tests —
si no existe, detente y pide que se corra Spec Kit primero. No te ocupes de seguridad — eso lo hace otro agente.
No generes el reporte final — eso también es de otro agente.

Cuando te invoquen:
1. Verifica que exista `specs/*/spec.md`.
2. Usa la skill qa-unit.
3. Usa la skill qa-integration.
4. Usa la skill qa-e2e.
5. Usa la skill qa-coverage.
6. Resume tus hallazgos en 3-5 líneas, sin extenderte.

## Tarea
Verificar la calidad funcional de este proyecto.

## Criterios de aceptación
- [ ] Genera y corre tests unitarios según specs/*/spec.md
- [ ] Genera y corre el test de integración (en memoria) según specs/*/spec.md
- [ ] Genera y corre el test end-to-end (proceso completo) según specs/*/spec.md
- [ ] Reporta el % de cobertura y qué líneas quedaron sin probar

## Entregable esperado
Resumen de 3-5 líneas, sin código completo pegado en el chat.
'''

ARCHIVOS[".agents/agents/security-agent/agent.md"] = '''---
name: security-agent
description: Especialista en seguridad básica. Úsalo para revisar secretos expuestos, validación de entradas y manejo de excepciones.
subagent: true
---
# Security Agent

Eres el Security-Agent. Tu única responsabilidad es encontrar riesgos de seguridad básicos.
No te importa si los tests pasan o no — eso es del Tester-Agent.

Cuando te invoquen:
1. Usa la skill qa-security.
2. Presenta la tabla de 3 filas tal como la generó la skill, sin resumirla de más.

## Tarea
Revisar riesgos de seguridad básicos en este proyecto.

## Criterios de aceptación
- [ ] Revisa secretos expuestos, validación de entradas, manejo de excepciones
- [ ] Reporta en la tabla de exactamente 3 filas

## Entregable esperado
La tabla, sin agregar hallazgos fuera de esas 3 categorías.
'''

ARCHIVOS[".agents/agents/report-agent/agent.md"] = '''---
name: report-agent
description: Consolida resultados de calidad en un reporte final. Úsalo al final del proceso, después del Tester y Security.
subagent: true
---
# Report Agent

Eres el Report-Agent. Solo consolidas — no vuelves a analizar nada por tu cuenta,
confías en lo que ya hicieron el Tester-Agent y el Security-Agent.

Cuando te invoquen:
1. Usa la skill qa-report.
2. Presenta el veredicto final de forma clara y breve.

## Tarea
Generar el veredicto final de calidad.

## Criterios de aceptación
- [ ] Ejecuta el script de reporte (no redacta el reporte con IA)
- [ ] Presenta el veredicto y, si aplica, los 2-3 problemas más importantes

## Entregable esperado
Veredicto + resumen de una línea, no el HTML completo pegado en el chat.
'''

# ------------------------------------------------------------------ HOOK

HOOK_SH = '''#!/bin/bash
# agy ejecuta este script con cwd = .agents/ (la carpeta que contiene hooks.json),
# no la raíz del proyecto — por eso subimos un nivel antes de correr pytest.
cd ..
if uv run pytest --tb=no -q > /tmp/gate-tests-agy.log 2>&1; then
  echo '{}'
else
  echo '{"decision":"continue","reason":"Hay tests fallando. No te detengas -- corrige el código antes de terminar."}'
fi
'''

ARCHIVOS[".agents/hooks.json"] = '''{
  "gate-tests": {
    "Stop": [
      { "type": "command", "command": "./hooks/gate-tests.sh", "timeout": 30 }
    ]
  }
}
'''


def main():
    raiz = Path(".").resolve()
    if not (raiz / "pyproject.toml").exists():
        print("ERROR: ejecuta este script desde la raiz de mi-proyecto-speckit")
        return

    for ruta, contenido in ARCHIVOS.items():
        destino = raiz / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(contenido, encoding="utf-8", newline="\n")
        print(f"  creado  {ruta}")

    # El hook es bash: necesita finales de linea LF aunque estemos en Windows
    hook = raiz / ".agents/hooks/gate-tests.sh"
    hook.parent.mkdir(parents=True, exist_ok=True)
    with open(hook, "w", encoding="utf-8", newline="\n") as f:
        f.write(HOOK_SH)
    print("  creado  .agents/hooks/gate-tests.sh  (finales de linea LF)")

    print()
    print(f"Listo: {len(ARCHIVOS) + 1} archivos.")
    print("Siguiente: git update-index --chmod=+x .agents/hooks/gate-tests.sh")


if __name__ == "__main__":
    main()
