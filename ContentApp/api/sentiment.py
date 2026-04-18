from fastapi import APIRouter, Depends
from ContentApp.schema.Analyzer import analyzerRequest, analyzerResponse    
from ContentApp.dependencies import get_llm_client
from ContentApp.service import analyzer_text
from langchain_google_genai import ChatGoogleGenerativeAI

router = APIRouter()

@router.post("/sentiment", response_model=analyzerResponse)
async def sentiment(
    request: analyzerRequest,
    llm: ChatGoogleGenerativeAI = Depends(get_llm_client)
):
    return await analyzer_text.analyzer_text(llm, request)