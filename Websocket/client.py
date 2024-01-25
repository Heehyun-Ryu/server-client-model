import websockets
import asyncio
import cv2
from websockets.exceptions import ConnectionClosedError

async def receive_event(websocket):
    try:
        while True:
            response = await websocket.recv()
            print(f"{response}")

    except websockets.exceptions.ConnectionClosedOK as e:
        print("recive_event closed")

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

                _, img_encode = cv2.imencode('.jpg', frame)

                await websocket.send(img_encode.tobytes())

            except KeyboardInterrupt as e:
                print("KeyboardInterrupt  - Client shutting down\n")
                print(e)
                break

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

async def send_data(websocket):
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        while True:
            ret, frame = capture.read()

            _, img_encode = cv2.imencode('.jpg', frame)

            await websocket.send(img_encode.tobytes())

    except websockets.exceptions.ConnectionClosedOK as e:
        print("ConnectionClosedOK - Server")

async def main():
    async with websockets.connect("ws://192.168.0.44:8000", ping_interval=None) as websocket:
        print("connect!!")
        await websocket.send('room1')

        task_send = asyncio.create_task(send_data(websocket))
        task_receive = asyncio.create_task(receive_event(websocket))

        await asyncio.gather(task_send, task_receive)

asyncio.run(main())
# asyncio.get_event_loop().run_until_complete(send_video())