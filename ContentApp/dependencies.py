from functools import lru_cache
from langchain_google_genai import ChatGoogleGenerativeAI
from ContentApp.config import Settings

@lru_cache()
def get_settings():
    return Settings()

def get_llm_client():
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=settings.DEFAULT_TEMPERATURE
    )
