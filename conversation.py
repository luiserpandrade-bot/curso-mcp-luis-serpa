"""In-memory conversation history with sliding window and rate limit handling."""

import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-2.5-flash"
SYSTEM_INSTRUCTION = "Eres un asistente breve. Respondes en español."

history: list[dict] = []
MAX_TURNS = 10


def trim_history() -> None:
    max_entries = MAX_TURNS * 2
    if len(history) > max_entries:
        del history[:-max_entries]


def send(message: str, _retries: int = 0) -> str:
    trim_history()
    history.append({"role": "user", "parts": [{"text": message}]})

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
        )
    except errors.ClientError as exc:
        if exc.code == 429 and _retries < 3:
            wait = 2 ** _retries
            print(f"[429] Límite de RPM alcanzado. Reintentando en {wait}s...")
            time.sleep(wait)
            history.pop()
            return send(message, _retries=_retries + 1)
        history.pop()
        return f"Error del cliente ({exc.code}): {exc.message}. No se reintenta."
    except errors.ServerError as exc:
        if _retries < 3:
            wait = 2 ** _retries
            print(f"[{exc.code}] Error del servidor. Reintentando en {wait}s...")
            time.sleep(wait)
            history.pop()
            return send(message, _retries=_retries + 1)
        history.pop()
        return f"El servicio no respondió tras varios intentos ({exc.code})."

    finish_reason = str(response.candidates[0].finish_reason)
    if "MAX_TOKENS" in finish_reason:
        print("[warning] Respuesta truncada por max_output_tokens.")

    u = response.usage_metadata
    print(f"[Tokens: Prompt={u.prompt_token_count}, Res={u.candidates_token_count}, Total={u.total_token_count}]")

    history.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text


def trigger_rate_limit() -> None:
    global history
    history = []
    print("\n--- Provocando Rate Limit (429) ---")
    for i in range(1, 21):
        print(f"Request {i}: {send(f'Cuenta hasta {i}.')}")


def main() -> None:
    print("--- Conversación de 8 turnos ---")
    prompts = [
        "Me llamo Alex y mi color favorito es el verde.",
        "¿Qué framework de Python vimos en la Clase 1?",
        "Dame un ejemplo de dato que no cabe en un int.",
        "¿Qué hace el comando uv init?",
        "Explica en una frase qué es un token.",
        "¿Qué significa que una API sea stateless?",
        "¿Para qué sirve un archivo .env?",
        "¿Cómo me llamo y cuál es mi color favorito?"
    ]
    
    for idx, prompt in enumerate(prompts, 1):
        print(f"\nTurno {idx}: {prompt}")
        ans = send(prompt)
        print(f"BOT: {ans}")

    trigger_rate_limit()


if __name__ == "__main__":
    main()
