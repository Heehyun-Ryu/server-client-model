import websockets
import asyncio
import cv2

async def send_video():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    async with websockets.connect("ws://192.168.0.44:8000") as websocket:
        print("connect!!")
        while True:
            ret, frame = capture.read()
            _, img_encode =  cv2.imencode('.jpg', frame)
            
            try:
                await websocket.send(img_encode.tobytes())
            except websockets.exceptions.ConnectionClosedOK:
                break

            if cv2.waitKey(33) == ord('w'):
                break

        capture.release()

# start_server = websockets.serve(send_video, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(send_video())