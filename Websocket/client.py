import websockets
import asyncio
import cv2
import sys
from websockets.exceptions import ConnectionClosedError

async def send_video():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    async with websockets.connect("ws://192.168.0.44:8000", ping_interval=None) as websocket:
        print("connect!!")
        await websocket.send('room1')

        while True:
            try:
                ret, frame = capture.read()

            except KeyboardInterrupt as e:
                print("KeyboardInterrupt  - Client shutting down\n")
                print(e)
                break

            _, img_encode = cv2.imencode('.jpg', frame)

            try:
                await websocket.send(img_encode.tobytes())

            except ConnectionClosedError as e:
                print("ConnectionClosedError - Server Shutting down?\n")
                print(e)
                await websocket.close()
                break

            except websockets.exceptions.ConnectionClosedOK as e:
                print("ConnectionClosedOK - Server Close Window\n")
                print(e)
                await websocket.close()
                break

        capture.release()

asyncio.get_event_loop().run_until_complete(send_video())

