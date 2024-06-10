const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const ioClient = require('socket.io-client');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Connect to the Python server
const pythonSocket = ioClient.connect('http://localhost:5000');

pythonSocket.on('connect', () => {
  console.log('Connected to Python server');
});

pythonSocket.on('response', (response) => {
  console.log('Received response from Python server:', response);

  if (response.originalSocketId) {
    io.to(response.originalSocketId).emit('response', response.message);
  }
});

io.on('connection', (socket) => {
  console.log('Client connected');

  socket.on('message', (message) => {
    console.log('Received message from client:', message);

    // Forward the message to the Python server
    pythonSocket.emit('message', { originalSocketId: socket.id, message: message });

    pythonSocket.once('response', (response) => {
      console.log('Sending response to client:', response);
      socket.emit('response', response);
    });
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

server.listen(4010, () => {
  console.log('Server is listening on port 4010');
});
