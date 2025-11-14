from typing import Dict, Any
from langchain_openai import ChatOpenAI

def call_llm(messages, model: str = "gpt-4o-mini", **kwargs) -> str:
    """Call OpenAI chat model using LangChain's ChatOpenAI.

    Args:
        messages: list of role/content dicts or LangChain messages
        model: model name
        **kwargs: temperature, etc.

    Returns:
        response content string
    """
    temperature = kwargs.pop("temperature", 0.2)
    force_json = kwargs.pop("force_json", False)
    model_kwargs = kwargs.pop("model_kwargs", None) or {}
    if force_json:
        # OpenAI JSON mode for more reliable JSON outputs
        model_kwargs["response_format"] = {"type": "json_object"}
    llm = ChatOpenAI(model=model, temperature=temperature, model_kwargs=model_kwargs)
    resp = llm.invoke(messages)
    # ChatOpenAI returns an AIMessage with .content
    return getattr(resp, "content", str(resp))
