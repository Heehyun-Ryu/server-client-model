import cv2
import datetime

fourcc = cv2.VideoWriter_fourcc(*'XVID')

start = True
record = False
video = None

def save_video(place, frame):
    global record, start, video
    if start:
        print("start")
        now = datetime.datetime.now()
        nowDatetime_path = now.strftime('%Y-%m-%d %H_%M_%S')
        video = cv2.VideoWriter(f"{place}/" + place + "_" + nowDatetime_path + ".avi", fourcc, 30, (frame.shape[1], frame.shape[0]))
        start = False
        record = True

    elif record:
        video.write(frame)

    elif not record:
        print("end")
        start = True

def control_video():
    global record
    record = False
    print("!!!!!!!!Control Video!!!!!!!!")





