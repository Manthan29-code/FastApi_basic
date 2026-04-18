from langchain_chroma import Chroma


def add_documents_to_store(
	*,
	chunks,
	embeddings,
	persist_directory: str,
	collection_name: str,
	document_id: str,
	filename: str,
) -> int:
	if not chunks:
		return 0

	for index, chunk in enumerate(chunks):
		chunk.metadata = {
			**(chunk.metadata or {}),
			"document_id": document_id,
			"filename": filename,
			"chunk_index": index,
		}

	vector_store = Chroma(
		collection_name=collection_name,
		embedding_function=embeddings,
		persist_directory=persist_directory,
	)

	ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
	vector_store.add_documents(documents=chunks, ids=ids)
	return len(chunks)
