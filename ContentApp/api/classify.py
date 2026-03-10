from fastapi import APIRouter, Depends
from ContentApp.schema.classify import classifyRequest, classifyResponse
from ContentApp.dependencies import get_llm_client
from ContentApp.service import classifyText
from langchain_google_genai import ChatGoogleGenerativeAI

router = APIRouter()

@router.post("/classify", response_model=classifyResponse)
async def classify(
    request: classifyRequest,
    llm: ChatGoogleGenerativeAI = Depends(get_llm_client)
):
    return await classifyText.classify_text(llm, request)
