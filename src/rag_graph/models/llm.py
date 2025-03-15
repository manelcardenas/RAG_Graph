import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


def get_llm():
    """Initialize LLM based on environment configuration.

    Returns:
        ChatOpenAI or ChatOllama: Configured LLM client

    Raises:
        ValueError: If the specified model type is not supported
    """
    model_type = os.getenv("MODEL_TYPE", "openai").lower()

    if model_type == "openai":
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            temperature=float(os.getenv("MODEL_TEMPERATURE", "0")),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif model_type == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1"),
            temperature=float(os.getenv("MODEL_TEMPERATURE", "0")),
        )
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
