import websockets
import asyncio
import cv2
import numpy as np

clients = {}

def show_video(client_id, frame):
    window_name = f"Client {client_id}"
    cv2.imshow(window_name, frame)

    if cv2.waitKey(33) == ord('q'):
        print("disconnect:", client_id)
        cv2.destroyAllWindows()
        return 1

async def receive_video(websockets, path):
    print("connected!")
    print(websockets.remote_address)

    client_id = id(websockets)
    clients[client_id] = websockets

    print("client connected:", client_id)

    try:
        while True:
            data = await websockets.recv()
            frame = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if show_video(client_id, frame) == 1:
                break

            
    except websockets.ConnectionClosedOK:
        print("cat")
        del clients[client_id]



    # while True:
    #     data = await websockets.recv()
    #     frame = np.frombuffer(data, dtype=np.uint8)
    #     frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    #     cv2.imshow("Received Frame", frame)
    #     # cv2.imshow("222", frame)

    #     if cv2.waitKey(33) == ord('q'):
    #         print("disconnect:", websockets.remote_address[1])
    #         cv2.destroyAllWindows()
    #         break


# start_server = websockets.serve(hello, "localhost", 8000)

start_server = websockets.serve(receive_video, "192.168.0.44", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()