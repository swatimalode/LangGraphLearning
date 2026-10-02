from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END, MessagesState
from tool_registry import tool_registry
from config import MODEL, BASE_URL, API_KEY

from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI()


class ChatRequest(BaseModel):
    message: str


llm = ChatOpenAI(
    model=MODEL,
    base_url=BASE_URL,
    api_key=API_KEY
)

llm_with_tools = llm.bind_tools(tool_registry)

graph = StateGraph(MessagesState)

def should_continue(state: MessagesState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END

tool_node = ToolNode(tool_registry)

def call_llm(state:MessagesState):
    result = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [result]
    }

graph.add_node("llm", call_llm)
graph.add_node("tools", tool_node)

graph.add_edge(START, "llm")
graph.add_conditional_edges(
    "llm",
    should_continue
)

graph.add_edge("tools", "llm")


CompiledStateGraph = graph.compile()

def chat(message: str, file: UploadFile | None = None):
    print("MESSAGE:", message)

    if file:
        print("FILE:", file.filename)

        response = f"""
            Message received: {message}

            File received: {file.filename if file else "No file"}
        """

        return response
    else:
        result = CompiledStateGraph.invoke({
            "messages": [
                ("user", message)
            ]
        })

        return result["messages"][-1].content


@app.post("/chat")
def chat_endpoint(
    message: str = Form(""),
    file: UploadFile | None = File(None)
):
    return StreamingResponse(
        chat(
            message=message,
            file=file
        ),
        media_type="text/plain"
    )


app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static"
)