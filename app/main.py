__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.agent import rag_agent
from app.rag import add_documents
from app.config import UPLOAD_FOLDER
from app.models import ChatRequest, ChatResponse, UploadResponse
from app.sql_handler import get_sql_answer
import os
import shutil
from langchain_core.messages import HumanMessage

app = FastAPI(title="LangGraph RAG + SQL Agent")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ---------- Эндпоинты ----------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/rag", response_class=HTMLResponse)
async def rag_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "mode": "rag", "title": "📄 Поиск по документам"})

@app.get("/sql", response_class=HTMLResponse)
async def sql_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "mode": "sql", "title": "🗄️ Запрос к базе данных"})

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if request.mode == "rag":
            result = rag_agent.invoke({"messages": [HumanMessage(content=request.question)]})
            answer = result["messages"][-1].content
        elif request.mode == "sql":
            answer = get_sql_answer(request.question)
        else:
            raise HTTPException(status_code=400, detail="Неизвестный режим")
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_FOLDER / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Не удалось сохранить файл: {str(e)}")
    try:
        chunks_added = add_documents(str(file_path))
        os.remove(file_path)
        return UploadResponse(
            message=f"Документ '{file.filename}' успешно загружен и добавлен в базу знаний.",
            chunks_added=chunks_added
        )
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")