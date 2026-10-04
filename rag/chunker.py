from rag.document_loader import read_document
from rag.retriever import DocumentRetriever
from config import CHUNK_SIZE, OVERLAP_CHUNK_SIZE
import tiktoken
import uuid

retriever = DocumentRetriever()

tokenizer = tiktoken.get_encoding("cl100k_base")


def chunk_text(file, chunk_size=CHUNK_SIZE,overlap=OVERLAP_CHUNK_SIZE):
    text = read_document(file)
    tokens = tokenizer.encode(text)
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        text_chunk = tokenizer.decode(chunk_tokens)
        chunks.append(text_chunk)
        start += chunk_size - overlap
    return chunks

def store(file):
    chunks = chunk_text(file)
    document_id = str(uuid.uuid4())

    for index, chunk in enumerate(chunks):
        retriever.save(
            document_id=f"{document_id}_{index}",
            content=chunk,
            metadata={
                "document_id": document_id,
                "chunk_index": index,
                "filename": file.filename
            }
        )

    return f"Document with Id: {document_id} and File Name: {file.filename} uploaded successfully"
