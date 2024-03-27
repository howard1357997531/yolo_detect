from django.shortcuts import render
from django.http import StreamingHttpResponse


import sys
import os
from pathlib import Path
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))
from models.experimental import attempt_load
from utils.general import non_max_suppression
import torch.backends.cudnn as cudnn
import cv2
import torch
from auth_user.models import CameraSplitSetting, CameraSplitSettingPrivate

def web_camera_pre_setting():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = attempt_load('yolov5s.pt', device=device)  # model weight here, replace yolov5s.pt
    cudnn.benchmark = True
    names = model.module.names if hasattr(model, 'module') else model.names

    return device, model, names

def web_camera_yield(frame, device, model, names, xStart, xEnd, yStart, yEnd):
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

    # cv2.imwrite( f'static/frame_output.jpg', frame) # open('static/frame_output.jpg', 'rb').read()
    #　print(frame.shape) #(480, 640, 3)
    
    width = frame.shape[1]
    height = frame.shape[0]
    xs = width * xStart
    xe = width * xEnd
    ys = height * yStart
    ye = height * yEnd
    jpeg = cv2.imencode('.jpg', frame[int(ys):int(ye), int(xs):int(xe)])[1]
    return jpeg

def web_camera_get_frame_split(request, mode):
    device, model, names = web_camera_pre_setting()
    # django
    if request.user.is_authenticated:
        camera = CameraSplitSettingPrivate.objects.filter(user=request.user, camera_name='web-camera').first()
    else:
        camera = CameraSplitSetting.objects.filter(camera_name='web-camera').first()

    if camera:
        if mode == 'split':
            xStart = camera.x_start
            xEnd = camera.x_end 
            yStart = camera.y_start
            yEnd = camera.y_end
    else:
        xStart = 0
        xEnd = 100 
        yStart = 0
        yEnd = 100

    # ------------------------------------

    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    intel_camera_isopen = list(rs.context().devices)
    if intel_camera_isopen:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        jpeg = web_camera_yield(frame, device, model, names, xStart, xEnd, yStart, yEnd)

        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        
def web_camera_video_feed_split(request, mode):
    return StreamingHttpResponse(web_camera_get_frame_split(request, mode), content_type = 'multipart/x-mixed-replace; boundary=frame')

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
def intel_camera_pre_setting():
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

    return device, model, names

def intel_camera_yield(frame, device, model, names, xStart, xEnd, yStart, yEnd):
    augment=False
    iou_thres=0.45
    max_det=1000
    conf_thres=0.25
    classes=None
    agnostic_nms=False
    line_thickness=2
    hide_labels=False
    hide_conf=True
    img = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
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

        #print(f"(i, det) : ({i}, {det})")
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

    width = im0.shape[1]
    height = im0.shape[0]
    xs = width * xStart
    xe = width * xEnd
    ys = height * yStart
    ye = height * yEnd
    jpeg = cv2.imencode('.jpg', im0[int(ys):int(ye), int(xs):int(xe)])[1]
    return jpeg
        
def intel_camera_get_frame_split(request, mode):
    device, model, names = intel_camera_pre_setting()
    # django
    if request.user.is_authenticated:
        camera = CameraSplitSettingPrivate.objects.filter(user=request.user, camera_name='intel-camera').first()
    else:
        camera = CameraSplitSetting.objects.filter(camera_name='intel-camera').first()

    if camera and mode == 'split':
        xStart = camera.x_start
        xEnd = camera.x_end 
        yStart = camera.y_start
        yEnd = camera.y_end
    else:
        xStart = 0
        xEnd = 100 
        yStart = 0
        yEnd = 100

    # 改用 Videoapture, rs套件可能會有問題
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while(True):
        ret, frame = cap.read()
        if ret:
            jpeg = intel_camera_yield(frame, device, model, names, xStart, xEnd, yStart, yEnd)
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        
def intel_camera_video_feed_split(request, mode):
    return StreamingHttpResponse(intel_camera_get_frame_split(request, mode),
                    content_type='multipart/x-mixed-replace; boundary=frame')

def all_camera_get_frame(request, camera_name):
    # django
    if request.user.is_authenticated:
        camera = CameraSplitSettingPrivate.objects.filter(user=request.user, camera_name=camera_name).first()
    else:
        camera = CameraSplitSetting.objects.filter(camera_name=camera_name).first()
    
    if camera:
        xStart = camera.x_start
        xEnd = camera.x_end 
        yStart = camera.y_start
        yEnd = camera.y_end
    else:
        xStart = 0
        xEnd = 100
        yStart = 0
        yEnd = 100
    # ------------------------------------

    web_camera_device, web_camera_model, web_camera_names = web_camera_pre_setting()
    if camera_name == 'intel-camera':
        intel_camera_device, intel_camera_model, intel_camera_names = intel_camera_pre_setting()
   
    intel_camera_isopen = list(rs.context().devices)
    if intel_camera_isopen:
        # 目前不知道為甚麼同時開web_camera和intel_camera, web會變1, intel會變0,
        # 而且還要多加 cv2.CAP_DSHOW 才不會報錯
        cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    else:
        cap1 = cv2.VideoCapture(0)
        cap2 = None

    while True:
        ret1, frame1 = cap1.read()
        ret2 = None
        if cap2 is not None:
            ret2, frame2 = cap2.read()
        
        if ret2 is None:
            jpeg = web_camera_yield(frame1, web_camera_device, web_camera_model, web_camera_names,
                                          xStart, xEnd, yStart, yEnd)
        else:
            if camera_name == 'web-camera':
                jpeg = web_camera_yield(frame2, web_camera_device, web_camera_model, web_camera_names,
                                          xStart, xEnd, yStart, yEnd)
            elif camera_name == 'intel-camera':
                jpeg = intel_camera_yield(frame1, intel_camera_device, intel_camera_model, intel_camera_names,
                                          xStart, xEnd, yStart, yEnd)
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        
def all_camera_video_feed(request, camera_name):
    return StreamingHttpResponse(all_camera_get_frame(request, camera_name), 
                                 content_type = 'multipart/x-mixed-replace; boundary=frame')