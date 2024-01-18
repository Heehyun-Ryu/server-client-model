import base64

from flask import Flask, request, render_template
from flask_socketio import emit, SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

connected_clients = {}

@socketio.on('connect')
def connect():
    client_id = request.sid
    connected_clients[client_id] = True
    print(f'Client {client_id} connected')

    NS = '/'+'AAA'
    print("NS:", NS)

    @socketio.on('connect', namespace=NS)
    def pr():
        print("NS connected")

    # @socketio.on('data', namespace=NS)
    # def receive_data(data):
    #     base64_image = base64.b64encode(data).decode('utf-8')
    #     emit('draw', base64_image, broadcast=True)
        socketio.sleep(0)
    # join_room('')

@socketio.on('disconnect')
def disconnect():
    client_id = request.sid
    del connected_clients[client_id]
    print(f'Client {client_id} disconnected')

@socketio.on('data')
def receive_data(data, namespace='/a'):
    print("fuck data /a")
    base64_image = base64.b64encode(data).decode('utf-8')
    emit('draw', base64_image, broadcast=True)
    socketio.sleep(0)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)