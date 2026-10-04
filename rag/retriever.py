import chromadb

class DocumentRetriever():

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path='./data/chroma'
        )
        self.collection = self.client.get_or_create_collection(
            name='rag_documents'
        )

    def save(self, document_id, content, metadata=None):
        self.collection.upsert(
            ids=[document_id],
            documents=[content],
            metadatas=[metadata or {}]
        )

    def search(self, query, limit=3):
        return self.collection.query(
            query_texts=[query],
            n_results=limit
        )