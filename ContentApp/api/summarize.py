from fastapi import APIRouter, Depends
from ContentApp.schema.summarize import SummarizeRequest, SummarizeResponse
from ContentApp.dependencies import get_llm_client
from ContentApp.service import llm_service
from langchain_google_genai import ChatGoogleGenerativeAI

router = APIRouter()

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(
    request: SummarizeRequest,
    llm: ChatGoogleGenerativeAI = Depends(get_llm_client)
):
    return await llm_service.summarize_text(llm, request)
