from langchain_google_genai import ChatGoogleGenerativeAI
from ContentApp.schema.classify import classifyRequest, classifyResponse
from ContentApp.prompt.classifyPrompt import CLASSIFY_TEXT_PROMPT


async def classify_text(llm: ChatGoogleGenerativeAI, request: classifyRequest) -> classifyResponse:
    print(request)
    # 1. Bind Pydantic schema — forces LLM to return structured JSON
    structured_llm = llm.with_structured_output(classifyResponse)

    # 2. Build the chain (no StrOutputParser needed)
    chain = CLASSIFY_TEXT_PROMPT | structured_llm

    # 3. Call the chain — returns classifyResponse directly
    result = await chain.ainvoke({
        "text": request.text,
        "categories": ", ".join(request.categories),
        "multi_label": request.multi_label
    })

    return result
