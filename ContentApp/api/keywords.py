from fastapi import APIRouter, Depends
from ContentApp.schema.keyword import keywordRequest, keywordResponse
from ContentApp.dependencies import get_llm_client
from ContentApp.service import keyword
from langchain_google_genai import ChatGoogleGenerativeAI

router = APIRouter()

@router.post("/extract-keywords", response_model=keywordResponse)
async def extract_keywords(
    request: keywordRequest,
    llm: ChatGoogleGenerativeAI = Depends(get_llm_client)
):
    return await keyword.extract_keywords(llm, request)
