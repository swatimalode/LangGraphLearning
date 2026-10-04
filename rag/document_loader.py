from pypdf import PdfReader
from docx import Document


def read_txt(file) -> str:
    content = file.file.read()
    return content.decode("utf-8")


def read_pdf(file) -> str:
    reader = PdfReader(file.file)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def read_docx(file) -> str:
    document = Document(file.file)

    paragraphs = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def read_document(file) -> str:
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        return read_txt(file)

    if filename.endswith(".pdf"):
        return read_pdf(file)

    if filename.endswith(".docx"):
        return read_docx(file)

    raise ValueError(f"Unsupported file type: {filename}")