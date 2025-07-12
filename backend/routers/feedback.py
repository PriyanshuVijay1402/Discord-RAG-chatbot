from fastapi import APIRouter
from pydantic import BaseModel
from loguru import logger

router = APIRouter(prefix="/api")

class FeedbackRequest(BaseModel):
    user_id: str
    query: str
    feedback: str

@router.post("/feedback")
async def feedback(payload: FeedbackRequest):
    logger.info(f"Feedback from {payload.user_id} on query '{payload.query}': {payload.feedback}")
    return {"status": "received"}
