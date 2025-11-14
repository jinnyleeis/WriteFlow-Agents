import streamlit as st
import os
from dotenv import load_dotenv
from aicu.agents.schemas import UserTask, Draft, FinalPackage
from aicu.agents.critic import run_critic
from aicu.agents.rewriter import run_rewriter
from aicu.agents.designer import run_designer
from ui.magazine import render_magazine
#from evalhooks.opik_hook import maybe_run_opik_evals

st.set_page_config(page_title="AI Agent — 000 Writer", layout="wide")

# Load environment variables from .env and ensure OPENAI_API_KEY is available
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key:
    # Normalize potential smart quotes or stray quotes
    norm = key.strip().strip('"').strip('“').strip('”')
    if norm != key:
        os.environ["OPENAI_API_KEY"] = norm
else:
    st.warning("OPENAI_API_KEY가 설정되지 않았습니다. .env 또는 환경변수에 키를 추가하세요.")

st.title("🤖 AI Agent — 000 Writer · Critic → Rewriter → Designer")

with st.sidebar:
    st.subheader("AI Agent — 000 Writer")
    st.caption("Design System: Magazine DS (Swiss grid, tokens)")
    st.subheader("Generation Options")
    model = st.selectbox("Model", ["gpt-4o-mini","gpt-4o","openrouter/meta-llama/llama-3.2-3b-instruct"])
    tone = st.selectbox("Tone", ["technical","business","friendly","persuasive","neutral"])
    length = st.selectbox("Length", ["short","medium","long"])
    audience = st.text_input("Audience", "비평가")
    key_points = st.text_area("Key points (comma)", "Process Transparency, Authorship Split, Data Provenance, Latent Space Aesthetics, Critique Framework").split(",")
    constraints = st.text_area("Constraints (comma)", "개인정보(PII) 금지, 출처 0–2개 간단 인용, 마크다운만 사용, H2–H3 헤딩만 사용, 풀쿼트 2개 포함, 콜아웃 리스트 1개 포함, 700–900단어, Streamlit 호환(생 HTML 금지)").split(",")

title = st.text_input("Title", "기계의 눈, 인간의 손: 현대예술과 인공지능의 공진화")
raw = st.text_area("Draft Markdown", height=240, value=
"""## 문제 상황

생성형 인공지능의 급속한 확산으로 예술의 저작권, 창작 주체성, 그리고 비평의 기준이 혼재되고 있습니다. 동일한 프롬프트로도 모델·세팅·데이터셋에 따라 결과가 달라지며, “누가 무엇을 창작했는가”라는 전통적 질문이 충분히 설명력을 갖지 못합니다. 그 결과, 전시·심사·거래의 현장에서 작품의 가치 판단이 지연되거나 일관성을 잃는 문제가 발생합니다.

## 논지

인공지능은 **도구**이자 **공저자**이며 동시에 **미학적 매체**입니다. 따라서 비평의 초점은 결과물의 표면에만 머물지 않고, **과정(Process)·의도(Intent)·맥락(Context)**으로 확장되어야 합니다. 이 세 축을 기준으로 투명성을 확보하면, 인간의 개입이 어디에 놓였는지, 기계가 생성한 우연성이 어떻게 미학으로 승화되었는지 평가할 수 있습니다.

## 근거와 사례

* **과정(Process)**: 프롬프트 엔지니어링, 모델·체크포인트 선택, 시드 고정, 업스케일·리터칭 파이프라인은 ‘붓질’에 준하는 작가적 결정입니다. 동일한 텍스트라도 파라미터의 작은 차이가 조형 언어를 바꿉니다.
* **의도(Intent)**: 데이터셋 큐레이션은 주제·미감·윤리의 압축판입니다. 어떤 이미지를 학습의 재료로 선택·배제했는지가 결과의 정치성을 좌우합니다.
* **맥락(Context)**: 전시는 시스템을 드러내는 무대가 됩니다. 생성 과정, 실패작, 프로세스 로그를 함께 제시할 때 관객은 ‘우연의 설계’를 읽어낼 수 있습니다.

## 반론과 재반박

* **“기계가 만들었으니 예술이 아니다.”**
  예술사에서 새 매체는 반복적으로 ‘비예술’로 의심받았습니다. 사진·비디오·인터넷 아트가 그랬듯, 핵심은 매체의 물성으로 무엇을 발명했는가입니다. AI는 **잠재공간(latent space)**이라는 새로운 조형 영역을 열었습니다.
* **“프롬프트는 단지 지시문이다.”**
  시·각본·악보도 지시문입니다. 작가성은 지시의 정밀도, 반복·변주, 우연의 편집에서 발생합니다.

## 실천 제안(비평가·기관용 체크리스트)

1. **프로세스 라벨**: 모델·버전·시드·핵심 파라미터·후처리 툴을 메타데이터로 공개합니다.
2. **데이터 출처 크레딧**: 학습·참조 데이터의 출처와 사용 범위를 명시하고, 불명확한 경우 표시합니다.
3. **프롬프트 노트**: 초안→수정→최종 프롬프트의 변주 과정을 기록해 의도와 판단을 추적 가능하게 합니다.
4. **공동 저자 표기**: 인간/모델/도구의 역할 분담(기획·생성·편집)을 작품 카드에 명확히 기재합니다.

## 결론

AI는 ‘대체자’가 아니라 **확장자**입니다. 인간의 개입이 설계·해석·윤리로 이동할수록, 예술은 더 깊은 의식과 넓은 감각을 획득합니다. 비평의 역할은 단죄가 아니라 **투명성의 설계**이며, 그 투명성 위에서 우리는 기계의 우연과 인간의 의도를 하나의 미학으로 읽어낼 수 있습니다.
""")

if st.button("Generate Magazine", type="primary"):
    with st.spinner("Running agents..."):
        user_task = UserTask(
            title=title, audience=audience, tone=tone, length=length,
            key_points=[k.strip() for k in key_points if k.strip()],
            constraints=[c.strip() for c in constraints if c.strip()],
            raw_context=raw
        )
        # 초안(여기선 입력을 그대로 초안으로 간주. 필요시 초안 생성 프롬프트 추가)
        draft = Draft(
            outline=["문제 상황","해결 방법","성과"],
            key_messages=user_task.key_points,
            risks_or_gaps=[],
            body_markdown=user_task.raw_context or ""
        )

        critic = run_critic(draft, model=model)
        rewrite = run_rewriter(draft, critic, model=model)
        design = run_designer(
            title=user_task.title, audience=user_task.audience, tone=user_task.tone,
            length=user_task.length, key_points=user_task.key_points,
            constraints=user_task.constraints, body=rewrite.improved_body_markdown,
            model=model
        )

        # 평가 훅 (Opik 있으면 실행)
        #eval_res = maybe_run_opik_evals(rewrite.improved_body_markdown)

        st.success("Agents completed")
        with st.expander("Critic Report (JSON)"):
            st.json(critic.model_dump())

        with st.expander("Rewriter Change Log"):
            st.write(rewrite.change_log)

        with st.expander("Designer Spec (JSON)"):
            st.json(design.model_dump())

        st.divider()
        st.subheader("Magazine Preview")
        render_magazine(design, title=user_task.title, author="Auto", md=rewrite.improved_body_markdown)

        st.divider()
        st.subheader("Final Package (JSON)")
        pack = FinalPackage(
            meta={"model": model},
            user_task=user_task,
            draft=draft,
            critic=critic,
            rewrite=rewrite,
            design=design
        )
        st.json(pack.model_dump())
