//DOM

document.addEventListener("DOMContentLoaded", () => {

    
    const messagesContainer = document.querySelector(".messages");
    const sendButton = document.getElementById("send-button");
    const userInput = document.getElementById("user-input");

    if (!messagesContainer) {
        console.error("No .messages container found in the DOM");
        return;
    }

    if (!sendButton) {
    console.error("No .send button container found in the DOM");
    return;
    }

    if (!userInput) {
    console.error("No .user input container found in the DOM");
    return;
    }




    const appendResponse = (text, who) => {
        const wrapper = document.createElement("div");
        wrapper.className = who;
        const pTag = document.createElement("p");
        wrapper.appendChild(pTag);
        pTag.textContent = text;
        messagesContainer.appendChild(wrapper);
        // keep the newest message visible
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };
    


    // Read input value at the moment of sending (don't capture once at load)
    const userResponse = (text) => {
        const trimmed = String(text || '').trim();
        if (!trimmed) {
            // keep previous behavior of prompting when input is empty
            alert('Please enter a message');
            return;
        }
        appendResponse(trimmed, 'user-message');
    };

    const agentResponse = (text) => {
        // Simulate an agent reply after a short delay.
        const reply = 'Agent reply: ' + String(text || '').trim();
        setTimeout(() => appendResponse(reply, 'agent-message'), 400);
    };

    const send = () => {
        const current = userInput.value;
        const trimmed = current.trim();
        if (!trimmed) {
            alert('Please enter a message');
            return;
        }
        userResponse(trimmed);
        userInput.value = '';
        agentResponse(trimmed);
    };

    sendButton.addEventListener('click', send);

    // Allow pressing Enter to send (single-line input).
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            send();
        }
    });

   
}); //Used AI to fix the code on the bottom involving checking for null responses and onclick buttons. Also used AI to connect appendResponse function to both user and agent responses.