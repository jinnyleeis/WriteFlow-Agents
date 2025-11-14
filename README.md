# WriteFlow-Agents
Multi-agent writing assistant for long-form content (articles, reports, newsletters, magazines). Paragraph-level evaluation & selective rewriting, JSON design specs, and preview/export. Extensible to video/image context.


## 프로젝트 요약

**WriteFlow Agents — Draft → Critique → Rewrite → Design**

길고 구조화된 글(기사, 리포트, 뉴스레터, 매거진 등)을 대상으로 초안 생성 → 정량 평가(JSON) → 문단 단위 부분 재작성 → 디자인 스펙 산출을 자동화하는 멀티 에이전트 파이프라인입니다. 

매거진은 데모 템플릿 중 하나일 뿐이며, 블로그/화이트페이퍼/케이스스터디 등으로 쉽게 확장될 예정입니다. 


---

## 💡 프로젝트 개요

### 1. 사용자 페인포인트 & 차별화

* 동일 프롬프트라도 모델/세팅/데이터에 따라 **품질 편차** 발생
* 생성물 전체를 다시 돌리면 **편집 비용** 과다
* 의사결정/심사에 필요한 **평가 근거(지표)** 부족
  **차별화**: 문단 단위 **정량 평가(JSON)** → 임계치 미달 **부분만 재작성**, Designer가 **JSON 스펙**으로 레이아웃을 표준화

### 2. 추후 고도화할 내용

* 평가 단위: **문서 전체 → 문단**
* Rewriter: **미달 구간만 patch**
* Designer: 테마/모듈/블록 스펙(JSON)로 frontend 이식성 강화

---

## 🧭 UX & 시나리오

### 3. 사용자 흐름 예시

1. 사용자가 **Title, Draft Markdown** 입력
2. **Writer** 초안 생성
3. **Critic**이 항목별 **JSON 스코어** 산출
4. **Rewriter**가 **낮은 점수 구간만** 부분 재작성
5. **Designer**가 **레이아웃/테마 스펙(JSON)** 생성
6. **Preview/Export** (초기: Streamlit → 이후 Web 프런트 전환)

---

## 🏗 시스템 구조

### 5. High-Level 아키텍처

* **Orchestrator**: Streamlit/Backend
* **Agents**: Writer, Critic, Rewriter, Designer
* **Evaluator**: Rule/Prompt 기반 루브릭 → JSON
* **Artifacts**: Draft/Design/Scores/Preview (JSON, PNG)
* **Renderer**: Magazine Preview/Export

### 6. 세부 구조 (코드 인용 & 평가 이유) - 추후 개발 진행 예정

문단 단위 선택적 재작성으로 **불필요한 재생성**을 줄여 **품질 변동성**과 **비용**을 동시에 절감합니다. 평가를 JSON으로 고정하면 **재현성/추적성**이 생기고, Rewriter는 **must_fix** 타깃만 수정합니다.

```python
# pipeline pseudo
draft = writer.generate(title, draft_md)
critic = evaluate(draft, rubric)  # JSON scores per section/paragraph

if critic.overall < 4.5:
    draft = rewriter.patch(
        draft,
        targets=critic.must_fix,     # 낮은 점수 원인/구간
        unit="paragraph"             # 문단 단위로 최소 변경
    )

design = designer.spec(draft, theme="Modern Art & AI")  # JSON 레이아웃 스펙
package = {"draft": draft, "critic": critic, "design": design}
```

**평가 JSON 예시** — 루브릭 항목별 점수와 수정 지시가 명시됩니다.

```json
{
  "overall": 4.5,
  "scores": [
    {"name": "accuracy", "score": 5},
    {"name": "completeness", "score": 4},
    {"name": "structure", "score": 5},
    {"name": "clarity", "score": 4},
    {"name": "technical_nuance", "score": 5},
    {"name": "audience_fit", "score": 4},
    {"name": "conciseness", "score": 4}
  ],
  "must_fix": [
    "Clarify technical terms like 'latent space'",
    "Add concrete examples in '근거와 사례'"
  ],
  "nice_to_have": ["Add key takeaways", "Add citations"]
}
```

**Designer 스펙(JSON) 스니펫**

```json
{
  "theme": {"brand": "Modern Art & AI", "accent": "#FF5722"},
  "layout": {
    "template": "feature",
    "modules": ["hero", "lede", "pullquote", "body", "callouts"]
  },
  "pulls": [
    "AI는 ‘대체자’가 아니라 확장자입니다.",
    "비평의 역할은 단죄가 아니라 투명성의 설계입니다."
  ]
}
```

---

## 7. ⚠️ 리스크 & 대응, 🧪 실험 & 평가

**리스크**

* 환각/일관성 저하 → **Critic JSON + 근거스팬** 추가
* 전체 재생성 비용 → **문단 patch 방식**
* 렌더 품질 제한 → **Designer 스펙의 블록/템플릿 확장**

**실험/평가**

* A/B: **전체 재생성 vs 문단 재작성** 비교(비용/점수/가독성)
* 루브릭 **threshold/weight** 민감도 튜닝
* **사용자 편집 → 재평가** 피드백 루프

---

## 8. 추후 계획

* **Vertex AI** 연결 안정화(비디오 URL → 장면/무드 분석 반영)
* **이미지 업로드** → 에이전트가 **레이아웃 위치 자동 배치**
* **프론트 전환**: Streamlit → React/Next 기반 잡지 템플릿
* **평가 고도화**: 문단별 스코어 + 국소적 재생성 강화
* **사용자 채팅 편집**: 특정 구간 지시 → 즉시 재작성

---

## 매거진 결과물 고도화

* 프론트(React/Next)로 전환하여 **타이포/그리드/애니메이션** 품질 향상
* **템플릿/블록 시스템**: hero, lede, pullquote, callouts
* 인쇄용 **PDF Export**, 다국어 폰트 프리셋

---

## context에 반영되는 데이터 고도화

* **Map Video Agent**: 비디오 URL 분석값을 **콘텐츠/무드/디자인**에 반영
* Vertex AI 연결 이슈 해결 후 **자동 맵핑 파이프라인**
* 사용자 이미지 업로드 → **콘텐츠/레이아웃 자동 배치**

---

## 평가 고도화

* 현재: **문서 전체 재생성** 경향 → 변경: **문단 단위 스코어링**
* **threshold 미달 문단만 재작성**하여 **맥락 보존 + 비용 절감**
* 매거진 출력 후 **사용자 편집 & AI 부분 재생성** 플로우 추가

---

## 실제 실행 결과

* 📰 **Magazine Writer — Critic → Rewriter → Designer**
* 입력 화면 & 미리보기
![alt text](magazine_input.png)
![alt text](magazine_Preview_Img.png)

---

## 시작

```bash
# 1) 환경
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) 실행 (초기 Streamlit)
streamlit run app.py

# 3) 입력
# - Title
# - Draft Markdown
# - 옵션: 디자인 테마, 길이 등 
```

---

