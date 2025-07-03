"""ollama_agent.py — local‑only client
------------------------------------------------
Tiny helper for talking to a **locally running** Ollama instance from a
Streamlit app.

•   **No remote URLs** — always targets `http://localhost:11434`.
•   Supports both blocking and streaming generation.
•   Designed for single‑user, offline workflows.
"""

from __future__ import annotations

from typing import Generator, Union

import json
import requests
import streamlit as st

__all__ = ["ask_ollama", "OllamaClient"]

# ---------------------------------------------------------------------------
# Constants (local‑only)
# ---------------------------------------------------------------------------

LOCAL_OLLAMA_URL = "http://localhost:11434"
GENERATE_ENDPOINT = f"{LOCAL_OLLAMA_URL}/api/generate"


# ---------------------------------------------------------------------------
# Low‑level synchronous client
# ---------------------------------------------------------------------------

class OllamaClient:
    """Simple wrapper around the local Ollama HTTP API."""

    def __init__(self, timeout: int = 160) -> None:  # noqa: D401  (simple description)
        self.timeout = timeout

    # -------------------- internal helpers --------------------
    def _post(self, payload: dict, stream: bool) -> requests.Response:
        """Send POST to Ollama with common settings."""
        return requests.post(
            GENERATE_ENDPOINT,
            json=payload,
            timeout=self.timeout,
            stream=stream,
        )

    # -------------------- public API --------------------
    def generate(
        self,
        prompt: str,
        model: str = "mistral",
        stream: bool = False,
        **params,
    ) -> Union[str, Generator[str, None, None]]:
        """Return full response or stream chunks from Ollama."""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **params,
        }
        print("📤 Prompt sent to Ollama:\n", prompt)

        if stream:
            try:
                resp = self._post(payload, stream=True)
                resp.raise_for_status()
                for raw in resp.iter_lines():
                    if not raw:
                        continue
                    try:
                        message = json.loads(raw.decode("utf-8"))
                    except json.JSONDecodeError:
                        continue

                    text_piece = message.get("response", "")
                    if text_piece:
                        #print("🧠 DeepSeek:", text_piece, flush=True)  # 👈 👈 👈 log LLM thinking
                        yield text_piece
                    if message.get("done"):
                        break
            except requests.RequestException as exc:
                raise RuntimeError(f"Streaming failed: {exc}") from exc

        else:
            try:
                resp = self._post(payload, stream=False)
                resp.raise_for_status()
                return resp.json().get("response", "").strip()
            except requests.RequestException as exc:
                raise RuntimeError(f"Request failed: {exc}") from exc


# ---------------------------------------------------------------------------
# Streamlit helper
# ---------------------------------------------------------------------------

def ask_ollama(
    prompt: str,
    model: str = "mistral",
    stream: bool = False,
    **params,
) -> str:
    """High‑level helper that plugs nicely into Streamlit UIs."""

    client = OllamaClient()
    answer: str = ""

    try:
        if stream:
            placeholder = st.empty()
            for piece in client.generate(prompt, model=model, stream=True, **params):
                answer += piece
                # Use markdown to support formatted answers
                placeholder.markdown(answer)
        else:
            with st.spinner("Generating …"):
                answer = client.generate(prompt, model=model, stream=False, **params)  # type: ignore[arg-type]
            st.markdown(answer)
    except RuntimeError as err:
        st.error(str(err))

    return answer
