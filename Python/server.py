import websockets
import asyncio
import cv2
import numpy as np

async def receive_video(websockets, path):
    print("connected!")
    while True:
        data = await websockets.recv()
        frame = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        cv2.imshow("Received Frame", frame)

        if cv2.waitKey(33) == ord('q'):
            cv2.destroyAllWindows()
            break

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello! {name}!"
    await websocket.send(greeting)
    print(f"> {greeting}")

# start_server = websockets.serve(hello, "localhost", 8000)

start_server = websockets.serve(receive_video, "192.168.0.44", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()