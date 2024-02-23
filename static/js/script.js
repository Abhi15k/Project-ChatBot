// Initialize WebSocket connection
const socket = new WebSocket(`ws://${window.location.host}/ws`);

// Function to display messages in the chat container
function displayMessage(message, isUser = false) {
    const chatContainer = document.getElementById('chat-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
    // Scroll to the bottom of the chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Event listener for form submission (uploading PDF)
document.getElementById('pdf-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission
    const formData = new FormData(event.target); // Create FormData object from form data

    try {
        const response = await fetch('/upload-pdf/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to upload PDF');
        }

        const data = await response.json();
        alert(`Uploaded PDF: ${data.filename}`);
    } catch (error) {
        console.error('Error uploading PDF:', error);
        alert('Error uploading PDF. Please try again.');
    }
});



// Event listener for sending messages
async function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim(); // Trim whitespace
    const apiKey = document.getElementById('api-key').value.trim(); // Get API key from input field

    if (!userInput || !apiKey) {
        alert("Please enter your question and API key.");
        return;
    }

    try {

        // Send message through WebSocket
        socket.send(JSON.stringify({ message: userInput, api_key: apiKey }));

        // Display user's question in the chat container
        displayChatMessage("You: " + userInput);
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Error sending message. Please try again.');
    }
}



// Event listener for receiving messages from WebSocket
socket.onmessage = function (event) {
    console.log("Received data:", event.data); // Log received data to console

    // Display the received message content in the chat container with formatting
    const chatContainer = document.getElementById('chat-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('bot-message'); // Add CSS class for styling
    displayChatMessage("Chatty: " + event.data); // Use the received data directly
    chatContainer.appendChild(messageElement);
};

// Function to clear the chat history
function clearChatHistory() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.innerHTML = ''; // Clear all child elements
}

// Function to toggle visibility of the API key input
function toggleApiKeyInput() {
    const apiKeyInput = document.getElementById('api-key');
    apiKeyInput.classList.toggle('hidden');
}

// Function to show/hide the API key input based on checkbox state
function toggleApiKeyVisibility() {
    const apiKeyCheckbox = document.getElementById('show-api-key');
    if (apiKeyCheckbox.checked) {
        toggleApiKeyInput(); // Show API key input
    } else {
        toggleApiKeyInput(); // Hide API key input
    }
}

function displayChatMessage(message) {
    const chatContainer = document.getElementById('chat-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message'); // Add CSS class for styling
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
}