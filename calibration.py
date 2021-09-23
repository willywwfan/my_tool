import cv2
import numpy as np
import os
import time

def text_draw(text,img,position=(20,20)):
    font_scale = 1
    font = cv2.FONT_HERSHEY_PLAIN
    rectangle_bgr = (255, 255, 255)
    (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=1)[0]
    text_offset_x, text_offset_y = position
    box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width + 2, text_offset_y - text_height - 2))
    cv2.rectangle(img, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)
    cv2.putText(img, text, (text_offset_x, text_offset_y), font, fontScale=font_scale, color=(0, 0, 0), thickness=1)

#Set 
time_str = time.strftime("%Y_%m_%d_%H%M%S", time.localtime()) 
imsave_folder = './calibration_data/pic_' + time_str
if "calibration_data" not in os.listdir('./'):
    os.mkdir('./calibration_data')
os.mkdir(imsave_folder)
press_number = 0
cap = cv2.VideoCapture(0)# 選擇攝影機
max_press_number = 15

#Camera Clibration Parameters
CHECKERBOARD = (6, 9)# Define the dimensions of checkerboard
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
threedpoints = []# Vector for 3D points
twodpoints = []# Vector for 2D points
objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)#  3D points real world coordinates
objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)*24 #30mm
prev_img_shape = None

while (cap.isOpened()):
    key = cv2.waitKey(1)
    ret, frame = cap.read()
    # s to start the algrithm
    if ret:
        image = frame.copy()
        text = 'Saved number: ' + str(press_number)
        text_draw(text,image)
        text_hint = "Hint : Press s and q to save and quit. Must to save " + str(max_press_number) + " pictures."
        text_draw(text_hint,image,(20,40))
        cv2.imshow('image', image)
        if key == ord('s'):
            grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(grayColor, CHECKERBOARD,cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            if ret == True:
                # append camera calibration matrix
                threedpoints.append(objectp3d)
                corners2 = cv2.cornerSubPix(grayColor, corners, (11, 11), (-1, -1), criteria)# Refining pixel coordinates for given 2d points.
                twodpoints.append(corners2)
                #visualize
                image = cv2.drawChessboardCorners(image, CHECKERBOARD, corners2, ret)# Draw and display the corners
                cv2.imshow('image', image)
                cv2.waitKey(0)
                
                cv2.imwrite(imsave_folder+ '/' + str(press_number+1) + '.jpg', frame)
                press_number = press_number + 1
    if key == ord('q') or press_number == max_press_number:
        break
# 釋放攝影機
cap.release()
# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(threedpoints, twodpoints, grayColor.shape[::-1], None, None)
np.savez(imsave_folder + '/data.npz', mtx=matrix, dist=distortion, rvecs=r_vecs, tvecs=t_vecs)