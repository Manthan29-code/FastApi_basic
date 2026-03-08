from fastapi import APIRouter
from .user import userRouter
from .ai_route import aiRouter
from .fileRouter import FileRouter
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

routes  = APIRouter()

# combine routers
routes.include_router(userRouter)
routes.include_router(aiRouter)
routes.include_router(FileRouter)