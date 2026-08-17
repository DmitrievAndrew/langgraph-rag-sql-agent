from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from app.rag import retrieve_docs
from app.config import LLM_MODEL, OLLAMA_BASE_URL

llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
    num_ctx=2048,
    num_threads=8
)

rag_prompt = (
    "Ты — помощник, который отвечает на вопросы, используя только загруженные документы. "
    "Для поиска информации обязательно вызывай инструмент retrieve_docs. "
    "Если в документах нет ответа, скажи об этом честно."
)

rag_agent = create_react_agent(llm, tools=[retrieve_docs], state_modifier=rag_prompt)