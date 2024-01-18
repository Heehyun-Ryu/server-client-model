// npm install socket.io
// npm install express

const express = require('express');
const http = require('http');
const socketio = require('socket.io');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const io = socketio(server);

app.use(express.static('templates'));


const clients = {};

io.of('/client').on('connection', (socket) => {
    clients[socket.id] = true;

    io.of('/client').emit('clientList', Object.keys(clients));

    socket.on('data', (data) => {
        const base64Image = Buffer.from(data, 'binary').toString('base64');
        io.emit('draw', base64Image);
    });

    socket.on('disconnect', () => {
        io.of('/client').emit('clientList', Object.keys(clients));
    });
});

io.on('connection', (socket) => {
    console.log("fuck client in");

    socket.on('data', (data) => {
        const base64Image = Buffer.from(data, 'binary').toString('base64');
        io.emit('draw', base64Image);
    });
});


//app.listen 아닌 것 유의!
server.listen(8080, () => {
    console.log("Start Server");
});