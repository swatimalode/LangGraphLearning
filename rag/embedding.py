from openai import OpenAI
from config import BASE_URL, API_KEY, EMBEDDING_MODEL

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

def create_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
        encoding_format="float"
    )

    return response.data[0].embedding