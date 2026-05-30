import time
from typing import List
from openai import OpenAI

from src.config import NVIDIA_API_KEY, NVIDIA_BASE_URL, NVIDIA_EMBED_MODEL


def get_embedding_client():
    return OpenAI(
        api_key=NVIDIA_API_KEY,
        base_url=NVIDIA_BASE_URL,
    )


def embed_texts(texts: List[str], model: str = None) -> List[List[float]]:
    """
    Generate embeddings for a list of text strings using NVIDIA NeMo embeddings.
    Retries once on failure.
    """
    if model is None:
        model = NVIDIA_EMBED_MODEL

    client = get_embedding_client()

    for attempt in range(2):
        try:
            response = client.embeddings.create(
                input=texts,
                model=model,
                extra_body={"input_type": "passage", "truncate": "END"},
            )
            embeddings = []
            for i, data in enumerate(response.data):
                if hasattr(data, "embedding") and data.embedding:
                    embeddings.append(data.embedding)
                elif hasattr(response, "data") and i < len(response.data):
                    embeddings.append(response.data[i].embedding)
            if embeddings and len(embeddings) == len(texts):
                return embeddings
            raise ValueError(f"Expected {len(texts)} embeddings, got {len(embeddings)}")
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
                continue
            raise RuntimeError(f"NVIDIA embedding failed after retry: {e}")


def embed_query(text: str, model: str = None) -> List[float]:
    """
    Generate embedding for a single query string.
    """
    if model is None:
        model = NVIDIA_EMBED_MODEL

    client = get_embedding_client()

    for attempt in range(2):
        try:
            response = client.embeddings.create(
                input=[text],
                model=model,
                extra_body={"input_type": "query", "truncate": "END"},
            )
            if response.data and len(response.data) > 0:
                return response.data[0].embedding
            raise ValueError("Empty embedding response")
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
                continue
            raise RuntimeError(f"NVIDIA query embedding failed after retry: {e}")
