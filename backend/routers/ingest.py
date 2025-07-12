from fastapi import APIRouter, UploadFile, File
from loguru import logger

router = APIRouter(prefix="/api")

@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    content = await file.read()
    logger.info(f"Ingested file: {file.filename} (size={len(content)} bytes)")
    # Placeholder: process or vectorize content here
    return {"filename": file.filename, "status": "success"}
