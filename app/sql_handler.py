from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.config import LLM_MODEL, OLLAMA_BASE_URL, CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD, CLICKHOUSE_DATABASE
import clickhouse_connect

# Инициализация LLM для SQL
sql_llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
    num_ctx=2048,
    num_threads=8
)

sql_prompt = ChatPromptTemplate.from_messages([
    ("system", "Ты — эксперт по SQL для ClickHouse. Преобразуй вопрос пользователя в SQL-запрос. Отвечай только SQL-запросом, без пояснений. Если вопрос не относится к данным, скажи 'не могу'."),
    ("human", "{question}")
])
sql_chain = sql_prompt | sql_llm

def execute_sql(query: str) -> str:
    """Выполняет SQL-запрос к ClickHouse и возвращает отформатированный результат."""
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            user=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE
        )
        result = client.query(query)
        if result.result_rows:
            header = "\t".join(result.column_names)
            rows = "\n".join(["\t".join(str(r) for r in row) for row in result.result_rows])
            return f"Результаты:\n{header}\n{rows}"
        else:
            return "Запрос выполнен, но результатов нет."
    except Exception as e:
        return f"Ошибка выполнения SQL: {e}"

def get_sql_answer(question: str) -> str:
    """Основная функция для обработки вопроса в SQL-режиме."""
    response = sql_chain.invoke({"question": question})
    sql_query = response.content.strip()
    if "не могу" in sql_query.lower():
        return "Не удалось сгенерировать SQL-запрос по вашему вопросу."
    return execute_sql(sql_query)