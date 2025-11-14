from typing import Dict
from aicu.agents.schemas import ThemeTokens

def tokens_to_css(tokens: ThemeTokens) -> str:
    return f"""
    <style>
      /* Global page background: very light gray */
      body {{
        background: #f5f6f7;
      }}
      :root {{
        --color-primary: {tokens.primary};
        --color-secondary: {tokens.secondary};
        --color-accent: {tokens.accent};
        --radius: {tokens.radius}px;
      }}
      .mag-container {{
        font-family: {tokens.font_body};
        color: var(--color-secondary);
        background: #fafafa; /* magazine main canvas slightly lighter gray */
        padding: 24px;
        border-radius: var(--radius);
      }}
      .mag-h1 {{
        font-family: {tokens.font_heading};
        letter-spacing: -0.02em;
        font-weight: 800;
        font-size: 44px;
        margin: 0 0 8px 0;
        color: var(--color-secondary);
      }}
      .masthead {{
        font-weight: 900; font-size: 52px; letter-spacing: 0.08em;
      }}
      .accent-rule {{
        height: 6px; background: var(--color-primary); width: 88px; border-radius: 3px;
        margin: 12px 0 24px 0;
      }}
      .lede {{
        font-size: 18px; color: #555; line-height: 1.6;
      }}
      .pullquote {{
        font-size: 22px; line-height:1.5; padding: 16px;
        border-left: 6px solid var(--color-primary);
        background: var(--color-accent);
        border-radius: var(--radius);
        margin: 16px 0;
      }}
      .card {{
        border: 1px solid #eee; border-radius: var(--radius); padding: 16px;
        background: white;
      }}
      .circle-mask img {{
        width: 180px; height: 180px; border-radius: 999px; object-fit: cover; 
        border: 6px solid var(--color-accent);
      }}
    </style>
    """
