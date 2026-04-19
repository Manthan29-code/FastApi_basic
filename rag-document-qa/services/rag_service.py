from __future__ import annotations

from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage

from ..dependencies import get_settings

SOURCE_TEXT_MAX_CHARS = 400


def _truncate_text(text: str, max_chars: int = SOURCE_TEXT_MAX_CHARS) -> str:
	if len(text) <= max_chars:
		return text
	return text[: max_chars - 3].rstrip() + "..."


def _confidence_from_scores(scores: list[float]) -> str:
	if not scores:
		return "low"
	top_score = max(scores)
	if top_score >= 0.8:
		return "high"
	if top_score >= 0.6:
		return "medium"
	return "low"


def _build_vector_store(collection_id: str, embeddings):
	settings = get_settings()
	return Chroma(
		collection_name=collection_id,
		persist_directory=settings.CHROMA_PERSIST_DIR,
		embedding_function=embeddings,
	)


def semantic_search(collection_id: str, query: str, embeddings, top_k: int, score_threshold: float) -> list[dict]:
	vector_store = _build_vector_store(collection_id=collection_id, embeddings=embeddings)
	retrieved = vector_store.similarity_search_with_relevance_scores(query=query, k=top_k)

	results: list[dict] = []
	for doc, score in retrieved:
		if score < score_threshold:
			continue

		metadata = doc.metadata or {}
		results.append(
			{
				"chunk_text": _truncate_text(doc.page_content),
				"source_document": metadata.get("filename") or metadata.get("source_document") or "unknown",
				"page_number": metadata.get("page") or metadata.get("page_number"),
				"relevance_score": float(score),
				"metadata": metadata,
			}
		)

	return results


async def query_documents(
	collection_id: str,
	question: str,
	llm,
	embeddings,
	top_k: int = 4,
	score_threshold: float = 0.5,
	include_sources: bool = True,
) -> dict:
	sources = semantic_search(
		collection_id=collection_id,
		query=question,
		embeddings=embeddings,
		top_k=top_k,
		score_threshold=score_threshold,
	)

	if not sources:
		return {
			"answer": "I couldn't find this information in the uploaded documents.",
			"confidence": "low",
			"sources": [],
			"chunks_retrieved": 0,
			"chunks_used": 0,
		}

	context = "\n\n".join(
		[
			f"Source: {item['source_document']} (score={item['relevance_score']:.3f})\n{item['chunk_text']}"
			for item in sources
		]
	)

	system_prompt = (
		"You are a helpful assistant that answers questions based ONLY on the provided context. "
		"If the context does not contain the answer, reply exactly: "
		"I couldn't find this information in the uploaded documents."
	)
	human_prompt = f"Context:\n{context}\n\nQuestion: {question}"

	response = await llm.ainvoke(
		[
			SystemMessage(content=system_prompt),
			HumanMessage(content=human_prompt),
		]
	)

	answer = getattr(response, "content", str(response))
	scores = [float(item["relevance_score"]) for item in sources]

	return {
		"answer": answer,
		"confidence": _confidence_from_scores(scores),
		"sources": sources if include_sources else [],
		"chunks_retrieved": len(sources),
		"chunks_used": len(sources),
	}
