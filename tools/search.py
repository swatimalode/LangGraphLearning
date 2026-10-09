from ddgs import DDGS
from ddgs.exceptions import TimeoutException
from langchain_core.tools import tool

@tool
def search(query):
    """ 
        Search the internet for information.
            Use this tool whenever the user asks for:
            - current information
            - recent information
            - latest information
            - upcoming events
            - historical facts that need verification
            - information that may have changed

            After receiving search results:
            1. Read the titles and snippets.
            2. Identify which results directly answer the question.
            3. Prefer authoritative and reputable sources.
            4. Ignore irrelevant results.
            5. If the results are insufficient or contradictory, search again
            using a more specific query.
            6. Never claim something is true if the search results do not
            provide sufficient evidence.
    """
    try:
        results = DDGS().text(
            query,
            max_results=5
        )
    except TimeoutException:
        return {
            "query": query,
            "results": [],
            "error": "Web search timed out. Try again later."
        }

    clean_results = []

    for result in results:
        clean_results.append({
            "title": result.get("title"),
            "url": result.get("href"),
            "snippet": result.get("body")
        })

    return {
        "query": query,
        "results": clean_results
    }