from langchain_core.prompts import ChatPromptTemplate

SUMMARIZE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a professional text summarizer. "
               "Produce a {length} summary. "
               "short = 1-2 sentences, medium = 3-5 sentences, detailed = full paragraph. "
               "Return ONLY the summary text, nothing else."),
    ("human", "{text}")
])