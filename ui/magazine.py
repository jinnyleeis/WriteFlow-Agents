import streamlit as st
from aicu.agents.schemas import DesignerOutput
from .theme_tokens import tokens_to_css
from typing import Dict

def render_magazine(design: DesignerOutput, title: str, author: str, md: str):
    st.markdown(tokens_to_css(design.theme), unsafe_allow_html=True)
    st.markdown('<div class="mag-container">', unsafe_allow_html=True)

    # Cover / Feature header (잡지 레퍼런스 스타일)
    if design.layout.template in ("cover","feature","case_study"):
        cols = st.columns([1.2, 2])
        with cols[0]:
            st.markdown('<div class="masthead">MAGAZINE</div>', unsafe_allow_html=True)
            st.markdown('<div class="accent-rule"></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mag-h1">{title}</div>', unsafe_allow_html=True)
            if design.pulls:
                st.markdown(f'<div class="lede">{design.pulls[0]}</div>', unsafe_allow_html=True)
        with cols[1]:
            # 이미지 힌트만 제공하므로, 업로더/플레이스홀더
            st.markdown('<div class="circle-mask">', unsafe_allow_html=True)
            #st.image("https://picsum.photos/400/400", caption="Hero", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Pullquote
    for b in design.layout.blocks:
        if b.get("type") == "pullquote":
            st.markdown(f'<div class="pullquote">“{b.get("text","") }”</div>', unsafe_allow_html=True)
            break

    # Two-column body
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(md, unsafe_allow_html=False)
    with c2:
        # callouts/statcards
        for b in design.layout.blocks:
            if b.get("type") == "callouts":
                with st.container(border=True):
                    st.markdown("**Key Callouts**")
                    items = b.get("items",[])
                    for it in items:
                        st.markdown(f"- **{it.get('label','')}**: {it.get('value','')}")
        # extra pulls
        for p in design.pulls[1:3]:
            st.markdown(f'<div class="pullquote">{p}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
