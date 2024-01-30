import os.path
import socket
import time
import datetime
import cv2
import threading
import face_recognition

def send_file(file, type):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.0.44", 8080))
    print("Connect Server")

    client_socket.sendall(f"room1 {file} {type} ".encode('utf-8'))

    start = time.time()

    with open(file, 'rb') as file:
        send_data = 0
        while True:
            data = file.read(1024*1024)

            if not data:
                break

            client_socket.sendall(data)
            send_data += len(data)
            print(f"Sent data: {send_data}bytes")

    print("Complete sending")
    end = time.time()
    print(f"Total time: {end - start} sec")
    client_socket.close()

if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    while True:
        now = datetime.datetime.now()
        file_name = now.strftime('%Y-%m-%d_%H_%M_%S')
        video = cv2.VideoWriter(f"TCP_Client1/{file_name}.avi", fourcc, 30, (640, 480))

        for i in range(300):
            ret, frame = capture.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_frame)

            for top, right, bottom, left in face_locations:
                top *= 4
                right *= 4
                left *= 4
                bottom *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            if face_locations:
                now = datetime.datetime.now()
                image_file_name = now.strftime('%Y-%m-%d_%H_%M_%S')
                if not os.path.exists('TCP_Client1/{image_file_name}.jpg'):
                    cv2.imwrite(f"TCP_Client1/{image_file_name}.jpg", frame)

                thread_img = threading.Thread(target=send_file, args=(f"TCP_Client1/{image_file_name}.jpg", 'image',))
                thread_img.start()

            video.write(frame)

            cv2.imshow('frame', frame)

            cv2.waitKey(1)

        thread = threading.Thread(target=send_file, args=(f"TCP_Client1/{file_name}.avi", 'video',))
        thread.start()