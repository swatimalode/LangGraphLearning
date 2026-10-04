from langchain_openai import ChatOpenAI
from config import MODEL, BASE_URL, API_KEY
from tool_registry import tool_registry
from langgraph.graph import MessagesState


llm = ChatOpenAI(
    model=MODEL,
    base_url=BASE_URL,
    api_key=API_KEY
)

llm_with_tools = llm.bind_tools(tool_registry)


def call_llm(state: MessagesState):
    result = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [result]
    }