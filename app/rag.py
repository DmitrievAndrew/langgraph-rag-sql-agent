from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.tools import tool
from app.config import CHROMA_PERSIST_DIR, COLLECTION_NAME, EMBEDDINGS_MODEL
import os

# Инициализация векторного хранилища
embeddings = OllamaEmbeddings(model=EMBEDDINGS_MODEL)
vectorstore = Chroma(
    persist_directory=CHROMA_PERSIST_DIR,
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def load_document(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext in [".docx", ".doc"]:
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Неподдерживаемый формат: {ext}")
    docs = loader.load()
    return text_splitter.split_documents(docs)

def add_documents(file_path: str) -> int:
    chunks = load_document(file_path)
    if chunks:
        vectorstore.add_documents(chunks)
        return len(chunks)
    return 0

@tool
def retrieve_docs(query: str) -> str:
    """Поиск информации в загруженных документах (RAG)."""
    docs = vectorstore.similarity_search(query, k=3)
    return "\n\n".join([d.page_content for d in docs])