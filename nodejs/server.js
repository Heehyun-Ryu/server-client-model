// const express = require('express');
// const http = require('http');
// const WebSocket = require('ws');
// const socketIO = require('socket.io');
// const {v4:uuidV4} = require('uuid');

// const app = express();
// const server = http.createServer(app);
// const io = socketIO(server);

// // const video = io.of('video');
// // video.on('connection', (socket) => {
// //     console.log(`video channel connected`);

// //     socket.on('videoData', (data) => {
// //         console.log(`video data recived:`, data)
// //     });
// // });

// app.set('view engine', 'ejs')
// app.use(express.static('pubilc'))

// // app.get('/', (req, res) => {
// //     res.send(`SocketIO Server!!`);
// // });

// app.get('/', (req, res) => {
//     res.redirect(`/${uuidV4()}`)
// })

// app.get('/:room', (res, req) => {
//     res.render('room', {roomId: req.params.room})
// })

// io.on('connection', socket => {
//     socket.on('join-room', (roomId, userId) => {
//         socket.join(roomId)
//         socket.broadcast.emit('user-connected', userId)

//         socket.on(`disconnect`, () => {
//             socket.broadcast.emit('user-disconnected', userId)
//         })
//     })
// })

// server.listen(8000, () => {
//     console.log(`Server port is 8000`);
// })


//Create our express and socket.io servers
const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(server)
const {v4: uuidV4} = require('uuid')

app.set('view engine', 'ejs') // Tell Express we are using EJS
app.use(express.static('public')) // Tell express to pull the client script from the public folder

// If they join the base link, generate a random UUID and send them to a new room with said UUID
app.get('/', (req, res) => {
    res.redirect(`/${uuidV4()}`)
})
// If they join a specific room, then render that room
app.get('/:room', (req, res) => {
    res.render('room', {roomId: req.params.room})
})

// When someone connects to the server
io.on('connection', socket => {
    // When someone attempts to join the room
    socket.on('join-room', (roomId, userId) => {
        socket.join(roomId)  // Join the room
        socket.broadcast.emit('user-connected', userId) // Tell everyone else in the room that we joined
        
        // Communicate the disconnection
        socket.on('disconnect', () => {
            socket.broadcast.emit('user-disconnected', userId)
        })
    })
})

server.listen(8000) // Run the server on the 3000 port