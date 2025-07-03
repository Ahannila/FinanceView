from __future__ import annotations

"""ollama_agent.py
A lightweight, stream‑friendly client for talking to a local **Ollama** instance
from a Streamlit app.  Works with any model you have pulled (e.g. `mistral`,
`llama3`, `phi3` …) and supports both one‑shot *and* incremental streaming
responses.

Usage (non‑streaming)
---------------------
```python
from ollama_agent import ask_ollama

answer = ask_ollama("Summarise Apple’s latest 10‑Q in 5 bullets")
```

Usage (streaming)
-----------------
```python
answer = ask_ollama(prompt, stream=True)
```
The text will render token‑by‑token in the Streamlit UI.
"""

import os
from typing import Generator, Iterable, Union, Optional

import requests
import streamlit as st

__all__ = ["ask_ollama", "OllamaClient"]

# ---------------------------------------------------------------------------
# Low‑level client
# ---------------------------------------------------------------------------

DEFAULT_OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")


class OllamaClient:
    """Minimal synchronous wrapper around the Ollama HTTP API."""

    def __init__(self, base_url: str = DEFAULT_OLLAMA_URL, timeout: int = 30) -> None:
        self.base_url = base_url
        self.timeout = timeout

    # ----------------------- private helpers -------------------------------
    def _post(self, endpoint: str, payload: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return requests.post(url, json=payload, timeout=self.timeout, stream=payload.get("stream", False))

    # ----------------------- public interface ------------------------------
    def generate(
        self,
        prompt: str,
        model: str = "mistral",
        stream: bool = False,
        **params,
    ) -> Union[str, Generator[str, None, None]]:
        """Hit */api/generate*.

        Parameters
        ----------
        prompt : str
            The user prompt.
        model : str, default "mistral"
            Name of the local Ollama model.
        stream : bool, default ``False``
            If *True*, returns a *generator* that yields chunks as they arrive.
        **params
            Additional parameters supported by the Ollama API (e.g. *temperature*,
            *top_p*).
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **params,
        }

        if stream:
            try:
                resp = self._post("/api/generate", payload)
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:  # ignore keep‑alives
                        yield line.decode("utf-8")
            except requests.RequestException as exc:
                raise RuntimeError(f"🛑 Streaming request failed: {exc}") from exc
        else:
            try:
                resp = self._post("/api/generate", payload)
                resp.raise_for_status()
                return resp.json().get("response", "").strip()
            except requests.RequestException as exc:
                raise RuntimeError(f"🛑 Request failed: {exc}") from exc


# ---------------------------------------------------------------------------
# Streamlit convenience wrapper
# ---------------------------------------------------------------------------

def ask_ollama(
    prompt: str,
    model: str = "mistral",
    stream: bool = False,
    **params,
) -> str:
    """Convenience wrapper for Streamlit apps.

    Displays progress and surfaces errors nicely in the UI.  Always returns the
    *full* answer as a string for downstream use, even when *stream=True*.
    """

    client = OllamaClient()
    answer: str = ""

    try:
        if stream:
            placeholder = st.empty()
            for chunk in client.generate(prompt, model=model, stream=True, **params):
                answer += chunk
                placeholder.markdown(answer)
        else:
            with st.spinner("Generating…"):
                answer = client.generate(prompt, model=model, stream=False, **params)  # type: ignore[arg-type]
                st.markdown(answer)

    except RuntimeError as exc:
        st.error(str(exc))

    return answer
