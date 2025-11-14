from .runtime import call_llm
from .schemas import Draft, CriticReport, CriticScore
from aicu.utils.json_utils import safe_json_loads
import json

CRITIC_SYSTEM = """You are a rigorous technical editor and evaluation critic.
Score with explicit rubrics and return STRICT JSON per schema.
Focus on correctness, completeness, structure, tone consistency, and audience fit.
Also detect potential hallucinations or unverifiable claims."""

CRITIC_PROMPT = """
Document (Markdown):
---
{body}
---

Evaluate the document with the following rubrics (0-5):
- accuracy
- completeness
- structure
- clarity
- technical_nuance
- audience_fit
- conciseness

List MUST-FIX issues that block publication, NICE-TO-HAVE improvements, and quote any hallucination spans.

Return JSON only:
{{
  "overall": <float 0-5>,
  "scores": [
    {{"name":"accuracy","score":..,"reason":".."}},
    ...
  ],
  "must_fix":[ "...", ... ],
  "nice_to_have":[ "...", ... ],
  "hallucination_spans":[ "...", ... ]
}}
"""

def run_critic(draft: Draft, model="gpt-4o-mini"):
  msg = [
    {"role":"system","content":CRITIC_SYSTEM},
    {"role":"user","content":CRITIC_PROMPT.format(body=draft.body_markdown)}
  ]
  out = call_llm(msg, model=model, temperature=0.2, force_json=True)
  data = safe_json_loads(out)
  return CriticReport(
        overall=data["overall"],
        scores=[CriticScore(**s) for s in data["scores"]],
        must_fix=data["must_fix"],
        nice_to_have=data["nice_to_have"],
        hallucination_spans=data.get("hallucination_spans",[])
    )
