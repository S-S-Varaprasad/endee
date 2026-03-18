document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');

    function addMessage(content, isUser) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-message' : 'system-message'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const formattedContent = content.replace(/`(.*?)`/g, '<code>$1</code>');
        contentDiv.innerHTML = formattedContent;
        
        msgDiv.appendChild(contentDiv);
        chatContainer.appendChild(msgDiv);
        
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function addTypingIndicator() {
        const indicatorDiv = document.createElement('div');
        indicatorDiv.className = 'message system-message typing-indicator-wrapper';
        indicatorDiv.id = 'typing-indicator';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'typing-indicator';
        contentDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        indicatorDiv.appendChild(contentDiv);
        chatContainer.appendChild(indicatorDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        return indicatorDiv;
    }

    async function handleSend() {
        const query = inputField.value.trim();
        if (!query) return;

        inputField.value = '';
        inputField.disabled = true;
        sendButton.disabled = true;

        addMessage(query, true);
        const indicator = addTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();
            
            indicator.remove();
            
            if (response.ok) {
                setTimeout(() => {
                    addMessage(data.answer, false);
                }, 100);
            } else {
                addMessage("Oops! Something went wrong: " + (data.error || "Unknown error"), false);
            }
        } catch (error) {
            indicator.remove();
            addMessage("Network error connecting to the AI backend.", false);
        } finally {
            inputField.disabled = false;
            sendButton.disabled = false;
            inputField.focus();
        }
    }

    sendButton.addEventListener('click', handleSend);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
});
