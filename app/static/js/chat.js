const urlConversationId = window.location.pathname.split('/').pop()

let currentConversationId = '';

function logout() {
    fetch('/auth/logout', {
        method: 'POST'
    }).then(response => {
        if (response.ok) {
            window.location.href = '/auth/login';
        }
    });
}

function selectModel(model) {
    document.getElementById('current-model').innerText = model;
    var links = document.querySelectorAll('.dropdown-content a');

    links.forEach(link => {
        if (link.innerText === model) {
            link.classList.add('selected');
        } else {
            link.classList.remove('selected');
        }
    });
}

function createConversation() {
    fetch('/create_conversation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    .then(response => response.json())
    .then(data => {
        loadConversationList()
        .then(() => {
            selectConversation(data.conversation_id);
        });
    });
}

function selectConversation(conversationId) {
    currentConversationId = conversationId;
    var buttons = document.querySelectorAll('.sidebar button');

    buttons.forEach(btn => {
        btn.classList.remove('selected');
    });

    document.querySelector(`button[onclick="selectConversation('${conversationId}')"]`).classList.add('selected');

    loadConversation(conversationId);
    window.history.pushState({}, '', `/chat/${conversationId}`);
}

function toggleSendButton() {
    var messageInput = document.getElementById('message-input');
    var sendButton = document.getElementById('send-button');

    sendButton.classList.toggle('active', messageInput.value.trim() !== "");
    sendButton.classList.toggle('inactive', messageInput.value.trim() === "");
}

function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var chatContent = document.getElementById('chat-content');

    var userMessage = messageInput.value.trim();
    var selectedModel = document.getElementById('current-model').innerText;

    if (userMessage === "")
        return;

    var userMessageElement = document.createElement('div');

    userMessageElement.className = 'user-message';
    userMessageElement.innerText = userMessage;

    chatContent.appendChild(userMessageElement);

    messageInput.value = "";
    toggleSendButton();

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage, conversation_id: currentConversationId, model: selectedModel })
    })

    .then(response => response.json())
    .then(data => {
        var aiMessageElement = document.createElement('div');

        aiMessageElement.className = 'ai-message';
        aiMessageElement.innerText = data.response;

        chatContent.appendChild(aiMessageElement);
        chatContent.scrollTop = chatContent.scrollHeight;
    });
}

function handleKeyPress(event) {
    if (event.key === 'Enter')
        sendMessage();
}

function getConversations() {
    return fetch('/get_conversations').then(response => response.json());
}

function loadConversation(conversationId) {
    getConversations()

    .then(data => {
        var chatContent = document.getElementById('chat-content');
        chatContent.innerHTML = '';

        var convoObject = data[conversationId] || {};
        var conversation = convoObject.conversation || [];

        conversation.forEach(message => {
            var messageElement = document.createElement('div');
            messageElement.className = message.role === 'user' ? 'user-message' : 'ai-message';

            messageElement.innerText = message.content[0].text;
            chatContent.appendChild(messageElement);
        });

        chatContent.scrollTop = chatContent.scrollHeight;
    });
}

function loadConversationList() {
    return getConversations()

    .then(data => {
        var conversationList = document.getElementById('conversation-list');
        conversationList.innerHTML = '';

        let count = 1;

        for (var conversationId in data) {
            var conversationName = data[conversationId].name || `Conversation ${count++}`;
            var conversationItem = document.createElement('div');

            conversationItem.className = 'conversation-item';

            var button = document.createElement('button');

            button.innerText = conversationName;
            button.setAttribute('onclick', `selectConversation('${conversationId}')`);
            button.className = 'conversation-button';

            conversationItem.appendChild(button);
            conversationList.appendChild(conversationItem);
        }
    });
}

function editConversationName(conversationId) {
    var newName = prompt("Enter new conversation name:");

    if (newName) {
        fetch(`/edit_conversation_name/${conversationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: newName })
        })

        .then(() => loadConversationList())
        .then(() => {
            document.querySelector(`button[onclick="selectConversation('${conversationId}')"]`).classList.add('selected');
        });
    }
}

function handleDropdownDisplay() {
    const currentModel = document.getElementById('current-model').innerText;
    const links = document.querySelectorAll('.dropdown-content a');

    links.forEach(link => {
        link.classList.toggle('selected', link.innerText === currentModel);
    });
}

function deleteConversation(conversationId) {
    if (confirm("Are you sure you want to delete this conversation?")) {
        fetch(`/delete_conversation/${conversationId}`, {
            method: 'DELETE'
        })

        .then(() => {
            loadConversationList()

            .then(() => {
                getConversations()

                .then(data => {
                    let conversationIds = Object.keys(data);

                    if (conversationIds.length > 0)
                        selectConversation(conversationIds[0]);
                    else
                        createConversation();
                });
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    loadConversationList()

    .then(() => {
        getConversations()

        .then(data => {
            let conversationIds = Object.keys(data);

            if (conversationIds.length === 0)
                createConversation();
            else if (urlConversationId && urlConversationId !== 'chat' && conversationIds.includes(urlConversationId))
                selectConversation(urlConversationId);
            else
                selectConversation(conversationIds[0]);
        });
    });

    toggleSendButton();
    handleDropdownDisplay();
    
    document.querySelector('.dropdown').addEventListener('mouseenter', handleDropdownDisplay);
});
