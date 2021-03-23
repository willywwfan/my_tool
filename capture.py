import threading
import cv2
global timer
import sys
import time

def shot_img():
    global num
    success, frame = cameraCapture.read()
    path = "pic/"
    timer = threading.Timer(1, shot_img)
    localtime = time.asctime(time.localtime(time.time()))
    if (num % 30) == 0:
        cv2.imwrite( path + localtime + '.jpg', frame)
    print(num)
    num += 1
    if num==100000000:
        cameraCapture.release()
        cv2.destroyAllWindows()
        sys.exit()
    print(localtime)
    timer.start()

if __name__ == '__main__':
    num=0
    cameraCapture = cv2.VideoCapture(0)
    cameraCapture.set(3, 1920)
    cameraCapture.set(4, 1080)
    timer = threading.Timer(1,shot_img)
    timer.start()
