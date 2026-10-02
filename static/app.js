const messages = document.getElementById("messages");

const messageInput = document.getElementById("messageInput");

const fileInput = document.getElementById("fileInput");

const selectedFile = document.getElementById("selectedFile");

const fileName = document.getElementById("fileName");

const uploadStatus = document.getElementById("uploadStatus");

const loading = document.getElementById("loading");




/* =========================
FILE SELECTION
========================= */

fileInput.addEventListener("change", function () {

const file = fileInput.files[0];

if (!file) {
    return;
}

fileName.textContent = file.name;

selectedFile.classList.remove("hidden");

uploadStatus.textContent = "File selected";

});




/* =========================
REMOVE FILE
========================= */

function removeFile() {

fileInput.value = "";

fileName.textContent = "";

selectedFile.classList.add("hidden");

uploadStatus.textContent = "";

}




/* =========================
ADD MESSAGE
========================= */

function addMessage(text, type) {

const message = document.createElement("div");

message.className = `message ${type}`;


const bubble = document.createElement("div");

bubble.className = "bubble";


if (type === "assistant") {

    bubble.innerHTML = marked.parse(text);

} else {

    bubble.textContent = text;

}


message.appendChild(bubble);

messages.appendChild(message);


messages.scrollTop = messages.scrollHeight;


return bubble;

}




/* =========================
SEND MESSAGE
========================= */

async function sendMessage() {

const message = messageInput.value.trim();

const file = fileInput.files[0];


/*
    Nothing to send
*/

if (!message && !file) {

    return;

}


/*
    Show user's message
*/

let displayMessage = message;


if (file) {

    if (displayMessage) {

        displayMessage += `\n📎 ${file.name}`;

    } else {

        displayMessage = `📎 ${file.name}`;

    }

}


addMessage(displayMessage, "user");


/*
    Clear text box
*/

messageInput.value = "";


/*
    Show loading
*/

loading.classList.remove("hidden");


/*
    Create multipart request
*/

const formData = new FormData();


formData.append(
    "message",
    message
);


if (file) {

    formData.append(
        "file",
        file
    );

}


try {

    /*
        Send request to FastAPI
    */

    const response = await fetch(
        "/chat",
        {
            method: "POST",
            body: formData
        }
    );


    /*
        Handle error
    */

    if (!response.ok) {

        const errorText =
            await response.text();

        throw new Error(errorText);

    }


    /*
        Create assistant message
    */

    const assistantBubble =
        addMessage(
            "",
            "assistant"
        );


    /*
        Read streaming response
    */

    const reader =
        response.body.getReader();


    const decoder =
        new TextDecoder();


    let fullResponse = "";


    while (true) {

        const {
            value,
            done
        } = await reader.read();


        if (done) {

            break;

        }


        const text =
            decoder.decode(value);


        fullResponse += text;


        /*
            Convert Markdown → HTML
        */

        assistantBubble.innerHTML =
            marked.parse(fullResponse);


        /*
            Keep chat scrolled
        */

        messages.scrollTop =
            messages.scrollHeight;

    }


    /*
        Clear selected file
        after successful request
    */

    removeFile();


} catch (error) {

    console.error(
        "Chat error:",
        error
    );


    addMessage(
        "Sorry, something went wrong.",
        "assistant"
    );


} finally {

    loading.classList.add("hidden");

}

}




/* =========================
ENTER TO SEND
========================= */

messageInput.addEventListener(
"keydown",
function (event) {

    /*
        Enter = send
        Shift + Enter = new line
    */

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}

);