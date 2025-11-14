from .runtime import call_llm
from .schemas import Draft, CriticReport, RewriteOutput
from aicu.utils.json_utils import safe_json_loads
import json

REWRITER_SYSTEM = """You are a senior editor. Resolve MUST-FIX first.
Preserve the author's voice but tighten logic and flow. Output STRICT JSON."""

REWRITER_PROMPT = """
Original Markdown:
---
{body}
---

Critic Report (JSON):
{critic_json}

Rewrite rules:
- Fix MUST-FIX points explicitly.
- Keep technical accuracy; if claim uncertain, hedge or cite placeholders.
- Improve headings hierarchy and add signposting.
- Keep conciseness: remove redundancy, tighten sentences.
- Use Korean '습니다체' if the source is Korean; otherwise keep original language.
- Keep code blocks and tables if present.

Return JSON only:
{{
  "improved_outline": ["H1 ...","H2 ...", "..."],
  "improved_body_markdown": "....",
  "change_log": ["what changed and why", "..."]
}}
"""

def run_rewriter(draft: Draft, critic: CriticReport, model="gpt-4o-mini"):
    msg = [
        {"role":"system","content":REWRITER_SYSTEM},
        {"role":"user","content":REWRITER_PROMPT.format(
            body=draft.body_markdown,
            critic_json=critic.model_dump_json()
        )}
    ]
    out = call_llm(msg, model=model, temperature=0.3, force_json=True)
    data = safe_json_loads(out)
    return RewriteOutput(**data)
