# app_webrtc.py

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('sender.html')

@app.route('/receive_webrtc')
def receive_webrtc():
    return render_template('receiver.html')

@socketio.on('start_streaming')
def handle_start_streaming(stream):
    print('received start streaming', stream)
    stream_id = stream.get('id')

    emit('receive_stream', stream, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
