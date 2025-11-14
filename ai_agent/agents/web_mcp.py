
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

def _ensure_openai_api_key(explicit_key: str | None) -> None:
    """Set OPENAI_API_KEY into environment if provided.

    Raises:
        RuntimeError: If the key is still missing after attempting to set.
    """
    if explicit_key and not os.getenv("OPENAI_API_KEY"):
        # Only set if not already present so user-override stays.
        os.environ["OPENAI_API_KEY"] = explicit_key
    raw = os.getenv("OPENAI_API_KEY")
    if not raw or raw.strip() == "":
        raise RuntimeError(
            "OPENAI_API_KEY가 설정되지 않았습니다. .env 파일 또는 셸에서 수동으로 export OPENAI_API_KEY=sk-... 형태로 설정 후 다시 실행하세요."
        )
    # Guard against smart quotes (common copy issue):
    if raw.startswith("“") or raw.endswith("”"):
        raise RuntimeError(
            "OPENAI_API_KEY에 스마트 따옴표(“ ”)가 포함되어 있습니다. 일반 따옴표 없이 OPENAI_API_KEY=sk-... 로 수정하고 키를 재발급/회전하시기 바랍니다."
        )

# 아직 검증 xxx
def web_search_chain(openai_model: str, tavily_api_key: str | None, openai_api_key: str | None = None):
    # Ensure the API key exists before constructing the client for clearer error messaging.
    _ensure_openai_api_key(openai_api_key)
    llm = ChatOpenAI(model=openai_model, temperature=0)
    if tavily_api_key:
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        tool = TavilySearchResults(max_results=5)
        # 실제 호출은 네트워크 키 필요하므로 데모 환경에서는 생략
        prompt = ChatPromptTemplate.from_template(
            "질문: {query}\nTavily를 사용해 핵심 근거를 모으고 요약하라. 한국어."
        )
    else:
        # Tavily 키 없으면 Wikipedia로 대체
        wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="en"))  
        prompt = ChatPromptTemplate.from_template(
            "질문: {query}\n위키 기반의 상식과 당신의 지식을 요약해 답하라. 한국어."
        )
    return prompt | llm | StrOutputParser()
