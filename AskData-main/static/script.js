function straighten(message) {
    let newMessage = ""; // Create a new string
  
    for (let i = 0; i < message.length; i++) {
      let char = message[i]; // Get the current character
  
      // Check for backtick and asterisk
      if (char !== '`' && char !== '*') {
        newMessage += char; 
      }
  
      if (i <= message.length - 3 && 
          message[i].toLowerCase() === 's' &&
          message[i + 1].toLowerCase() === 'q' &&
          message[i + 2].toLowerCase() === 'l') {
        newMessage += "Following SQL code."; 
        i += 2;
      }
    }
  
    return newMessage;
  }
  function prettifyMe(textContent) {
    // Replace '**' with HTML <b><i> tags for bold and italic text
    textContent = textContent.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
  // Replace '*' with HTML <i> tags for boldened special text
    textContent = textContent.replace(/\`\`(.*?)\`\`/g, 
  "<span style='font-weight: bold; font-size: 15px;'>$1</span>");

    // Replace '*' with HTML <i> tags for italic text
    textContent = textContent.replace(/\*\*\*(.*?)\*\*\*/g, '<i>$1</i>');

    // Replace '--' with HTML <i> tags for italic text
    textContent = textContent.replace(/\-(.*?)\-/g, '<br>$1</br>');
    //Replace ``` with boldened special color text
    textContent = textContent.replace(/\`\`\`(.*?)\`\`\`/g, 
        "<span style='font-weight: bold; font-size: 15px; text-color: purple;'>$1</span>");
    // Replace triple backticks ''' with <pre><code> tags for code blocks
    textContent = textContent.replace(/'''(.*?)'''/gs, '<pre><code>$1</code></pre>');

    // Replace triple backticks ``` with <pre><code> tags for code blocks
    textContent = textContent.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');

    // Custom formatting for sections
    textContent = textContent.replace(/(Data Professional Question:)/g, '<span style="color: blue; font-size: 1.2em;">$1</span>');
    textContent = textContent.replace(/(Chatbot Response:)/g, '<span style="color: green; font-size: 1.2em;">$1</span>');
    textContent = textContent.replace(/(Additional Tips:)/g, '<span style="color: red; font-size: 1.2em;">$1</span>');

    // Custom formatting for bullet points
    textContent = textContent.replace(/(\* .+?)/g, '<span style="color: brown; font-size: 1em;">$1</span>');

    return textContent; 

}

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
        var prettyResponse = prettifyMe(aiResponse);
        console.log(aiResponse)
        text.innerHTML = '<span style="color: #089799;">AskData: </span>' + prettyResponse;
        botMessage.appendChild(text);

        chatBox.appendChild(botMessage);

        document.getElementById('user_input').value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}