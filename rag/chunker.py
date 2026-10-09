from rag.document_loader import read_document
from rag.retriever import DocumentRetriever
from config import CHUNK_SIZE, OVERLAP_CHUNK_SIZE
import tiktoken
import uuid
import re

retriever = DocumentRetriever()

tokenizer = tiktoken.get_encoding("cl100k_base")

def split_paragraphs(text):
    results = []

    for paragraph in text.split("\n\n"):
        clean_paagraph = paragraph.strip()
        if clean_paagraph:
            results.append(clean_paagraph)

    return results

def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

def get_overlap_text(chunk_parts, overlap):
    if not chunk_parts or overlap <= 0:
        return "", 0

    text = "\n\n".join(chunk_parts)
    tokens = tokenizer.encode(text)

    overlap_tokens = tokens[-overlap:]
    overlap_text = tokenizer.decode(overlap_tokens)

    return overlap_text, len(overlap_tokens)

def build_chunk(file, chunk_size=CHUNK_SIZE, overlap=OVERLAP_CHUNK_SIZE):
    text = read_document(file)
    chunks = []
    chunk_counter = 0
    paragraph_chunk = []

    p_chunks = split_paragraphs(text)

    for paragraph in p_chunks:
        counter = len(tokenizer.encode(paragraph))

        if counter > chunk_size:
            sentances = split_sentences(paragraph)

            for sentance in sentances:
                sen_counter = len(tokenizer.encode(sentance))
                if chunk_counter + sen_counter <= chunk_size:
                    chunk_counter += sen_counter
                    paragraph_chunk.append(sentance)
                else:
                    if paragraph_chunk:
                        chunks.append("\n\n".join(paragraph_chunk))

                    overlap_text, overlap_count = get_overlap_text(
                        paragraph_chunk, overlap
                    )

                    paragraph_chunk = (
                        [overlap_text, sentance]
                        if overlap_text
                        else [sentance]
                    )

                    chunk_counter = overlap_count + sen_counter

        elif chunk_counter + counter <= chunk_size:
            chunk_counter += counter
            paragraph_chunk.append(paragraph)
        else:
            if paragraph_chunk:
                chunks.append("\n\n".join(paragraph_chunk))

            overlap_text, overlap_count = get_overlap_text(
                paragraph_chunk, overlap
            )

            paragraph_chunk = (
                [overlap_text, paragraph]
                if overlap_text
                else [paragraph]
            )

            chunk_counter = overlap_count + counter
    if paragraph_chunk:
        print("777", paragraph_chunk)
        chunks.append("\n\n".join(paragraph_chunk))

    return chunks

# def chunk_text(file, chunk_size=CHUNK_SIZE,overlap=OVERLAP_CHUNK_SIZE):
#     text = read_document(file)
#     tokens = tokenizer.encode(text)
#     chunks = []
#     start = 0

#     while start < len(tokens):
#         end = start + chunk_size
#         chunk_tokens = tokens[start:end]
#         text_chunk = tokenizer.decode(chunk_tokens)
#         chunks.append(text_chunk)
#         start += chunk_size - overlap
#     return chunks

def store(file):
    chunks = build_chunk(file)
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
