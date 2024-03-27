from django.test import TestCase

# import cv2
# for i in range(10):
#     cap = cv2.VideoCapture(i)
#     if cap.isOpened():
#         # 尝试读取一帧图像
#         ret, frame = cap.read()
#         if ret:
#             print(f"找到设备ID: {i}")
#             cv2.imshow("Camera", frame)
#             cv2.waitKey(0)
#             break
#         cap.release()

import cv2
cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# cap1 = cv2.VideoCapture(0, cv2.CAP_V4L2)
# cap2 = cv2.VideoCapture(1, cv2.CAP_V4L2)
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    print('ret1 : ', ret1)
    print('ret2 : ', ret2)
    if ret1:
        cv2.imshow('cam1', frame1)
    
    if ret2:
        cv2.imshow('cam2', frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap1.release()
cap2.release()
cv2.destroyAllWindows()

# 只有web_camera ret1=True ret2=False
# web_camera 使用' cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 有連接intel_camera情況下，ret1=True ret2=True
# intel_camera 使用 cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# web_camera 使用 cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)


path = 'D:/work/a/yolo_detect/yolo_detect'
import os

# def add_ffmpeg_to_path(ffmpeg_path):
#     # 取得目前的環境變數中的 PATH 值
#     current_path = os.environ.get('PATH', '')
#     print(ffmpeg_path in current_path)
#     # 確認 ffmpeg.exe 的路徑是否已存在於環境變數中
#     if ffmpeg_path not in current_path:
#         # 將 ffmpeg.exe 的路徑加入環境變數的 PATH 中
#         os.environ['PATH'] = current_path + os.pathsep + ffmpeg_path



# # 將 ffmpeg.exe 的路徑新增到環境變數中
# ffmpeg_path = os.path.join(path, 'mainapp/ffmpeg.exe')
# add_ffmpeg_to_path(ffmpeg_path)

# 呼叫切割音訊的函式
# import ffmpeg
# def extract_audio(video_path, output_path):
#     ffmpeg.input(video_path).output(output_path, format='mp3').run()

# video_path = os.path.join(path, 'mainapp/video.mp4')
# output_path = os.path.join(path, 'mainapp/audio.mp3')
# extract_audio(video_path, output_path)

# import cv2
# import os
# path = 'D:/work/a/yolo_detect/yolo_detect'
# image = os.path.join(path, 'mainapp/12_46.png')
# a = cv2.imread(image)
# cv2.imshow('My Image', a)

# # 按下任意鍵則關閉所有視窗
# cv2.waitKey(0)
# cv2.destroyAllWindows()


