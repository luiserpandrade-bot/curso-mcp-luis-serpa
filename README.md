# curso-mcp-luis-serpa

Proyecto del taller MCP.

### Clase 2 — APIs de IA Generativa y memoria conversacional

### Conversación de 8 turnos (Paso 7)

Ver evidencia en ntregas/s02/evidencia/memoria.txt.

### Por qué elegí ventana deslizante

Se eligió la ventana deslizante (sliding window) porque permite mantener el contexto reciente relevante limitando estrictamente el uso máximo de tokens. Es una estrategia liviana y predecible para conversaciones interactivas donde la información remota no requiere almacenamiento permanente.

### Límite de solicitudes provocado (Paso 9)

Ver evidencia en ntregas/s02/evidencia/rate_limit.txt.

El programa capturó las excepciones de tipo ClientError (código 429) y aplicó reintentos con backoff exponencial, evitando caídas inesperadas del script.
