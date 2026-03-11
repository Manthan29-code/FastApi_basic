from langchain_google_genai import ChatGoogleGenerativeAI
from ContentApp.schema.keyword import keywordRequest, keywordResponse
from ContentApp.prompt.keywordPrompt import KEYWORD_EXTRACTION_PROMPT


async def extract_keywords(llm: ChatGoogleGenerativeAI, request: keywordRequest) -> keywordResponse:
    print(request)
    # 1. Bind Pydantic schema — forces LLM to return structured JSON
    structured_llm = llm.with_structured_output(keywordResponse)

    # 2. Build the chain (no StrOutputParser needed)
    chain = KEYWORD_EXTRACTION_PROMPT | structured_llm

    # 3. Call the chain — returns keywordResponse directly
    result = await chain.ainvoke({
        "text": request.text,
        "max_keywords": request.max_keywords
    })

    return result