# from flask import Flask, render_template, Response, url_for, redirect
# from PIL import ImageFont, ImageDraw, Image
# import cv2
# import numpy as np
# from flask_socketio import SocketIO, join_room
# import time
#
# app = Flask(__name__)
# socketio = SocketIO(app)
#
# global is_capture, is_record, start_record
# capture = cv2.VideoCapture(1)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# is_record = False
# is_capture = False
# start_record = False
#
# clients = {}
#
# def gen_frames(client_id):
#     global is_record, start_record, is_capture, video
#     while True:
#         now = datetime.datetime.now()  # 현재시각 받아옴
#         nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')  # 현재시각을 문자열 형태로 저장
#         nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S')
#         ref, frame = capture.read()
#         if not ref:
#             break
#         else:
#             frame = Image.fromarray(frame)
#             frame = np.array(frame)
#             ref, buffer = cv2.imencode('.jpg', frame)
#             frame1 = frame
#             frame = buffer.tobytes()
#             if start_record == True and is_record == False:
#                 is_record = True
#                 start_record = False
#                 video = cv2.VideoWriter("녹화 " + nowDatetime_path + ".avi", fourcc, 15,
#                                         (frame1.shape[1], frame1.shape[0]))
#             elif start_record and is_record == True:
#                 is_record = False
#                 start_record = False
#                 video.release()
#             elif is_capture:
#                 is_capture = False
#                 cv2.imwrite("capture " + nowDatetime_path + ".png", frame1)
#             if is_record == True:
#                 video.write(frame1)
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#
#
# @app.route('/')
# def index():
#     global is_record
#     # client_id = str(int(time.time() * 1000))
#     # join_room(client_id)
#     # return render_template('index.html', is_record=is_record, client_id = client_id)
#     return render_template('index.html', is_record=is_record)
#
#
# @app.route('/video_feed/<client_id>')
# def video_feed(client_id):
#     return Response(gen_frames(client_id), mimetype='multipart/x-mixed-replace; boundary=frame')
#
# @app.route('/shutup/<client>')
# def shit(client):
#     return f"client: {client}"
#
# @socketio.on('connect')
# def handle_connect():
#     client_id = request.sid
#     clients[client_id] = {'is_record': False, 'is_capture': False, 'start_record': False}
#     print(f"Client {client_id} connected")
#
# @socketio.on('disconnect')
# def handle_disconnect():
#     client_id = request.sid
#     del clients[client_id]
#     print(f"Client {client_id} disconnected")
#
# @app.route('/push_record')
# def push_record():
#     global start_record
#     start_record = not start_record
#     return redirect(url_for('index'))
#
#
# @app.route('/push_capture')
# def push_capture():
#     global is_capture
#     is_capture = True
#     return redirect(url_for('index'))
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port="8080")


from flask import Flask, render_template, Response, url_for, redirect
from PIL import ImageFont, ImageDraw, Image
import datetime
import cv2
import numpy as np

app = Flask(__name__)
global is_capture, is_record, start_record
capture = cv2.VideoCapture(1)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

is_record = False
is_capture = False
start_record = False  # 각 변수들은 처음엔 거짓(버튼을 누르지 않음)


def gen_frames():
    global is_record, start_record, is_capture, video
    while True:
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S')
        ref, frame = capture.read()
        if not ref:
            break
        else:
            frame = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame)

            frame = np.array(frame)
            ref, buffer = cv2.imencode('.jpg', frame)
            frame1 = frame
            frame = buffer.tobytes()
            if start_record == True and is_record == False:
                is_record = True
                start_record = False

                video = cv2.VideoWriter("녹화 " + nowDatetime_path + ".avi", fourcc, 15,
                                        (frame1.shape[1], frame1.shape[0]))
            elif start_record and is_record == True:
                is_record = False
                start_record = False
                video.release()
            elif is_capture:
                is_capture = False
                cv2.imwrite("capture " + nowDatetime_path + ".png", frame1)
            if is_record == True:
                video.write(frame1)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 그림파일들을 쌓아두고 호출을 기다림


@app.route('/')
def index():
    global is_record
    return render_template('index.html', is_record=is_record)


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/push_record')
def push_record():
    global start_record
    start_record = not start_record
    return redirect(url_for('index'))


@app.route('/push_capture')
def push_capture():
    global is_capture
    is_capture = True
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")