from langchain_core.prompts import ChatPromptTemplate

REWRITE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert text rewriting engine. "
        "Rewrite the given text in the requested tone and return ONLY a valid JSON object — no explanation, no markdown, no extra text.\n\n"

        "Always return these fields:\n"
        "- original: the original input text exactly as provided\n"
        "- rewritten: the rewritten version of the text in the requested tone\n"
        "- tone_applied: the tone that was applied\n"
        "- changes_made: a list of specific changes you made during rewriting\n\n"

        "Tone options:\n"
        "- formal: professional, polished, suitable for business communication\n"
        "- casual: relaxed, conversational, friendly\n"
        "- technical: precise, uses domain-specific terminology\n"
        "- simplified: easy to understand, plain language, shorter sentences\n"
        "- persuasive: compelling, action-oriented, convincing\n\n"

        "Rules:\n"
        "- If preserve_meaning is true, preserve the original meaning as closely as possible. If false, you may alter the meaning to better fit the tone.\n"
        "- Ensure the rewritten text sounds natural in the requested tone.\n"
        "- List ALL notable changes in 'changes_made'.\n\n"

        "Example output:\n"
        "{{\n"
        '  "original": "Hey, so basically the server crashed and we lost some data lol",\n'
        '  "rewritten": "We experienced an unexpected server failure that resulted in partial data loss.",\n'
        '  "tone_applied": "formal",\n'
        '  "changes_made": [\n'
        '    "Removed informal language",\n'
        '    "Restructured for professional tone",\n'
        '    "Clarified the impact statement"\n'
        "  ]\n"
        "}}"
    ),
    (
        "human",
        "Text: {text}\n"
        "Tone: {tone}\n"
        "Preserve meaning: {preserve_meaning}"
    )
])