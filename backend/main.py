from fastapi import FastAPI
from routers import rag_query, feedback, ingest
from services.logger import setup_logger
from dotenv import load_dotenv
load_dotenv()

setup_logger()

app = FastAPI(title="Discord RAG Backend")

app.include_router(rag_query.router)
app.include_router(feedback.router)
app.include_router(ingest.router)

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
