import cv2
import websockets

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) != ord('q'):
    ret, frame = capture.read()
    
    if ret:
        cv2.imshow("videoFrame", frame)
    else:
        print("no frame")
        break

capture.release()
cv2.destroyAllWindows()


# 2. OpenCV로 동영상 파일 재생하기
# 위에서 말씀드렸 듯이 OpenCV를 이용해서 동영상 파일을 열 때도  cv2.VideoCapture 클래스를 이용합니다.
# 차이점은 cv2.VideoCapture( ) 안에 0 대신에 파일명을 넣어주면 됩니다.