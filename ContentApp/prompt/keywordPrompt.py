from langchain_core.prompts import ChatPromptTemplate

KEYWORD_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert keyword and entity extraction engine. "
        "Analyze the given text and return ONLY a valid JSON object — no explanation, no markdown, no extra text.\n\n"

        "Always return these fields:\n"
        "- keywords: list of the most important key phrases extracted from the text (up to max_keywords)\n"
        "- entities: list of named entities, each with 'text' (the entity) and 'type' (one of PERSON, ORGANIZATION, LOCATION, DATE, EVENT, PRODUCT, or OTHER)\n"
        "- topics: list of high-level topics or themes the text covers\n\n"

        "Rules:\n"
        "- Return at most {{max_keywords}} keywords, ordered by relevance.\n"
        "- Include ALL named entities found in the text.\n"
        "- Topics should be broad theme labels (e.g. 'automotive', 'politics', 'technology').\n\n"

        "Example output:\n"
        "{{\n"
        '  "keywords": ["Tesla", "Gigafactory", "Texas", "electric vehicles", "manufacturing"],\n'
        '  "entities": [\n'
        '    {{"text": "Elon Musk", "type": "PERSON"}},\n'
        '    {{"text": "Tesla", "type": "ORGANIZATION"}},\n'
        '    {{"text": "Texas", "type": "LOCATION"}}\n'
        "  ],\n"
        '  "topics": ["automotive", "manufacturing", "business expansion"]\n'
        "}}"
    ),
    (
        "human",
        "Text: {text}\n"
        "Max keywords: {max_keywords}"
    )
])