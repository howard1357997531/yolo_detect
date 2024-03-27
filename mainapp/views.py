from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def home(request):
    return render(request, 'home.html', locals())

import sys
import os
from pathlib import Path
FILE = Path(__file__).resolve()
print('FILE: ', FILE)
ROOT = FILE.parents[0]  # YOLOv5 root directory
# print("ROOT:", ROOT)  # D:\work\a\project1\yolo_detect\mainapp
# print(sys.path)       # ['D:\\work\\a\\yolo_detect\\yolo_detect', 'c:\\python38\\python38.zip', 'c:\\python38\\DLLs',['D:\\work\\a\\yolo_detect\\yolo_detect', 'c:\\python38\\python38.zip', 'c:\\python38\\DLLs', ...]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))
# print("ROOT:", ROOT)    # mainapp 
from models.experimental import attempt_load
from utils.general import non_max_suppression
import torch.backends.cudnn as cudnn
from base64 import b64decode, b64encode
import cv2
import torch
from auth_user.models import CameraSplitSetting, CameraSplitSettingPrivate, AlertPureQuantity, AlertPureQuantityPrivate

# 使用cv2.Dshow() intel_camera 問題還是無法解決
# 猜測可能是要在while True裡面一次瞟兩個cap, 像test.py一樣,這邊是跑兩個 while
# web_camera
def web_camera(request): 
    # print('os.path.dirname(__file__)[:-8]:', os.path.dirname(__file__)[:-8]) # D:\work\a\yolo_detect\yolo_detect
    return render(request, 'yolo/web_camera.html', locals())

def web_camera_get_frame():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = attempt_load('yolov5s.pt', device=device)  # model weight here, replace yolov5s.pt
    cudnn.benchmark = True
    names = model.module.names if hasattr(model, 'module') else model.names

    intel_camera_isopen = list(rs.context().devices)
    if intel_camera_isopen:
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = torch.from_numpy(frame)
        img = img.permute(2, 0, 1).float().to(device)
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.50, 0.45)  # img, conf, iou

        #　print(frame.shape) #(480, 640, 3)
        
        for i, det in enumerate(pred):
            if len(det):
                for d in det:
                    # d = (x1, y1, x2, y2, conf, cls)
                    x1 = int(d[0].item())
                    y1 = int(d[1].item())
                    x2 = int(d[2].item())
                    y2 = int(d[3].item())
                    c = int(d[5].item())
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # box
                    frame = cv2.putText(frame, names[c], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 0, 255), 2, cv2.LINE_AA)  # object name

        # cv2.imwrite( f'static/frame_output.jpg', frame) # open('static/frame_output.jpg', 'rb').read(        
        jpeg = cv2.imencode('.jpg', frame)[1]

        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

def web_camera_video_feed(request):
    return StreamingHttpResponse(web_camera_get_frame(), content_type = 'multipart/x-mixed-replace; boundary=frame')

# intel_camera
from utils.dataloaders import IMG_FORMATS, VID_FORMATS
from utils.general import  check_file, check_img_size, cv2, increment_path, non_max_suppression, scale_boxes
from utils.plots import Annotator, colors
from utils.torch_utils import select_device, time_sync
from models.common import DetectMultiBackend
import pyrealsense2 as rs
import numpy as np

def intel_camera(request):
    return render(request, 'yolo/intel_camera.html', locals())

@torch.no_grad()
def intel_camera_get_frame():
    weights = ROOT / 'minghong_v5m_110323.pt'  # model.pt path(s)
    source=ROOT / 'bus.jpg'  # file/dir/URL/glob, 0 for webcam
    data=ROOT / 'data/coco128.yaml'  # dataset.yaml path
    imgsz=(1920, 1080)  # inference size (height, width)
    conf_thres=0.25  # confidence threshold
    iou_thres=0.45  # NMS IOU threshold
    max_det=1000  # maximum detections per image
    device=''  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    save_txt=False  # save results to *.txt
    nosave=False  # do not save images/videos
    classes=None  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=False  # class-agnostic NMS
    augment=False  # augmented inference
    visualize=False  # visualize features
    update=False  # update all models
    project=ROOT / 'runs/detect'  # save results to project/name
    name='exp'  # save results to project/name
    exist_ok=False  # existing project/name ok, do not increment
    line_thickness=2  # bounding box thickness (pixels)
    hide_labels=False  # hide labels
    hide_conf=True  # hide confidences
    half=False  # use FP16 half-precision inference
    dnn=False  # use OpenCV DNN for ONNX inference

    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    bs =1
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
    dt, seen = [0.0, 0.0, 0.0], 0

    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    pipeline = rs.pipeline()
    profile = pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)
    
    # 改用 Videoapture, rs套件可能會有問題
    cap2 = cv2.VideoCapture(1)
    while(True):
        t1 = time_sync()
        ret2, frame2 = cap2.read()
        # frames = pipeline.wait_for_frames()
        # aligned_frames = align.process(frames)
        # color_frame = aligned_frames.get_color_frame()
        # depth_frame = aligned_frames.get_depth_frame()
        # if not depth_frame or not color_frame:
        #     continue
        # img = np.asanyarray(color_frame.get_data())
        # depth_image = np.asanyarray(depth_frame.get_data())

        #img = cv2.resize(img, (640,640), interpolation = cv2.INTER_AREA)
        # img = cv2.resize(img, (640,480), interpolation = cv2.INTER_AREA)
        img = cv2.resize(frame2, (640,480), interpolation = cv2.INTER_AREA)
        im = np.asanyarray(img)
        im0 = im.copy()
        im = im[np.newaxis, :, :, :]
        # Stack
        im = np.stack(im, 0)

        # Convert
        im = im[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW
        im = np.ascontiguousarray(im)
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0

        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        # Inference
        #visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
        pred = model(im, augment=augment, visualize=False)

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Process predictions
        for i, det in enumerate(pred):  # per image

            # print(f"(i, det) : ({i}, {det})")
            #print(f"det[0] : {det[:, :4]}")
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))

            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    #s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                    annotator.box_label(xyxy, label, color=colors(c, True))

        jpeg = cv2.imencode('.jpg', im0)[1]

        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

def intel_camera_video_feed(request):
    return StreamingHttpResponse(intel_camera_get_frame(),
                    content_type='multipart/x-mixed-replace; boundary=frame')

def check_intel_camera_isopen(request):
    camera_isopen = list(rs.context().devices)
    print('camera_isopen:', camera_isopen)
    if not camera_isopen:
        return JsonResponse({'status': 'fail'})
    else:
        return JsonResponse({'status': 'done'})

# camera_split
def camera_split(request):
    intel_camera_isopen_list = list(rs.context().devices)
    intel_camera_isopen = True if intel_camera_isopen_list else False
    print(intel_camera_isopen)
    context = {'intel_camera_isopen': intel_camera_isopen}
    return render(request, 'yolo/camera_split.html', context)

def camera_split_setting(request):
    # 因為使用了cropper.js來切相機，不知道為何會額外啟動兩次相機(總共3次)
    # 有發生reload網頁之後打不開內建相機的問題(內建相機會一直處於開起的狀態，用cap.isOpened()檢查的話)，
    # 但使用cap.release()之後又好了，所以在這頁面每次進來先release一次
    camera_name = ['web-camera', 'intel-camera', 'camera-3', 'camera-4', 'camera-5']
    if request.user.is_authenticated:
        camera = [CameraSplitSettingPrivate.objects.filter(user=request.user, camera_name=camera).first().is_original_state 
                  if CameraSplitSettingPrivate.objects.filter(user=request.user, camera_name=camera).exists()
                  else False
                  for camera in camera_name]
    camera_is_original_state = [camera.is_original_state for camera in CameraSplitSettingPrivate.objects.filter(user=request.user)] + [True]*3
    intel_camera_is_connected = True if list(rs.context().devices) else False
    camera_is_connected = [True, intel_camera_is_connected, True, True, True]
    camera_zip = zip(camera_name, camera_is_original_state, camera_is_connected)
    # 傳zip物件到前端無法多次使用(目前來看只能使用一次)，用list(zip)可以解決
    context = {'camera_zip': list(camera_zip)}
    return render(request, 'yolo/camera_split_setting.html', context)

def camera_split_setting_ajax(request):
    if request.method == 'POST' and is_ajax(request):
        cameraName = request.POST.get('cameraName')
        status = request.POST.get('status')
        if status == 'split':
            xCoordinate = float(request.POST.get('xCoordinate'))
            yCoordinate = float(request.POST.get('yCoordinate'))
            cropBoxWidth = float(request.POST.get('cropBoxWidth'))
            cropBoxHeight = float(request.POST.get('cropBoxHeight'))
            imgWidth = float(request.POST.get('imgWidth'))
            imgHeight = float(request.POST.get('imgHeight'))

        xStart = 0 if status == 'normal' else xCoordinate / imgWidth
        xEnd = 1 if status == 'normal' else (xCoordinate + cropBoxWidth) / imgWidth
        yStart = 0 if status == 'normal' else yCoordinate / imgHeight
        yEnd = 1 if status == 'normal' else (yCoordinate + cropBoxHeight) / imgHeight

        if request.user.is_authenticated:
            camera, created = CameraSplitSettingPrivate.objects.get_or_create(
                                user=request.user, camera_name=cameraName)      
        else:
            camera, created = CameraSplitSetting.objects.get_or_create(
                                camera_name=cameraName)
        camera.x_start = xStart
        camera.x_end = xEnd
        camera.y_start = yStart
        camera.y_end = yEnd

        if status == 'normal':
            camera.is_original_state = True
        else:
            camera.is_original_state = False
        camera.save()

        # alert
        if request.user.is_authenticated:
            if AlertPureQuantityPrivate.objects.filter(user=request.user).exists():
                max_code = AlertPureQuantityPrivate.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
                max_code = max_code if AlertPureQuantityPrivate.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
                AlertPureQuantityPrivate.objects.create(user=request.user, name='camera_setting', code=max_code)
            else:
                max_code = 1
                AlertPureQuantityPrivate.objects.create(user=request.user, name='camera_setting')
            alert, created = AlertPrivate.objects.get_or_create(user=request.user, is_checked=False)
        else:
            if AlertPureQuantity.objects.exists():
                max_code = AlertPureQuantity.objects.aggregate(Max('code')).get('code__max')
                max_code = max_code if AlertPureQuantity.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
                AlertPureQuantity.objects.create(user=request.user, name='camera_setting', code=max_code)
            else:
                max_code = 1
                AlertPureQuantity.objects.create(name='camera_setting')
            alert, created = Alert.objects.get_or_create(is_checked=False)
        alert.total_quantity += 1
        alert.alert_pure_code = max_code
        alert.alert_pure_camera_setting_quantity += 1

        last_one_item = alert.last_one_item
        if last_one_item == 'none':
            alert.last_one_item = 'camera_setting'
        else:
            if last_one_item != 'camera_setting':
                alert.last_one_item = 'camera_setting'
                alert.last_two_item = last_one_item
        alert.save()
        return JsonResponse({'ok': 'success'})

# image
def image(request):
    return render(request, 'yolo/image.html', locals())

from detect_image import run as image_run
from django.core.files.base import ContentFile
from image.models import (Image, ImagePrivate, ImageMultipleFolder, ImageMultipleFolderPrivate,
                          AlertImage, AlertImageNormalUser, AlertImageSuperUser,
                          AlertImageMultipleFolder, AlertImageMultipleFolderPrivate)
from auth_user.models import Alert, AlertPrivate

def image_detect(request):
    if  request.method == 'POST':
        file_name = request.POST.get('file_name')
        base64 = request.POST.get('base64')
        base64 = base64.split(',', 1)[1]
        
        run = image_run(hide_conf=True, base64=base64)    
        im_arr = cv2.imencode('.jpg', run)[1]
        im_bytes = im_arr.tobytes()
        im_b64 = b64encode(im_bytes)
        im_b64_tostring = im_b64.decode('ascii')
        im_b64 = 'data:image/jpeg;base64,' + im_b64_tostring

        # cv2 image(np.array) save to django model
        ret, buf = cv2.imencode('.jpg', run)
        content = ContentFile(buf.tobytes())
        count = 1
        
        if request.user.is_superuser or request.user.is_anonymous:
            name_repeat = Image.objects.filter(name=file_name).exists()
            user = 'superuser' if request.user.is_superuser else 'guest'
            if name_repeat:
                while name_repeat:
                    new_name = file_name[:-4] + '_' + str(count) + file_name[-4:]
                    name_repeat = Image.objects.filter(name=new_name).exists()
                    count += 1
                obj = Image(name=new_name, user=user)
                obj.image_file.save(new_name, content)
            else:
                obj = Image(name=file_name, user=user)
                obj.image_file.save(file_name, content)
        else:
            name_repeat = ImagePrivate.objects.filter(user=request.user, name=file_name).exists()
            if name_repeat:
                while name_repeat:
                    new_name = file_name[:-4] + '_' + str(count) + file_name[-4:]
                    name_repeat = ImagePrivate.objects.filter(user=request.user, name=new_name).exists()
                    count += 1
                obj = ImagePrivate(user=request.user, name=new_name)
                obj.image_file.save(new_name, content)
            else:
                obj = ImagePrivate(user=request.user, name=file_name)
                obj.image_file.save(file_name, content)

        #alert
        if request.user.is_superuser:
            if AlertImageSuperUser.objects.filter(user=request.user).exists():
                max_code = AlertImageSuperUser.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
                code = max_code if AlertImageSuperUser.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
                AlertImageSuperUser.objects.create(user=request.user, source=obj, code=code).save()
            else:
                AlertImageSuperUser.objects.create(user=request.user, source=obj).save()
        elif request.user.is_authenticated:
            if AlertImageNormalUser.objects.filter(user=request.user).exists():
                max_code = AlertImageNormalUser.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
                code = max_code if AlertImageNormalUser.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
                AlertImageNormalUser.objects.create(user=request.user, source=obj, code=code).save()
            else:
                AlertImageNormalUser.objects.create(user=request.user, source=obj).save()
        else:
            if AlertImage.objects.exists():
                max_code = AlertImage.objects.aggregate(Max('code')).get('code__max')
                code = max_code if AlertImage.objects.filter(is_checked=False).exists() else max_code + 1
                AlertImage.objects.create(source=obj, code=code).save()
            else:
                AlertImage.objects.create(source=obj).save()

        return JsonResponse({'ok': 'success', 'base64': im_b64})

# image_multiple
import time
import threading

def image_multiple(request):
    return render(request, 'yolo/image_multiple.html', locals())

def image_multiple_ajax(request):
    if request.method == 'POST':
        '''
        # 使用多執行續有時候cuda會跑error
        threads = []
        for i in range(int(len(request.POST)/2)):
            base64 = request.POST.get(f'base64_{i+1}')
            base64 = base64.split(',', 1)[1]
            threads.append(threading.Thread(target=image_run, kwargs={'hide_conf':True, 
                            'base64': base64, 'multiple_image_name': request.POST.get(f'image_name_{i+1}'), 
                            'multiple_image' : True}))

        for i in range(int(len(request.POST)/2)):
            threads[i].start()
            time.sleep(0.5)

        for i in range(int(len(request.POST)/2)):
            threads[i].join()
        '''

        # 用for迴圈是一定不會有問題，但就是會很慢(多執行序快多了)
        for i in range(int(len(request.POST)/2)):
            base64 = request.POST.get(f'base64_{i+1}')
            base64 = base64.split(',', 1)[1]
            file_name = request.POST.get(f'image_name_{i+1}')
            count = 1
            
            if request.user.is_superuser or not request.user.is_authenticated:
                name_repeat = Image.objects.filter(name=file_name).exists()
                if name_repeat:
                    while name_repeat:
                        new_name = file_name[:-4] + '_' + str(count) + file_name[-4:]
                        name_repeat = Image.objects.filter(name=new_name).exists()
                        count += 1
                    run = image_run(hide_conf=True, base64=base64, multiple_image_name=new_name,
                                    multiple_image=True)
                    ret, buf = cv2.imencode('.jpg', run)
                    content = ContentFile(buf.tobytes())
                    obj = Image(name=new_name)
                    obj.image_file.save(new_name, content)
                else:
                    run = image_run(hide_conf=True, base64=base64, multiple_image_name=file_name,
                                    multiple_image=True)
                    ret, buf = cv2.imencode('.jpg', run)
                    content = ContentFile(buf.tobytes())
                    obj = Image(name=file_name)
                    obj.image_file.save(file_name, content)
            else:
                name_repeat = ImagePrivate.objects.filter(user=request.user, name=file_name).exists()
                if name_repeat:
                    while name_repeat:
                        new_name = file_name[:-4] + '_' + str(count) + file_name[-4:]
                        name_repeat = ImagePrivate.objects.filter(user=request.user, name=new_name).exists()
                        count += 1
                    run = image_run(hide_conf=True, base64=base64, multiple_image_name=new_name,
                                    multiple_image=True)
                    ret, buf = cv2.imencode('.jpg', run)
                    content = ContentFile(buf.tobytes())
                    obj = ImagePrivate(user=request.user, name=new_name)
                    obj.image_file.save(new_name, content)
                else:
                    run = image_run(hide_conf=True, base64=base64, multiple_image_name=file_name,
                                    multiple_image=True)
                    ret, buf = cv2.imencode('.jpg', run)
                    content = ContentFile(buf.tobytes())
                    obj = ImagePrivate(user=request.user, name=file_name)
                    obj.image_file.save(file_name, content)

    return JsonResponse({'ok': '123'})

from django.db.models import Max

def image_multiple_folder_run(request, base64, file_name, save_to_album, code):
    run = image_run(hide_conf=True, base64=base64, multiple_image_name=file_name, multiple_image=True)
    ret, buf = cv2.imencode('.jpg', run)
    content = ContentFile(buf.tobytes())
    user = 'superuser' if request.user.is_superuser else 'guest'
    if save_to_album:
        if request.user.is_superuser or request.user.is_anonymous:
            obj = Image(name=file_name, user=user)
            obj2 = ImageMultipleFolder(code=code+1, name=file_name, user=user)
        else :
            obj = ImagePrivate(user=request.user, name=file_name)
            obj2 = ImageMultipleFolderPrivate(user=request.user, code=code+1, name=file_name)
        obj.image_file.save(file_name, content)
        obj2.image_file.save(file_name, content)

        #image
        if request.user.is_superuser:
            if AlertImageSuperUser.objects.filter(user=request.user).exists():
                max_code = AlertImageSuperUser.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
                max_code = max_code if AlertImageSuperUser.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
                AlertImageSuperUser.objects.create(user=request.user, source=obj, code=max_code)
            else:
                AlertImageSuperUser.objects.create(user=request.user, source=obj)
        elif request.user.is_authenticated:
            if AlertImageNormalUser.objects.filter(user=request.user).exists():
                max_code = AlertImageNormalUser.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
                max_code = max_code if AlertImageNormalUser.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
                AlertImageNormalUser.objects.create(user=request.user, source=obj, code=max_code)
            else:
                AlertImageNormalUser.objects.create(user=request.user, source=obj)
        else:
            if AlertImage.objects.exists():
                max_code = AlertImage.objects.aggregate(Max('code')).get('code__max')
                max_code = max_code if AlertImage.objects.filter(is_checked=False).exists() else max_code + 1
                AlertImage.objects.create(source=obj, code=max_code)
            else:
                AlertImage.objects.create(source=obj)
    else:
        if request.user.is_superuser or request.user.is_anonymous:
            obj = ImageMultipleFolder(code=code+1, name=file_name, user=user)
        else :
            obj = ImageMultipleFolderPrivate(user=request.user, code=code+1, name=file_name)
        obj.image_file.save(file_name, content)

# 選取多重檔案時不能選重複檔名的，所以在這邊也不用檢查重複檔名的問題
def image_multiple_folder_ajax(request):
    if request.user.is_superuser or request.user.is_anonymous:
        code = ImageMultipleFolder.objects.all().aggregate(Max('code')) # m = {'code__max': 1}
    else:
        code = ImageMultipleFolderPrivate.objects.filter(user=request.user).aggregate(Max('code'))
    # 如果沒有code會抓不到最大值，會回傳None
    code = 0 if code.get('code__max') is None else code.get('code__max')
    save_to_album = True if request.POST.get('save_to_album') == 'yes' else False
    # 因為多傳一個 request.posr 多傳一個 save_to_album 所以這邊要減一
    photo_count = (len(request.POST) - 1) / 2
    
    for i in range(int(photo_count)):
            base64 = request.POST.get(f'base64_{i+1}').split(',', 1)[1]
            file_name = request.POST.get(f'image_name_{i+1}')
            count = 1
            
            if request.user.is_superuser or request.user.is_anonymous:
                if save_to_album:
                    # 如果要儲存到相簿，再檢查image_name有沒有重複
                    name_repeat = Image.objects.filter(name=file_name).exists()
                    if name_repeat:
                        while name_repeat:
                            new_name = file_name[:-4] + '_' + str(count) + file_name[-4:]
                            name_repeat = Image.objects.filter(name=new_name).exists()
                            count += 1
                        image_multiple_folder_run(request, base64, new_name, save_to_album, code)
                    else:
                        image_multiple_folder_run(request, base64, file_name, save_to_album, code)
                else:
                    image_multiple_folder_run(request, base64, file_name, save_to_album, code)
            else:
                if save_to_album:
                    name_repeat = ImagePrivate.objects.filter(user=request.user, name=file_name).exists()
                    if name_repeat:
                        while name_repeat:
                            new_name = file_name[:-4] + '_' + str(count) + file_name[-4:]
                            name_repeat = ImagePrivate.objects.filter(user=request.user, name=new_name).exists()
                            count += 1
                        image_multiple_folder_run(request, base64, new_name, save_to_album, code)
                    else:
                        image_multiple_folder_run(request, base64, file_name, save_to_album, code)
                else:
                    image_multiple_folder_run(request, base64, file_name, save_to_album, code)

    # alert
    if request.user.is_authenticated:
        if AlertImageMultipleFolderPrivate.objects.filter(user=request.user).exists():
            max_code = AlertImageMultipleFolderPrivate.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
            max_code = max_code if AlertImageMultipleFolderPrivate.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
            AlertImageMultipleFolderPrivate.objects.create(user=request.user, code=max_code, folder_code=code+1, image_quantity=int(photo_count))
        else:
            AlertImageMultipleFolderPrivate.objects.create(user=request.user, folder_code=code+1, image_quantity=int(photo_count))
    else:
        if AlertImageMultipleFolder.objects.exists():
            max_code = AlertImageMultipleFolder.objects.aggregate(Max('code')).get('code__max')
            max_code = max_code if AlertImageMultipleFolder.objects.filter(is_checked=False).exists() else max_code + 1
            AlertImageMultipleFolder.objects.create(code=max_code, folder_code=code+1, image_quantity=int(photo_count))
        else:
            AlertImageMultipleFolder.objects.create(folder_code=code+1, image_quantity=int(photo_count))
        
    return JsonResponse({'ok': 'success'})

# video
import sys
sys.path.append('.')
from detect_video import run as video_run
from detect_video import BaseCamera
from video.models import Video, VideoPrivate, VideoOutput, VideoOutputPrivate
from django.conf import settings
import shutil
import ffmpeg

def extract_audio(video_path, output_path):
    ffmpeg.input(video_path).output(output_path, format='mp3').run()

def merge_audio_video(video_path, audio_path, output_path): 
    video = ffmpeg.input(video_path)
    audio = ffmpeg.input(audio_path)
    out = ffmpeg.output(video, audio, output_path, vcodec='libx264', acodec='copy')
    out.run()
    # os.system('taskkill /f /im ffmpeg.exe')

VIDEO_PATH = ''
VIDEO_NAME = ''

def video(request):
    print(settings.MEDIA_ROOT)
    print(os.path.join(settings.MEDIA_ROOT, 'video'))
    # 執行新的 ffmpeg 命令之前，先確保之前的 ffmpeg 執行程序已經結束並釋放對檔案的佔用。
    # 若要使用 shutil.rmtree 刪除指定檔案時，會因為 ffmpeg 還未執行結束會發生 error
    # error 為 [WinError 32] 程序無法存取檔案，因為檔案正由另一個程序使用
    os.system('taskkill /f /im ffmpeg.exe')
    # 是可以結束 ffmpeg 程序，但會跑出此: 錯誤: 找不到處理程序 "ffmpeg.exe"。
    # print(os.path.join(os.path.dirname(__file__)[:-8], 'static/media/video/video_output'))
    return render(request, 'yolo/video.html', locals())

def get_video(request):
    global VIDEO_PATH, VIDEO_NAME
    
    if request.method == 'POST':
        name = request.POST.get('name')
        myfile = request.FILES.get('file')        
        count = 1
        if request.user.is_superuser or request.user.is_anonymous:
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'video')):
                shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'video'))
            name_repeat = VideoOutput.objects.filter(name=name).exists()
            if name_repeat:
                while name_repeat:
                    new_name = name[:-4] + '_' + str(count) + name[-4:]
                    name_repeat = VideoOutput.objects.filter(name=new_name).exists()
                    count += 1
                Video.objects.create(name=new_name, videofile=myfile)
                os.rename(os.path.join(settings.MEDIA_ROOT, 'video',  name),
                        os.path.join(settings.MEDIA_ROOT, 'video',  new_name))
                name = new_name
            else:
                Video.objects.create(name=name, videofile=myfile)
            VIDEO_PATH = os.path.join(settings.MEDIA_ROOT, 'video',  name)
        else:
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, 'video_private', request.user.username)):
                shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'video_private', request.user.username))
            name_repeat = VideoOutputPrivate.objects.filter(user=request.user, name=name).exists()
            if name_repeat:
                while name_repeat:
                    new_name = name[:-4] + '_' + str(count) + name[-4:]
                    name_repeat = VideoOutputPrivate.objects.filter(user=request.user, name=new_name).exists()
                    count += 1
                VideoPrivate.objects.create(user=request.user, name=new_name, videofile=myfile)
                os.rename(os.path.join(settings.MEDIA_ROOT, 'video_private', request.user.username,  name),
                        os.path.join(settings.MEDIA_ROOT, 'video_private', request.user.username,  new_name))
                name = new_name
            else:
                VideoPrivate.objects.create(user=request.user, name=name, videofile=myfile)
            VIDEO_PATH = os.path.join(settings.MEDIA_ROOT, 'video_private', request.user.username, name)
        
        VIDEO_NAME = name
        audio_name = name.replace('.mp4', '') + '_audio.mp3'
        # ffmpeg
        if request.user.is_superuser or request.user.is_anonymous:
            audio_path = os.path.join(settings.MEDIA_ROOT, 'video', audio_name)
        else:
            audio_path = os.path.join(settings.MEDIA_ROOT, 'video_private', request.user.username, audio_name)  
        extract_audio(VIDEO_PATH, audio_path)
        
        if request.user.is_superuser or request.user.is_anonymous:
            Video.objects.all().delete()
        else:
            VideoOutputPrivate.objects.all().delete()

        return JsonResponse({'ok': 'success'})

def video_get_frame(request):
    global VIDEO_PATH
    camera = BaseCamera(request, True, VIDEO_PATH, False)
    cap = cv2.VideoCapture(VIDEO_PATH)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / 1)
    count = 1

    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if count == frame_count:
            # 加上 "data: Finished" 標記並結束串流
            yield b'data: Finished\n\n'
            break

        count += 1

def video_video_feed(request):
    response = StreamingHttpResponse(video_get_frame(request),
        content_type='multipart/x-mixed-replace; boundary=frame')

    return response

def video_merge_ajax(request):
    global VIDEO_NAME
    if request.method == 'POST' and is_ajax(request):
        # yolo偵測影片生成之後在使用ffmpeg合併音源檔yolo影片
        yolo_video_name = 'yolo_' + VIDEO_NAME
        audio_name = VIDEO_NAME.replace('.mp4', '') + '_audio.mp3'
        if request.user.is_superuser or request.user.is_anonymous:
            video_path = os.path.join(settings.MEDIA_ROOT, 'video', yolo_video_name)
            audio_path = os.path.join(settings.MEDIA_ROOT, 'video', audio_name)
            output_path = os.path.join(settings.MEDIA_ROOT, 'video_output', VIDEO_NAME)
        else:
            video_path = os.path.join(settings.MEDIA_ROOT, 'video_private', request.user.username, yolo_video_name)
            audio_path = os.path.join(settings.MEDIA_ROOT, 'video_private', request.user.username, audio_name)
            output_path = os.path.join(settings.MEDIA_ROOT, 'video_output', request.user.username, VIDEO_NAME)
        merge_audio_video(video_path, audio_path, output_path)
        # 執行新的 ffmpeg 命令之前，先確保之前的 ffmpeg 執行程序已經結束並釋放對檔案的佔用。
        # 若要使用 shutil.rmtree 刪除指定檔案時，會因為 ffmpeg 還未執行結束會發生 error
        # error 為 [WinError 32] 程序無法存取檔案，因為檔案正由另一個程序使用
        os.system('taskkill /f /im ffmpeg.exe')
        # 是可以結束 ffmpeg 程序，但會跑出此: 錯誤: 找不到處理程序 "ffmpeg.exe"。

        return JsonResponse({'ok': 'success'})


