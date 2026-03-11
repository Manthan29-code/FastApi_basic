from langchain_google_genai import ChatGoogleGenerativeAI
from ContentApp.schema.rewrite import RewriteRequest, RewriteResponse
from ContentApp.prompt.rewrite import REWRITE_PROMPT


async def rewrite_text(llm: ChatGoogleGenerativeAI, request: RewriteRequest) -> RewriteResponse:
    # 1. Bind Pydantic schema — forces LLM to return structured JSON
    structured_llm = llm.with_structured_output(RewriteResponse)

    # 2. Build the chain (no StrOutputParser needed)
    chain = REWRITE_PROMPT | structured_llm

    # 3. Call the chain — returns RewriteResponse directly
    result = await chain.ainvoke({
        "text": request.text,
        "tone": request.tone,
        "preserve_meaning": request.preserve_meaning
    })

    return result