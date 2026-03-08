from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from ContentApp.schema.summarize import SummarizeRequest, SummarizeResponse
from ContentApp.prompt.template import SUMMARIZE_PROMPT

async def summarize_text(llm: ChatGoogleGenerativeAI, request: SummarizeRequest) -> SummarizeResponse:
    # 1. Temporarily override temperature if provided
    current_temperature = llm.temperature
    if request.temperature is not None:
        llm.temperature = request.temperature
        
    # 2. Build the LCEL Chain
    chain = SUMMARIZE_PROMPT | llm | StrOutputParser()
    
    # 3. Call the chain
    summary_result = await chain.ainvoke({
        "text": request.text,
        "length": request.length.value
    })
    
    # 4. Restore original temperature
    llm.temperature = current_temperature
    
    # 5. Calculate statistics
    original_len = len(request.text)
    summary_len = len(summary_result)
    compression = summary_len / original_len if original_len > 0 else 0.0
    
    # 6. Return response schema
    return SummarizeResponse(
        summary=summary_result,
        original_length=original_len,
        summary_length=summary_len,
        compression_ratio=round(compression, 3)
    )
