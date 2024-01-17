import socketio
import cv2

sio = socketio.Client()

@sio.event
def connect():
    print('connected')

@sio.event
def disconnect():
    print('disconnected')

def send_video():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = capture.read()

        _, img_encoded = cv2.imencode('.jpg', frame)
        try:
            sio.emit('data', img_encoded.tobytes())

        except socketio.exceptions.ConnectionError:
            break

    capture.release()



if __name__ == '__main__':
    sio.connect('http://192.168.0.44:8080/a')
    send_video()
