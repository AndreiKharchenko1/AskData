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
        
        var icon = document.createElement('img');
        icon.src = '../static/icon.png'; // Add your icon's URL here
        icon.classList.add('bot-icon');
        botMessage.appendChild(icon);

        var text = document.createElement('span');
        text.innerHTML = '<span style="color: #089799;">AskData: </span><span style="color: #5e3101;">' + aiResponse + '</span>';
        botMessage.appendChild(text);
        
        chatBox.appendChild(botMessage);

        document.getElementById('user_input').value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}