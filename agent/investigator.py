
import httpx
from ollama import Client, ResponseError

from agent.prompts import SYSTEM_PROMPT


# Ollama model configuration
MODEL_NAME = "qwen2.5-coder:latest"

# Create Ollama client
client = Client(
    timeout=httpx.Timeout(300.0, connect=10.0)
)


def investigate_error(source_code, traceback_text):
    """
    Analyze Python errors using a local Ollama model.
    """

    # Prepare investigation prompt
    user_prompt = f"""
Investigate the following Python program.

PYTHON SOURCE CODE:
{source_code}

ERROR TRACEBACK:
{traceback_text}

Explain the error and suggest a correction.
"""

    try:
        # Send request to Ollama
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                "temperature": 0.2,
                "num_predict": 350,
                "num_ctx": 2048
            }
        )

        return (
            response.message.content
            or "No explanation returned."
        )

    except httpx.ReadTimeout:
        return (
            "Ollama timed out while generating "
            "the explanation. Try again."
        )

    except (ResponseError, httpx.RequestError) as error:
        return f"Ollama investigation failed: {error}"
