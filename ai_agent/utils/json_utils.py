import json
import re
from typing import Any

CODE_FENCE_RE = re.compile(r"^```[a-zA-Z0-9_\-]*\n|\n```$", re.MULTILINE)


def _strip_code_fences(text: str) -> str:
    # Remove triple backtick fences optionally with language tag
    return CODE_FENCE_RE.sub("", text.strip())


def safe_json_loads(text: str) -> Any:
    """Attempt to parse JSON from LLM output robustly.

    Strategy:
    - Try direct json.loads
    - Strip code fences and try again
    - Extract the largest JSON-like object between first '{' and last '}' (or '[' ']').
    """
    if text is None:
        raise ValueError("Empty response: None")
    s = text.strip()
    if not s:
        raise ValueError("Empty response: blank string")
    # 1) direct
    try:
        return json.loads(s)
    except Exception:
        pass
    # 2) strip code fences
    try:
        stripped = _strip_code_fences(s)
        return json.loads(stripped)
    except Exception:
        pass
    # 3) extract object or array
    first_lc, last_rc = stripped.find("{"), stripped.rfind("}") if 'stripped' in locals() else s.find("{"), s.rfind("}")
    if first_lc != -1 and last_rc != -1 and last_rc > first_lc:
        candidate = (stripped if 'stripped' in locals() else s)[first_lc:last_rc+1]
        try:
            return json.loads(candidate)
        except Exception:
            pass
    # try array
    first_lb, last_rb = (stripped if 'stripped' in locals() else s).find("["), (stripped if 'stripped' in locals() else s).rfind("]")
    if first_lb != -1 and last_rb != -1 and last_rb > first_lb:
        candidate = (stripped if 'stripped' in locals() else s)[first_lb:last_rb+1]
        try:
            return json.loads(candidate)
        except Exception:
            pass
    # Give up with a concise preview
    preview = (s[:200] + "...") if len(s) > 200 else s
    raise ValueError(f"Failed to parse JSON from response. Preview: {preview}")
