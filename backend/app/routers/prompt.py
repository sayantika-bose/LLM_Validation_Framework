from fastapi import APIRouter, HTTPException
from app.models.prompt import PromptRequest, PromptResponse
from app.services.llm_service import LLMService
import logging

router = APIRouter()
llm_service = LLMService()

@router.post("/ask", response_model=PromptResponse)
async def ask_model(request: PromptRequest):
    logging.info(f"Received /api/ask request with prompt: {request.prompt}")
    try:
        response = await llm_service.get_response(request.prompt)
        logging.info("Successfully got response from LLMService.")
        return {"response": response}
    except Exception as e:
        logging.error(f"Error in /api/ask: {e}")
        raise HTTPException(status_code=500, detail="Model error.")
