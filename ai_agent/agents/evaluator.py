
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def evaluator_chain(model: str):
    llm = ChatOpenAI(model=model, temperature=0.2)
    prompt = ChatPromptTemplate.from_template(
        "주어진 자료를 종합하여 200자 내외 요약, 핵심 인사이트 3개, 신뢰도 점수(0~100)를 JSON으로 출력. 한국어.\n자료:\n{content}"
    )
    return prompt | llm | StrOutputParser()
