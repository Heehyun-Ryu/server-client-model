import websockets
import asyncio
import cv2
import numpy as np
from websockets.exceptions import ConnectionClosedOK
import os
import psutil
import json
from PIL import Image, ImageDraw, ImageFont
import datetime
import schedule

clients = {}
font = ImageFont.truetype("arial.ttf", 20)

def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print("Error: Failed to create directory")

def memory_usage():
    p = psutil.Process()
    rss = p.memory_info().rss / 2 ** 20
    print(f"memory usage: {rss: 10.5f} MB")
    # [{message}]

async def receive_video(websockets):
    def control_record():
        nonlocal record, start
        record = False
        start = True

    start = True
    record = False

    file = open('info.json', 'r')

    print("connected!")
    print("websockets: ", websockets)
    print(websockets.remote_address)

    client_id = id(websockets)
    clients[client_id] = websockets

    print("pid:", os.getpid())

    place = await websockets.recv()

    print("client connected:", client_id)
    print("place:", place)

    js = json.load(file)
    file.seek(0)

    schedule.every(int(js['video_time'])).minute.do(control_record)
    # schedule.every(5).seconds.do(control_record)

    create_directory(place)

    try:
        while True:
            now = datetime.datetime.now()
            nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
            nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S')

            data = await websockets.recv()

            try:
                js = json.load(file)
                file.seek(0)

            except json.decoder.JSONDecodeError:
                print("Tlqkf")
                js = json.load(file)
                file.seek(0)

            if data == "None":
                print("Fuck!")

            else:
                if js['event'] == '1':
                    print("I will receive event")

                frame = np.frombuffer(data, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                frame = Image.fromarray(frame)
                draw = ImageDraw.Draw(frame)
                draw.text(xy=(10,5), text= nowDatetime, font=font, fill=(0,0,0))
                frame = np.array(frame)

                cv2.imshow(str(client_id) + str(place), frame)

                if start:
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    video = cv2.VideoWriter(f"{place}/{place}_{nowDatetime_path}video.avi", fourcc, 30, (640, 480))
                    start = False
                    record = True

                elif record:
                    video.write(frame)

                cv2.waitKey(1)

                if cv2.getWindowProperty(str(client_id) + str(place), cv2.WND_PROP_VISIBLE) < 1:
                    control_record()
                    break

                schedule.run_pending()

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