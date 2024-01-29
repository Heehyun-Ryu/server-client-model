import socket
import time
import threading
import os

def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print("Error: Failed to create directory", e)

def receive_file(client):
    init = client.recv(1024)
    init = init.decode('utf-8')
    print("init:", init, type(init))

    room_num, file_path = init.split()

    create_directory(f"TCP_Server/{room_num}")

    file_path = f"TCP_Server/{room_num}/{file_path.split('/')[1]}"
    print(room_num, file_path)

    start = time.time()

    with open(file_path, "wb") as file:
        # conn, addr = server_socket.accept()
        # print(f"Connected by: {addr}")

        while True:
            recv_data_len = 0
            recv_data = client.recv(1024*1024)

            if not recv_data:
                break

            file.write(recv_data)
            recv_data_len += len(recv_data)

            print(f"received data: {recv_data_len}")
    client.close()
    end = time.time()

    print(f"receiving file complete: {end - start} sec")


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.0.44", 8080))
    server_socket.listen(1)
    print("Server started")

    while True:
        client, addr = server_socket.accept()
        print(f"Connected by: {addr}")
        # now = datetime.datetime.now()
        # nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S')

        thread = threading.Thread(target=receive_file, args=(client,))
        thread.start()