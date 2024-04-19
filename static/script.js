function sendMessage() {
    var userInput = document.getElementById('user_input').value;

    if (userInput.trim() === '') {
        return;
    }

    var chatBox = document.getElementById('chat-box');

    var userMessage = document.createElement('div');
    userMessage.classList.add('message-user');
    var userTimestamp = new Date().toLocaleTimeString();
    userMessage.textContent = `User: ${userInput}`;
    chatBox.appendChild(userMessage);

    // Fetch response from server
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_input=${encodeURIComponent(userInput)}`
    })
    .then(response => response.text())
    .then(aiResponse => {
        var botMessage = document.createElement('div');
        botMessage.classList.add('message-bot');
        var botTimestamp = new Date().toLocaleTimeString();
        botMessage.textContent = `AskData: ${aiResponse}`;
        chatBox.appendChild(botMessage);

        document.getElementById('user-input').value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
