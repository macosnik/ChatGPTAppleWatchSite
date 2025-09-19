function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}
scrollToBottom();

async function sendMessage() {
    const input = document.getElementById('message-input');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';

    const chat = document.getElementById('chat-container');
    const userDiv = document.createElement('div');
    userDiv.className = 'msg-user';
    userDiv.innerHTML = "<p>" + text + "</p>";
    chat.appendChild(userDiv);
    scrollToBottom();

    const res = await fetch('/send', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text})
    });
    const data = await res.json();

    const pcDiv = document.createElement('div');
    pcDiv.className = 'msg-pc';
    pcDiv.innerHTML = data.reply_html;
    chat.appendChild(pcDiv);
    scrollToBottom();
}

document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('message-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
