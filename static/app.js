"use strict";

/* =========================
   DOM ELEMENTS
========================= */

const messages = document.getElementById("messages");
const messageInput = document.getElementById("messageInput");
const fileInput = document.getElementById("fileInput");
const selectedFile = document.getElementById("selectedFile");
const fileName = document.getElementById("fileName");
const uploadStatus = document.getElementById("uploadStatus");
const loading = document.getElementById("loading");

let isSending = false;
let selectedFiles = [];

/* =========================
   FILE SELECTION
========================= */

fileInput.addEventListener("change", function () {
    const newFiles = Array.from(fileInput.files);

    for (const file of newFiles) {
        const alreadySelected = selectedFiles.some(
            existingFile =>
                existingFile.name === file.name &&
                existingFile.size === file.size &&
                existingFile.lastModified === file.lastModified
        );

        if (!alreadySelected) {
            selectedFiles.push(file);
        }
    }

    renderSelectedFiles();

    // Allow the same picker to be opened again.
    fileInput.value = "";
});

function renderSelectedFiles() {
    if (selectedFiles.length === 0) {
        fileName.textContent = "";
        selectedFile.classList.add("hidden");
        uploadStatus.textContent = "";
        return;
    }

    fileName.textContent = selectedFiles
        .map(file => file.name)
        .join(", ");

    selectedFile.classList.remove("hidden");
    uploadStatus.textContent =
        `${selectedFiles.length} file(s) selected`;
}

/* =========================
   REMOVE SELECTED FILES
========================= */

function removeFile() {
    selectedFiles = [];
    fileInput.value = "";
    renderSelectedFiles();
}

/* =========================
   ADD CHAT MESSAGE
========================= */

function addMessage(text, type) {
    const messageElement = document.createElement("div");
    messageElement.className = `message ${type}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    if (type === "assistant") {
        bubble.innerHTML = marked.parse(text || "");
    } else {
        bubble.textContent = text;
    }

    messageElement.appendChild(bubble);
    messages.appendChild(messageElement);

    messages.scrollTop = messages.scrollHeight;

    return bubble;
}

/* =========================
   SEND MESSAGE
========================= */

async function sendMessage() {
    if (isSending) {
        return;
    }

    const message = messageInput.value.trim();
    const files = [...selectedFiles];

    if (!message && files.length === 0) {
        return;
    }

    isSending = true;

    // Display the user's message and all attachments.
    let displayMessage = message;

    if (files.length > 0) {
        const attachments = files
            .map(file => `📎 ${file.name}`)
            .join("\n");

        displayMessage = displayMessage
            ? `${displayMessage}\n${attachments}`
            : attachments;
    }

    addMessage(displayMessage, "user");

    messageInput.value = "";
    loading.classList.remove("hidden");
    uploadStatus.textContent = "";

    // Create the multipart request.
    const formData = new FormData();
    formData.append("message", message);

    for (const file of files) {
        formData.append("files", file);
    }

    console.log(
        "Files being sent:",
        formData.getAll("files").map(file => file.name)
    );

    try {
        const response = await fetch("/chat", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorText = await response.text();

            throw new Error(
                errorText || `Request failed: ${response.status}`
            );
        }

        const assistantBubble = addMessage("", "assistant");

        if (response.body) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let fullResponse = "";

            while (true) {
                const { value, done } = await reader.read();

                if (done) {
                    break;
                }

                fullResponse += decoder.decode(value, {
                    stream: true
                });

                assistantBubble.innerHTML = marked.parse(fullResponse);
                messages.scrollTop = messages.scrollHeight;
            }

            fullResponse += decoder.decode();
            assistantBubble.innerHTML = marked.parse(fullResponse);
        } else {
            assistantBubble.textContent = await response.text();
        }

        messages.scrollTop = messages.scrollHeight;

        // Clear files after a successful request.
        removeFile();

    } catch (error) {
        console.error("Chat error:", error);

        addMessage(
            "Sorry, something went wrong while processing your request.",
            "assistant"
        );

        uploadStatus.textContent =
            "Request failed. Your selected files are still available to retry.";

    } finally {
        loading.classList.add("hidden");
        isSending = false;
        messageInput.focus();
    }
}

/* =========================
   ENTER TO SEND
========================= */

messageInput.addEventListener("keydown", function (event) {
    if (
        event.key === "Enter" &&
        !event.shiftKey &&
        !event.isComposing
    ) {
        event.preventDefault();
        sendMessage();
    }
});
