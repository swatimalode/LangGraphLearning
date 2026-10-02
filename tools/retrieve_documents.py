from langchain_core.tools import tool
from rag.retriever import DocumentRetriever


retriever = DocumentRetriever()


@tool
def retrieve_documents(query: str):
    """Search the knowledge base for information relevant to the user's question."""

    results = retriever.search(query)

    return results