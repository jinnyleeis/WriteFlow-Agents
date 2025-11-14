from .runtime import call_llm
from .schemas import DesignerOutput, ThemeTokens, LayoutSpec
from aicu.utils.json_utils import safe_json_loads
import json
from string import Template

DESIGNER_SYSTEM = """You are a magazine art director and design system engineer.
Propose a theme and layout for a modern magazine spread, then map content to blocks.
Return STRICT JSON according to schema."""

DESIGNER_PROMPT = """
Context:
- Title: $title
- Audience: $audience
- Tone: $tone
- Length: $length
- Key points: $key_points
- Constraints: $constraints

Content (Markdown):
---
$body
---

Guidelines:
- Follow clean Swiss-style grid. 12-col layout, generous whitespace.
- Choose a bold accent color and muted neutrals; accessible contrast.
- Modules to consider: hero, lede, toc, pullquote, body, sidebar, statcards, gallery.
- Template pick:
  - "cover": full-bleed hero + circular photo frame + big masthead
  - "toc": 2-column list + accent rule
  - "feature": hero + lede + two-column body + pullquote
  - "two_column": simple article
  - "case_study": problem/solution/impact blocks

Return JSON only:
{{
  "theme": {{
    "brand": "...",
    "primary": "#RRGGBB",
    "secondary": "#RRGGBB",
    "accent": "#RRGGBB",
    "font_heading": "Noto Sans KR, sans-serif",
    "font_body": "Noto Sans KR, sans-serif",
    "spacing_scale": [4,8,12,16,24],
    "radius": 16
  }},
  "layout": {{
    "template": "feature",
    "modules": ["hero","lede","pullquote","body","callouts"],
    "blocks": [
  {{"type":"hero","title":"$title","kicker":"Feature","image_hint":"circle-mask"}},
      {{"type":"lede","text":"한 문장 요약"}},
      {{"type":"pullquote","text":"핵심 메시지"}},
      {{"type":"body","md": "본문 일부"}},
      {{"type":"callouts","items":[{{"label":"Impact","value":"..."}},{{"label":"Stack","value":"..."}]}}
    ]
  }},
  "pulls": ["핵심 문장 1","핵심 문장 2"]
}}
"""

def run_designer(title, audience, tone, length, key_points, constraints, body, model="gpt-4o-mini"):
    prompt_text = Template(DESIGNER_PROMPT).safe_substitute(
        title=title,
        audience=audience,
        tone=tone,
        length=length,
        key_points=", ".join(key_points or []),
        constraints=", ".join(constraints or []),
        body=body,
    )
    msg = [
        {"role": "system", "content": DESIGNER_SYSTEM},
        {"role": "user", "content": prompt_text},
    ]
    out = call_llm(msg, model=model, temperature=0.4, force_json=True)
    data = safe_json_loads(out)
    return DesignerOutput(
        theme=ThemeTokens(**data["theme"]),
        layout=LayoutSpec(**data["layout"]),
        pulls=data.get("pulls", []),
    )
