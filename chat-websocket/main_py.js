const express = require('express');
const http = require('http');
const path = require('path')
const socketIo = require('socket.io');
const ioClient = require('socket.io-client');

const app = express();
const server = http.createServer(app);
const io = require('socket.io')(server)

app.use(express.static(path.join(__dirname, 'public')))

let socketsConnected = new Set()

// Connect to the Python server
const pythonSocket = ioClient.connect('http://localhost:5000');

pythonSocket.on('connect', () => {
  console.log('Connected to Python server');
});

pythonSocket.on('py_bot_response', (response) => {
  console.log('Sending response to client:', response.message);
  if (response.originalSocketId) {
    io.to(response.originalSocketId).emit('update_bot_response', response);
  }
  // io.emit('update_bot_response', response);
});

io.on('connection', (socket) => {
  console.log('Socket ID added : ',socket.id);
  socketsConnected.add(socket.id);
  console.log('Client connected');

  socket.on('client_message', (message) => {
    console.log('Received message from client:', message);

    // Forward the message to the Python server
    pythonSocket.emit('py_client_message', { originalSocketId: socket.id, message: message.message });
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
    socketsConnected.delete(socket.id);
    // io.emit('clients-total', socketsConnected.size);
  });

  socket.on('feedback', (data) => {
    // console.log(data);
    socket.emit('feedback-message', data);
})
});

server.listen(4010, () => {
  console.log('Server is listening on port 4010');
});
