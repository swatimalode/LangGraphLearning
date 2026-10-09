import chromadb
from rag.embedding import create_embedding

class DocumentRetriever():

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path='./data/chroma'
        )
        self.collection = self.client.get_or_create_collection(
            name='rag_documents_v2'
        )

    def save(self, document_id, content, metadata=None):
        embeddings = create_embedding(content)
        self.collection.upsert(
            ids=[document_id],
            embeddings=[embeddings],
            documents=[content],
            metadatas=[metadata or {}]
        )

    def search(self, query, limit=3):
        query_embedding = create_embedding(query)
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit
        )