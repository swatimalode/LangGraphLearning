from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from rag.chunker import store
from graph.graph import CompiledStateGraph


app = FastAPI()


def chat(message: str, file: UploadFile | None = None):

    print("MESSAGE:", message)

    messages = []

    if file:

        upload_status = store(file)

        messages.append(
            (
                "system",
                f"{upload_status} "
                "The document is available in the RAG document store."
            )
        )

    messages.append(("user", message))

    result = CompiledStateGraph.invoke(
        {
            "messages": messages
        }
    )

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
    StaticFiles(
        directory="static",
        html=True
    ),
    name="static"
)