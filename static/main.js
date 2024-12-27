//Combined everything into one file, tried websocket
window.onload = function() {
    const socket = io.connect();

    const chatBox = document.getElementById("chatBox");
    const messageInput = document.getElementById("messageInput");
    const chatForm = document.getElementById("chatForm");
    
    if (!username) {console.error("No Username??")}else {}
    if (chatForm && messageInput) {
      chatForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
          socket.send(`${username}: ${message}`);
          messageInput.value = "";
        }
      });

      socket.on('message', function(message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message");
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);

        chatBox.scrollTop = chatBox.scrollHeight;
      });
    } else {
      console.error("error");
    }
  }
//made with a lot of copy and pasting from stack overflow