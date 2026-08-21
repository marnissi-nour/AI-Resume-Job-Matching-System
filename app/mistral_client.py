import json
from typing import Any, Dict, List

from mistralai import Mistral

from app.config import settings

_client = Mistral(api_key=settings.mistral_api_key)


def chat_json(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    """
    Call the Mistral chat endpoint in JSON mode and return a parsed dict.
    Uses response_format=json_object, which Mistral guarantees will
    return valid JSON (as long as the prompt asks for JSON).
    """
    response = _client.chat.complete(
        model=settings.mistral_chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    content = response.choices[0].message.content
    return json.loads(content)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Return one embedding vector per input text, in the same order."""
    response = _client.embeddings.create(
        model=settings.mistral_embed_model,
        inputs=texts,
    )
    # Sort by index defensively in case the API doesn't guarantee order
    ordered = sorted(response.data, key=lambda d: d.index)
    return [item.embedding for item in ordered]
