from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from rag.chunker import store
from graph.graph import CompiledStateGraph


app = FastAPI()


def chat(message: str, files: list[UploadFile] | None = None):

    messages = []

    if files:
        upload_statuses = []

        for file in files: 
            upload_status = store(file) 
            upload_statuses.append(upload_status)

        messages.append(
            (
                "system", 
                "The following documents have been uploaded and stored in the RAG document store:\n" 
                + "\n".join(upload_statuses) + 
                "\nUse the RAG retrieval tools to answer questions about these documents."
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
    files: list[UploadFile] | None = File(None),
    file: UploadFile | None = File(None)
):
    files = list(files or [])
    if file:
        files.append(file)

    return StreamingResponse(
        chat(
            message=message,
            files=files
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