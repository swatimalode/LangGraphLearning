import chromadb


class LongTermMemory:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="long_term_memory"
        )

    def save(self, memory_id, content, metadata=None):
        self.collection.add(
            ids=[memory_id],
            documents=[content],
            metadatas=[metadata or {}]
        )

    def search(self, query, limit=3):
        return self.collection.query(
            query_texts=[query],
            n_results=limit
        )

    def update(self, memory_id, content, metadata=None):
        self.collection.update(
            ids=[memory_id],
            documents=[content],
            metadatas=[metadata or {}]
        )