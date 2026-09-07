"""Calls Gemini with a system instruction and explicit generation parameters."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = (
    "Eres un instructor de programación para principiantes. "
    "Respondes en español, máximo 3 frases. "
    "Sin jerga sin explicar, sin inventar funciones."
)


def ask(prompt: str, temperature: float = 0.7) -> tuple[str, str]:
    """Returns (text, finish_reason)."""
    response = client.models.generate_content(
        model=MODEL,
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=temperature,
            max_output_tokens=200,
        ),
    )
    
    u = response.usage_metadata
    print(f"--- Usage Info ---")
    print(f"prompt tokens   : {u.prompt_token_count}")
    print(f"response tokens : {u.candidates_token_count}")
    print(f"TOTAL tokens    : {u.total_token_count}")
    
    finish_reason = str(response.candidates[0].finish_reason)
    if "MAX_TOKENS" in finish_reason:
        print("[warning] La respuesta viene truncada por max_output_tokens.")
    return response.text, finish_reason


def main() -> None:
    text, _ = ask("¿Qué opinas de var en JS?")
    print("\nBOT:", text)


if __name__ == "__main__":
    main()
