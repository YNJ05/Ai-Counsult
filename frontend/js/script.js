const ws = new WebSocket("ws://127.0.0.1:8000/ws");
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const btn = document.getElementById("send-btn");
let thinkingEl = null;

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "thinking") {
        showThinking(data.msg);
    } 
    else if (data.type === "response") {
        removeThinking();
        addAiMessage(data.content, data.badge, data.mode);
    }
};

function send() {
    const text = input.value.trim();
    if (!text) return;
    
    document.getElementById("welcome")?.remove();
    
    // User Message
    const div = document.createElement("div");
    div.className = "msg user";
    div.textContent = text;
    chatBox.appendChild(div);
    
    ws.send(JSON.stringify({ message: text }));
    input.value = "";
    scrollToBottom();
}

function showThinking(text) {
    removeThinking();
    thinkingEl = document.createElement("div");
    thinkingEl.className = "thinking";
    thinkingEl.textContent = text;
    chatBox.appendChild(thinkingEl);
    scrollToBottom();
}

function removeThinking() {
    if (thinkingEl) thinkingEl.remove();
}

function addAiMessage(markdownText, badgeText, mode) {
    const wrapper = document.createElement("div");
    wrapper.className = "msg ai";
    
    const badge = document.createElement("div");
    badge.className = `badge ${mode === 'SIMPLE' ? 'simple' : 'complex'}`;
    badge.textContent = badgeText;
    
    const content = document.createElement("div");
    // Parse Markdown to HTML
    content.innerHTML = marked.parse(markdownText);
    
    wrapper.appendChild(badge);
    wrapper.appendChild(content);
    chatBox.appendChild(wrapper);
    scrollToBottom();
}

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

btn.onclick = send;
input.onkeydown = (e) => { if (e.key === "Enter") send(); };