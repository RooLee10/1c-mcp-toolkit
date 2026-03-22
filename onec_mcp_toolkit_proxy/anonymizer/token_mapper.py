import threading
import re
from typing import Dict


TOKEN_RE = re.compile(
    r"\[([A-Z]+)-(\d{5})\]",
    re.IGNORECASE,
)  # matches [ORG-00001], [org-00001] etc.


class TokenMapper:
    """Bidirectional mapping real_value ↔ token, thread-safe."""

    def __init__(self):
        self._real_to_token: Dict[str, str] = {}
        self._token_to_real: Dict[str, str] = {}
        self._counters: Dict[str, int] = {}
        self._lock = threading.Lock()

    def tokenize(self, value: str, category: str = "STR") -> str:
        """Stable: same value → same token always."""
        with self._lock:
            if value in self._real_to_token:
                return self._real_to_token[value]
            category = category.upper()
            count = self._counters.get(category, 0) + 1
            self._counters[category] = count
            token = f"[{category}-{count:05d}]"
            self._real_to_token[value] = token
            self._token_to_real[token] = value
            return token

    def detokenize(self, text: str) -> str:
        """Replace all known tokens in text with real values."""
        with self._lock:
            def _replace(m):
                normalized = f"[{m.group(1).upper()}-{m.group(2)}]"
                return self._token_to_real.get(normalized, m.group(0))
            return TOKEN_RE.sub(_replace, text)

    def has_tokens(self, text: str) -> bool:
        with self._lock:
            return bool(TOKEN_RE.search(text))

    def get_stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._counters)

    def get_mappings(self) -> list:
        """Return all mappings as list of {token, real_value, category} dicts."""
        with self._lock:
            result = []
            for real_val, token in self._real_to_token.items():
                m = TOKEN_RE.match(token)
                category = m.group(1).upper() if m else "UNKNOWN"
                result.append({"token": token, "real_value": real_val, "category": category})
            return result

    def clear(self):
        with self._lock:
            self._real_to_token.clear()
            self._token_to_real.clear()
            self._counters.clear()
