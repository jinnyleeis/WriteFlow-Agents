from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any

# 1) 사용자 입력 표준화
class UserTask(BaseModel):
    intent: Literal["qa","summary","article","code","portfolio","case_study"] = "article"
    title: str
    audience: str = "general"
    tone: Literal["neutral","business","technical","friendly","persuasive"] = "technical"
    length: Literal["short","medium","long"] = "medium"
    key_points: List[str] = []
    constraints: List[str] = []
    raw_context: Optional[str] = None

# 2) 초안
class Draft(BaseModel):
    outline: List[str]
    key_messages: List[str]
    risks_or_gaps: List[str]
    body_markdown: str

# 3) 비평가 평가지표(세부)
class CriticScore(BaseModel):
    name: str
    score: float
    reason: str

class CriticReport(BaseModel):
    overall: float
    scores: List[CriticScore]
    must_fix: List[str]
    nice_to_have: List[str]
    hallucination_spans: List[str] = []

# 4) 리라이터 결과
class RewriteOutput(BaseModel):
    improved_outline: List[str]
    improved_body_markdown: str
    change_log: List[str]

# 5) 디자이너: 테마/레이아웃/블록 구조
class ThemeTokens(BaseModel):
    brand: str = "Crimson"
    primary: str = "#B71C1C"
    secondary: str = "#333333"
    accent: str = "#F2F2F2"
    font_heading: str = "Noto Sans KR, sans-serif"
    font_body: str = "Noto Sans KR, sans-serif"
    spacing_scale: List[int] = [4,8,12,16,24]
    radius: int = 16

class LayoutSpec(BaseModel):
    # 잡지 페이지 타입
    template: Literal["cover","toc","feature","two_column","gallery","case_study"] = "feature"
    modules: List[str] = ["hero","lede","pullquote","body","callouts"]
    # 모듈별 블록 정의
    blocks: List[Dict[str, Any]] = []

class DesignerOutput(BaseModel):
    theme: ThemeTokens
    layout: LayoutSpec
    # 본문에서 하이라이트 추출 → 시각 블록에 배치
    pulls: List[str] = []

# 6) 최종 결과(스트림릿 렌더 입력)
class FinalPackage(BaseModel):
    meta: Dict[str, Any]
    user_task: UserTask
    draft: Draft
    critic: CriticReport
    rewrite: RewriteOutput
    design: DesignerOutput
