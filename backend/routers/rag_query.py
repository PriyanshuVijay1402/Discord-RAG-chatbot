from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_engine import get_rag_answer
from loguru import logger

router = APIRouter(prefix="/api")

class QueryRequest(BaseModel):
    user_id: str
    query: str

@router.post("/rag-query")
async def rag_query(payload: QueryRequest):
    logger.info(f"Received query from user {payload.user_id}")
    try:
        answer = get_rag_answer(payload.query)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"RAG failed: {e}")
        raise HTTPException(status_code=500, detail="RAG processing error")
