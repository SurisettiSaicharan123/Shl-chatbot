const API_URL = "http://127.0.0.1:8000/chat";

let messages = [];

async function sendMessage() {

    const input = document.getElementById("message");
    const text = input.value.trim();

    if (text === "") return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <div class="user">
            <p>${text}</p>
        </div>
    `;

    messages.push({
        role: "user",
        content: text
    });

    input.value = "";

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: messages
            })
        });

        const data = await response.json();

        chatBox.innerHTML += `
            <div class="bot">
                <p>${data.reply}</p>
            </div>
        `;

        if (data.recommendations.length > 0) {

            let html = "<ul>";

            data.recommendations.forEach(item => {

                html += `
                    <li>
                        <b>${item.name}</b><br>
                        ${item.test_type}<br>
                        <a href="${item.url}" target="_blank">
                            View Assessment
                        </a>
                    </li><br>
                `;

            });

            html += "</ul>";

            chatBox.innerHTML += html;
        }

        messages.push({
            role: "assistant",
            content: data.reply
        });

        chatBox.scrollTop = chatBox.scrollHeight;

    }
    catch(err){

        console.log(err);

    }

}