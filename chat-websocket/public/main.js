// defualt connect to windows.location ( location of index.html )
// paramters - URL of websocket server and options 
const socket = io();

const messageContainer = document.getElementById('message-container');
const nameInput = document.getElementById('name-input');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
// const messageTone = new Audio('/msg-tone.mp3');

messageForm.addEventListener('submit', (e) => {
    e.preventDefault(); // avoid reloading the page
    sendMessage();
})

// just to check the number of clients interacting with the websocket server
// socket.on('clients-total', (data) => {
//     console.log(data);
// })

function sendMessage() {
    // console.log(messageInput.value);

    if (messageInput.value === '') {
        // alert("Message cannot be empty!");   
        return;
    }

    const data = {
        name: nameInput.value,
        message: messageInput.value,
        dateTime: new Date()
    }

    // paramters - event name, data to send
    socket.emit('client_message', data);
    addMessageToUI(true, data);
    messageInput.value = '';
}

socket.on('update_bot_response', (data) => {
    // console.log('main.js : update_bot_response : ', data);
    // messageTone.play();
    addMessageToUI(false, data);
})

// if chatbot message : isOwnMessage = True
// function addMessageToUI(isOwnMessage, data) {
//     clearFeedback();

//     const element = `
//         <li class="${isOwnMessage ? 'message-right' : 'message-left'}">
//             <p class="message">
//                 ${data.message}
//             </p>
//         </li>
//         `;

//     messageContainer.innerHTML += element;
//     scrollToBottom();
// }

function addMessageToUI(isOwnMessage, data) {
    clearFeedback();

    const listItem = document.createElement('li');
    listItem.className = isOwnMessage ? 'message-right' : 'message-left';
    const messageElement = document.createElement('p');
    messageElement.className = 'message';
    listItem.appendChild(messageElement);

    messageContainer.appendChild(listItem);
    scrollToBottom();

    if (isOwnMessage) {
        messageElement.textContent = data.message;
    } else {
        typeWriter(messageElement, data.message);
    }
}

function typeWriter(element, text, index = 0, speed = 20) {
    if (index < text.length) {
        element.innerHTML += text.charAt(index);
        setTimeout(() => typeWriter(element, text, index + 1, speed), speed);
    }
}

function scrollToBottom() {
    messageContainer.scrollTo(0, messageContainer.scrollHeight);
}

messageInput.addEventListener('focus', (e) => {
    socket.emit('feedback', {
        feedback: `${nameInput.value} is typing...`
    })
})

messageInput.addEventListener('keypress', (e) => {
    socket.emit('feedback', {
        feedback: `${nameInput.value} is typing...`
    })
})

messageInput.addEventListener('blur', (e) => {
    socket.emit('feedback', {
        feedback: ``
    })
})

socket.on('feedback-message', (data) => {
    clearFeedback();

    const element = `
        <li class="message-feedback">
            <p class="feedback" id="feedback">
                ${data.feedback}
            </p>
        </li>
        `;

    messageContainer.innerHTML += element;
})

function clearFeedback() {
    document.querySelectorAll('li.message-feedback').forEach(element => {
        element.parentNode.removeChild(element);
    })
}