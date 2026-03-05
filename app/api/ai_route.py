from fastapi import APIRouter
aiRouter = APIRouter()
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')


@aiRouter.get("/aiRoutes")
def testAIResponse():

    return {"message": "API AI working 🚀"}

@aiRouter.post("/askAI/")
async def aiResponse(question : str):
    print(question)
    response = await llm.ainvoke(question)
    print(response)
    return {"question": question , "response" : response.content}

