from fastapi import APIRouter, Depends
from ContentApp.schema.rewrite import RewriteRequest, RewriteResponse
from ContentApp.dependencies import get_llm_client
from ContentApp.service import rewrite
from langchain_google_genai import ChatGoogleGenerativeAI

router = APIRouter()

@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite_text(
    request: RewriteRequest,
    llm: ChatGoogleGenerativeAI = Depends(get_llm_client)
):
    return await rewrite.rewrite_text(llm, request)