import socket, cv2, pickle, struct
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = "192.168.0.44"
print("Host IP:", host_ip)

port = 8080
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at", socket_address)


def recv_video(client_socket):
    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)

            if not packet: break

            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)


        cv2.imshow(f"real-time videio{client_socket}", frame)

        cv2.waitKey(1)

    

while True:
    client_socket, addr = server_socket.accept()
    print("Connect!!!", addr)
    thread = threading.Thread(target=recv_video, args=(client_socket,))
    thread.start()
    print("Total Client:", threading.active_count()-1)