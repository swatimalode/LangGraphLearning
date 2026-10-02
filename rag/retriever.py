import chromadb

class DocumentRetriever():

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path='./data/chroma'
        )
        self.collection = self.client.get_or_create_collection(
            name='rag_documents'
        )

    def search(self, query, limit=3):
        return self.collection.query(
            query_images=[query],
            n_results=limit
        )