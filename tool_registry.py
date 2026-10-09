from tools.weather import weather
from tools.geocoder import geocoder
from tools.memory import save, search_data
from tools.search import search
from tools.retrieve_documents import retrieve_documents
from tools.document_generator import generate_document

tool_registry = [
    weather,
    geocoder,
    save, search_data,
    search,
    retrieve_documents,
    generate_document
]