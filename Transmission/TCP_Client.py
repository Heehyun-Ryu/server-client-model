import socket
import time
import datetime
import cv2
import threading

def send_file(file):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.0.44", 8080))
    print("Connect Server")

    client_socket.sendall(f"room1 {file}".encode('utf-8'))

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
        video = cv2.VideoWriter(f"TCP_Client1/{file_name}.mp4", fourcc, 30, (640, 480))

        for i in range(300):
            ret, frame = capture.read()

            video.write(frame)

            cv2.imshow('frame', frame)

            cv2.waitKey(1)

        thread = threading.Thread(target=send_file, args=(f"TCP_Client1/{file_name}.mp4",))
        thread.start()