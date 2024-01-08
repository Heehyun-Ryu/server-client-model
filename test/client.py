import socket, cv2, pickle, struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.0.44"
port = 8080

capture = cv2.VideoCapture(1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

client_socket.connect((host_ip, port))
print("connect!")

data = b""
payload_size = struct.calcsize("Q")

while True:
    try:
        ret, frame = capture.read()
        
        a = pickle.dumps(frame)
        video = struct.pack("Q", len(a)) + a
        client_socket.sendall(video)

    except Exception as e:
        print(f"Disconnected!")
        pass



# Host IP: 172.23.80.1
# Listening at ('172.23.80.1', 8000)

#cd .\server-client-model\Python\