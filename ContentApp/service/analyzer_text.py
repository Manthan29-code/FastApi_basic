from langchain_google_genai import ChatGoogleGenerativeAI
from ContentApp.schema.Analyzer import analyzerRequest, analyzerResponse
from ContentApp.prompt.AnalyzerTemolate import SENTIMENT_ANALYSIS_PROMPT


async def analyzer_text(llm: ChatGoogleGenerativeAI, request: analyzerRequest) -> analyzerResponse:

    # 1. Bind Pydantic schema — forces LLM to return structured JSON
    print(request)
    structured_llm = llm.with_structured_output(analyzerResponse)

    # 2. Build the chain (no StrOutputParser needed)
    chain = SENTIMENT_ANALYSIS_PROMPT | structured_llm

    # 3. Call the chain — returns analyzerResponse directly
    result = await chain.ainvoke({
        "text": request.text,
        "detailed": request.detailed
    })
    with open("ContentApp/service/response.txt", "w") as f:
        f.write(result.model_dump_json(indent=2))
    return result


