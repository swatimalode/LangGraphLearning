from memory.long_term_memory import LongTermMemory
from langchain_core.tools import tool

memory = LongTermMemory()

@tool
def save(memory_id, content, metadata):
    """Saves the memory of user details. It does save important information about user. Metadata can type of memory, and key point of memory."""

    memory.save(memory_id, content, metadata)

    return "User Detail saved!"

@tool
def search_data(query):
    """Returns the memory of user. If no memory found that it will say It does not know"""

    results = memory.search(query)

    return results