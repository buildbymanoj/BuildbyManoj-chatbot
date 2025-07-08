document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const searchIndicator = document.getElementById('search-indicator');
    
    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Send message on Enter (but allow Shift+Enter for new lines)
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    sendButton.addEventListener('click', sendMessage);
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Disable input while waiting for response
        userInput.disabled = true;
        sendButton.disabled = true;
        
        // Call backend API
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator();
            if (data.reply) {
                addMessage(data.reply, 'bot');
            } else {
                addMessage("Sorry, I couldn't process your request. Please try again.", 'bot');
            }
        })
        .catch(error => {
            removeTypingIndicator();
            addMessage("There was an error connecting to the server. Please check your connection.", 'bot');
            console.error('Error:', error);
        })
        .finally(() => {
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        });
    }
    
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message-bubble ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Convert newlines to paragraphs for bot messages
        if (sender === 'bot') {
            content.split('\n\n').forEach(paragraph => {
                if (paragraph.trim()) {
                    const p = document.createElement('p');
                    p.textContent = paragraph;
                    messageContent.appendChild(p);
                }
            });
        } else {
            const p = document.createElement('p');
            p.textContent = content;
            messageContent.appendChild(p);
        }
        
        const messageMeta = document.createElement('div');
        messageMeta.className = 'message-meta';
        
        const timestamp = document.createElement('span');
        timestamp.className = 'timestamp';
        timestamp.textContent = getCurrentTime();
        
        const statusIndicator = document.createElement('span');
        statusIndicator.className = 'status-indicator';
        
        const icon = document.createElement('i');
        icon.className = sender === 'user' ? 'fas fa-check' : 'fas fa-robot';
        statusIndicator.appendChild(icon);
        
        messageMeta.appendChild(timestamp);
        messageMeta.appendChild(statusIndicator);
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageMeta);
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'typing-dot';
            typingDiv.appendChild(dot);
        }
        
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }
    
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    // Focus input on load
    userInput.focus();
});