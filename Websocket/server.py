import websockets
import asyncio
import cv2
import numpy as np
from websockets.exceptions import ConnectionClosedOK

clients = {}

async def receive_video(websockets, path):
    file = open("event.txt", "r")

    print("connected!")
    print("websockets: ", websockets)
    print(websockets.remote_address)

    client_id = id(websockets)
    clients[client_id] = websockets

    place = await websockets.recv()

    print("client connected:", client_id)
    print("place:", place)

    try:
        while True:
            data = await websockets.recv()

            event = file.readline()
            file.seek(0)

            if data == "None":
                print("Fuck!")
            else:
                if event == '1':
                    print("I will receive event")

                frame = np.frombuffer(data, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                cv2.imshow(str(client_id) + str(place), frame)

                cv2.waitKey(1)

                if cv2.getWindowProperty(str(client_id) + str(place), cv2.WND_PROP_VISIBLE) < 1:
                    break

    except ConnectionClosedOK as e:
        print("ConnectionClosedOK - Client shutting down?\n")
        cv2.destroyWindow(str(client_id) + str(place))
        print(e)
        del clients[client_id]


try:
    start_server = websockets.serve(receive_video, "192.168.0.44", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt as e:
    print("KeyboardInterrupt - Server shutting down\n")