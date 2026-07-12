import json
import os
import random
import time
import uuid

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import BadRequestError, OpenAI, RateLimitError

load_dotenv()

# MODEL = "openai/gpt-5.4-nano"
MODEL = "google-vertex-marketing/gemini-3-flash-preview"
FALLBACK_MODEL = "openai/gpt-5-mini"

_BASE_METADATA = {
    "env": os.environ.get("ENV", "local"),
    "service": os.environ.get("TFY_SERVICE", "pre_cap_generation"),
    "team": os.environ.get("TFY_TEAM", "literature"),
}


def get_tfy_chat_client(
    model_name: str,
    temperature: float = 1.0,
    reasoning_effort: str | None = None,
) -> ChatOpenAI:
    tfy_metadata = {
        **_BASE_METADATA,
        "request_id": str(uuid.uuid4()),
    }
    headers = {
        "X-TFY-METADATA": json.dumps(tfy_metadata),
        "X-TFY-LOGGING-CONFIG": json.dumps({"enabled": True}),
        "X-TFY-CACHE-CONFIG": json.dumps({"type": "exact-match", "ttl": 259200}),
    }
    kwargs = dict(
        api_key=os.environ["TFY_API_KEY"],
        base_url=os.environ["TFY_BASE_URL"],
        model=model_name,
        temperature=temperature,
        reasoning_effort=reasoning_effort,
        default_headers=headers,
    )
    if model_name.startswith("openai/"):
        kwargs["output_version"] = "responses/v1"
    return ChatOpenAI(**kwargs)


def _gemini_safety_settings() -> dict:
    categories = [
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_DANGEROUS_CONTENT",
    ]
    return {
        "safetySettings": [
            {"category": cat, "threshold": "BLOCK_NONE"} for cat in categories
        ]
    }


def _make_headers(extra_metadata: dict | None = None) -> dict:
    tfy_metadata = {
        **_BASE_METADATA,
        "request_id": str(uuid.uuid4()),
        **(extra_metadata or {}),
    }
    return {
        "X-TFY-METADATA": json.dumps(tfy_metadata),
        "X-TFY-LOGGING-CONFIG": json.dumps({"enabled": True}),
        "X-TFY-CACHE-CONFIG": json.dumps({"type": "exact-match", "ttl": 259200}),
    }


class ContentFilteredError(Exception):
    pass


def _call_model(model: str, messages, extra_metadata: dict | None = None) -> str:
    client = OpenAI(
        api_key=os.environ["TFY_API_KEY"],
        base_url=os.environ["TFY_BASE_URL"],
        default_headers=_make_headers(extra_metadata),
    )
    extra = _gemini_safety_settings() if "gemini" in model else {}
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1.0,
        extra_body=extra,
    )
    if not response.choices:
        raise ContentFilteredError(
            f"{model} returned no choices — content filtered by gateway"
        )
    return response.choices[0].message.content or ""


def complete(messages, retries: int = 5, metadata: dict | None = None) -> str:
    last_exc: Exception = RuntimeError("No attempts made")
    for attempt in range(retries):
        try:
            return _call_model(MODEL, messages, metadata)
        except ContentFilteredError:
            print(
                f"Gemini filtered content, retrying with fallback model {FALLBACK_MODEL}..."
            )
            return _call_model(FALLBACK_MODEL, messages, metadata)
        except BadRequestError:
            raise
        except RateLimitError as e:
            last_exc = e
            wait = 30 * (attempt + 1) + random.uniform(0, 10)
            print(
                f"Rate limit hit (attempt {attempt + 1}/{retries}). Retrying in {wait:.1f}s..."
            )
            time.sleep(wait)
        except Exception as e:
            last_exc = e
            wait = 2**attempt
            print(
                f"LLM call failed (attempt {attempt + 1}/{retries}): {e}. Retrying in {wait}s..."
            )
            time.sleep(wait)
    raise last_exc
