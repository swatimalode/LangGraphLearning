import json
from pathlib import Path

from fastapi import FastAPI, Form, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from rag.chunker import store
from graph.graph import CompiledStateGraph
from tools.document_generator import OUTPUT_DIR


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

    response = result["messages"][-1].content
    download_links = []

    for result_message in result["messages"]:
        if getattr(result_message, "name", None) != "generate_document":
            continue

        tool_result = result_message.content
        if isinstance(tool_result, str):
            try:
                tool_result = json.loads(tool_result)
            except json.JSONDecodeError:
                continue

        if not isinstance(tool_result, dict):
            continue

        filename = tool_result.get("filename")
        if not filename or Path(filename).name != filename:
            continue

        generated_file = OUTPUT_DIR / filename
        if generated_file.is_file():
            download_links.append(f"[Download {filename}](/download/{filename})")

    if download_links:
        response += "\n\n" + "\n".join(download_links)

    return response


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


@app.get("/download/{filename}")
def download_generated_document(filename: str):
    if Path(filename).name != filename:
        raise HTTPException(status_code=404, detail="File not found")

    generated_file = OUTPUT_DIR / filename
    if not generated_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        generated_file,
        filename=filename,
        media_type="application/octet-stream"
    )


app.mount(
    "/",
    StaticFiles(
        directory="static",
        html=True
    ),
    name="static"
)