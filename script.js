function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') {
        return;
    }

    var chatBox = document.getElementById('chat-box');
    
    var userMessage = document.createElement('div');
    userMessage.classList.add('message-user');
    var userTimestamp = new Date().toLocaleTimeString();
    userMessage.textContent = `${userInput} (${userTimestamp})`;
    chatBox.appendChild(userMessage);

    var botMessage = document.createElement('div');
    botMessage.classList.add('message-bot');
    var botTimestamp = new Date().toLocaleTimeString();
    botMessage.textContent = `AskData: ${userInput} (${botTimestamp})`;
    chatBox.appendChild(botMessage);

    document.getElementById('user-input').value = '';
    chatBox.scrollTop = chatBox.scrollHeight;
}