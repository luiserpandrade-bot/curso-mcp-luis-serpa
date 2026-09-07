# curso-mcp-luis-serpa

Proyecto del taller MCP.
## Environment check — Class 1 check — Class 1┃ Component ┃ Status ┃ Detail┡ Python 3.12              │   OK   │ 3.12.10                                                 ││ uv                       │   OK   │ uv 0.12.9 (9f9286029 2026-09-01 x86_64-pc-windows-msvc) ││ Git                      │   OK   │ git version 2.55.0.windows.4                            ││ Docker                   │   OK   │ Docker version 29.7.2, build a7dcaa6                    ││ .gitignore protects .env │   OK   │ protects .env                                           │└──────────────────────────┴────────┴─────────────────────────────────────────────────────────┘Environment ready. See you in Class 2.
## Clase 2 — APIs de IA Generativa y memoria conversacional

### Conversación de 8 turnos (Paso 7)

Ver evidencia en `entregas/s02/evidencia/memoria.txt`.

### Por qué elegí ventana deslizante

Se eligió la ventana deslizante (sliding window) porque permite mantener el contexto reciente relevante limitando estrictamente el uso máximo de tokens. Es una estrategia liviana y predecible para conversaciones interactivas donde la información remota no requiere almacenamiento permanente.

### Límite de solicitudes provocado (Paso 9)

Ver evidencia en `entregas/s02/evidencia/rate_limit.txt`.

El programa capturó las excepciones de tipo `ClientError` (código 429) y aplicó reintentos con backoff exponencial, evitando caídas inesperadas del script.