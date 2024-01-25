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

# async def receive_video(websockets):
#     file = open('info.json', 'r')
#
#     print("connected!")
#     print("websockets: ", websockets)
#     print(websockets.remote_address)
#
#     client_id = id(websockets)
#     clients[client_id] = websockets
#
#     print("pid:", os.getpid())
#
#     place = await websockets.recv()
#
#     print("client connected:", client_id)
#     print("place:", place)
#
#     js = json.load(file)
#     file.seek(0)
#
#     video_time = int(js['video_time'])
#
#     create_directory(place)
#
#     start_time = datetime.datetime.now()
#     filename = start_time.strftime('%Y-%m-%d %H_%M_%S')
#
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     video = cv2.VideoWriter(f"{place}/{place}_{filename}.avi", fourcc, 30, (640, 480))
#
#     event_collect = False
#
#     try:
#         while True:
#             now = datetime.datetime.now()
#             nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
#             nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S')
#
#             data = await websockets.recv()
#
#             try:
#                 js = json.load(file)
#                 file.seek(0)
#
#             except json.decoder.JSONDecodeError:
#                 print("JSON Error")
#                 js = {}
#
#             if data == "None":
#                 print("None data")
#
#             else:
#                 if js.get('event') == '1' and not event_collect:
#                     await websockets.send("event!!!")
#                     event_collect = True
#
#                 frame = np.frombuffer(data, dtype=np.uint8)
#                 frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
#
#                 frame = Image.fromarray(frame)
#                 draw = ImageDraw.Draw(frame)
#                 draw.text(xy=(10, 5), text=nowDatetime, font=font, fill=(0, 0, 0))
#                 frame = np.array(frame)
#
#                 # record video
#                 current_time = datetime.datetime.now()
#                 # if (current_time - start_time).total_seconds() >= video_time * 60:
#                 if (current_time - start_time).total_seconds() >= 10:
#                     video.release()
#                     start_time = datetime.datetime.now()
#                     filename = start_time.strftime('%Y-%m-%d %H_%M_%S')
#                     video = cv2.VideoWriter(f"{place}/{place}_{filename}.avi", fourcc, 30, (640, 480))
#
#                 video.write(frame)
#
#                 cv2.imshow(str(client_id) + str(place), frame)
#
#                 cv2.waitKey(1)
#
#                 if cv2.getWindowProperty(str(client_id) + str(place), cv2.WND_PROP_VISIBLE) < 1:
#                     video.release()
#                     break
#
#     except ConnectionClosedOK as e:
#         print("ConnectionClosedOK - Client shutting down?\n")
#         cv2.destroyWindow(str(client_id) + str(place))
#         print(e)
#         del clients[client_id]


async def receive_video(websockets):
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

    video_time = int(js['video_time'])

    create_directory(place)

    start_time = datetime.datetime.now()
    filename = start_time.strftime('%Y-%m-%d %H_%M_%S')



    event_collect = False

    try:
        while True:
            now = datetime.datetime.now()
            nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
            nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S')

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video = cv2.VideoWriter(f"{place}/{place}_{nowDatetime_path}.avi", fourcc, 30, (640, 480))
            print("start!!!")

            for _ in range(1800):
                data = await websockets.recv()

                try:
                    js = json.load(file)
                    file.seek(0)

                except json.decoder.JSONDecodeError:
                    print("JSON Error")
                    js = {}

                if data == "None":
                    print("None data")

                else:
                    if js.get('event') == '1':
                        await websockets.send("event!!!")

                    frame = np.frombuffer(data, dtype=np.uint8)
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                    now = datetime.datetime.now()
                    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

                    frame = Image.fromarray(frame)
                    draw = ImageDraw.Draw(frame)
                    draw.text(xy=(10, 5), text=nowDatetime, font=font, fill=(0, 0, 0))
                    frame = np.array(frame)

                    video.write(frame)

                    cv2.imshow(str(client_id) + str(place), frame)

                    cv2.waitKey(1)

                    if cv2.getWindowProperty(str(client_id) + str(place), cv2.WND_PROP_VISIBLE) < 1:
                        video.release()
                        break
            video.release()
            print("end!!!")

    except ConnectionClosedOK as e:
        print("ConnectionClosedOK - Client shutting down?\n")
        cv2.destroyWindow(str(client_id) + str(place))
        print(e)
        del clients[client_id]

try:
    start_server = websockets.serve(receive_video, "192.168.0.44", 8000)
    # start_server = websockets.serve(receive_video, "127.0.0.1", 8000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

except KeyboardInterrupt as e:
    print("KeyboardInterrupt - Server shutting down\n")
