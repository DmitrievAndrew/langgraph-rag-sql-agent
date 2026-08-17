from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from app.config import CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD, CLICKHOUSE_DATABASE

def get_sql_tools(llm):
    db_uri = f"clickhouse+native://{CLICKHOUSE_USER}:{CLICKHOUSE_PASSWORD}@{CLICKHOUSE_HOST}:9000/{CLICKHOUSE_DATABASE}"
    db = SQLDatabase.from_uri(db_uri)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return toolkit.get_tools()