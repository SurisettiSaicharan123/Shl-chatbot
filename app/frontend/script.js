const API_URL = "/chat";

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

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        console.log(data);

        chatBox.innerHTML += `
            <div class="bot">
                <p>${data.reply}</p>
            </div>
        `;

        if (data.recommendations && data.recommendations.length > 0) {

            let html = "";

            data.recommendations.forEach(item => {

                html += `
                    <div class="card">
                        <h3>${item.name}</h3>
                        <p>${item.test_type}</p>
                        <a href="${item.url}" target="_blank">
                            View Assessment
                        </a>
                    </div>
                `;

            });

            chatBox.innerHTML += html;
        }

        messages.push({
            role: "assistant",
            content: data.reply
        });

        chatBox.scrollTop = chatBox.scrollHeight;

    }
    catch(err){

        console.error(err);

        chatBox.innerHTML += `
            <div class="bot">
                <p style="color:red;">
                    ${err.message}
                </p>
            </div>
        `;
    }
}