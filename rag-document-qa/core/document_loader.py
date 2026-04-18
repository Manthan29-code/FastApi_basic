from pathlib import Path

from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def _load_text_file(file_path: str):
	with open(file_path, "r", encoding="utf-8") as handle:
		content = handle.read()
	return [Document(page_content=content, metadata={"source": file_path})]


def _load_pdf_file(file_path: str):
	try:
		from pypdf import PdfReader
	except ImportError as exc:
		raise RuntimeError("PDF support requires the 'pypdf' package") from exc

	reader = PdfReader(file_path)
	documents = []
	for index, page in enumerate(reader.pages):
		text = page.extract_text() or ""
		documents.append(
			Document(
				page_content=text,
				metadata={"source": file_path, "page": index + 1},
			)
		)
	return documents


def load_document(file_path: str):
	ext = Path(file_path).suffix.lower()
	if ext not in SUPPORTED_EXTENSIONS:
		raise ValueError("Unsupported file format. Supported formats: .pdf, .txt, .md")

	if ext == ".pdf":
		return _load_pdf_file(file_path)

	return _load_text_file(file_path)
