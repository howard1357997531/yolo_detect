import argparse
import os
import platform
import sys
from pathlib import Path

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode

from django.conf import settings
from django.db.models import Max
from video.models import VideoOutput, VideoOutputPrivate, AlertVideo, AlertVideoNormalUser, AlertVideoSuperUser
import time
import ffmpeg

def merge_audio_video(video_path, audio_path, output_path): 
    video = ffmpeg.input(video_path)
    audio = ffmpeg.input(audio_path)
    out = ffmpeg.output(video, audio, output_path, vcodec='libx264', acodec='copy')
    out.run()

@smart_inference_mode()
def run(
        request,
        weights=ROOT / 'yolov5s.pt',  # model path or triton URL
        source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=True,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project='static/media/video',  # save results to project/name  存在static
        name='',  # save results to project/name
        exist_ok=True,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        vid_stride=1,  # video frame-rate stride
):
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)
    screenshot = source.lower().startswith('screen')
    if is_url and is_file:
        source = check_file(source)  # download

    # django
    # project='static/media/video'
    # os.path.dirname(__file__)[:-8]  :  D:\work\a\project1\yolo_detect
    if request.user.is_superuser or request.user.is_anonymous:
        # project='static/media/video_output'
        media_dir = os.path.join(os.path.dirname(__file__)[:-8], project)
        video_front_img_dir = os.path.join(os.path.dirname(__file__)[:-8], 'static/media/video_front_img')
    else:
        project = 'static/media/video_private'
        media_dir = os.path.join(os.path.dirname(__file__)[:-8], project, request.user.username)
        video_front_img_dir = os.path.join(os.path.dirname(__file__)[:-8], 'static/media/video_front_img', request.user.username)
        if not os.path.exists(video_front_img_dir):
            os.mkdir(video_front_img_dir)
    # ----------------------------------------

    # Directories           project='static' 會自動儲存偵測結果到static
    save_dir = increment_path(Path(media_dir) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  #make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  #check image size

    # Dataloader
    bs = 1  # batch_size
    if webcam:
        view_img = check_imshow(warn=True)
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot:
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else: # 影片、照片跑這
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())

    # django Video outputs fileurl
    django_model_video_name = ''
    for path, im, im0s, vid_cap, s, last in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inferencereturn_file
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            # 不知為何這邊i輸出一直為0
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}:'
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            # save_dir = 超級使用者和訪客: static/media/video  其餘: static/media/video_private/(request.user.username)
            # p.name = 123.mp4(example)
            p = Path(p)  # to Path
            video_name = 'yolo_' + p.name
            save_path = str(save_dir / video_name)
            django_model_video_name = p.name
                
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(f'{txt_path}.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))
                    if save_crop:
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

            # Stream results
            im0 = annotator.result()
            if view_img:
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        # 偵測完影片存至 save_path
                        print('save_path:', save_path)
                        # if os.path.isfile(save_path):
                        #     os.remove(save_path)
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer[i].write(im0)
                    # 切第一禎儲存影片封面
                    if seen == 1:
                        img_name = p.name.replace('.mp4', '.png')
                        img_path = os.path.join(video_front_img_dir, img_name)
                        cv2.imwrite(img_path, im0)
                    l = last # 影格式最後

        yield cv2.imencode('.jpg', im0)[1].tobytes()

        # Print time (inference-only)
        LOGGER.info(f"{s} {'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

    if request.user.is_superuser or request.user.is_anonymous:
        user = 'superuser' if request.user.is_superuser else 'guest'
        file_path = 'media/video_output/' + django_model_video_name
        front_img_name_file_path = 'media/video_front_img/' + django_model_video_name.replace('.mp4', '.png')
        video = VideoOutput(user=user, name=django_model_video_name, file_url=file_path,
                            front_img_name_url = front_img_name_file_path)
    else: 
        file_path = 'media/video_output/' + request.user.username + '/' + django_model_video_name
        front_img_name_file_path = 'media/video_front_img/' + request.user.username + '/' + django_model_video_name.replace('.mp4', '.png')
        video = VideoOutputPrivate(user=request.user, name=django_model_video_name, file_url=file_path,
                                          front_img_name_url = front_img_name_file_path)
    video.save()

    # alert
    if request.user.is_superuser:
        if AlertVideoSuperUser.objects.exists():
            max_code = AlertVideoSuperUser.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
            code = max_code if AlertVideoSuperUser.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
            AlertVideoSuperUser.objects.create(user=request.user, source=video, code=code)
        else:
            AlertVideoSuperUser.objects.create(user=request.user, source=video)
    elif request.user.is_authenticated:
        if AlertVideoNormalUser.objects.exists():
            max_code = AlertVideoNormalUser.objects.filter(user=request.user).aggregate(Max('code')).get('code__max')
            code = max_code if AlertVideoNormalUser.objects.filter(user=request.user, is_checked=False).exists() else max_code + 1
            AlertVideoNormalUser.objects.create(user=request.user, source=video, code=code)
        else:
            AlertVideoNormalUser.objects.create(user=request.user, source=video)
    else:
        if AlertVideo.objects.exists():
            max_code = AlertVideo.objects.aggregate(Max('code')).get('code__max')
            code = max_code if AlertVideo.objects.filter(is_checked=False).exists() else max_code + 1
            AlertVideo.objects.create(source=video, code=code)
        else:
            AlertVideo.objects.create(source=video)

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)

'''..................................'''

import time
import threading
import inspect
import ctypes

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class CameraEvent(object):
    """An Event-like class that signals all active clients when a new frame is
    available.
    """

    def __init__(self):
        self.events = {}

    def wait(self):
        """Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    event = CameraEvent()

    def __init__(self, request, hide_conf, source, save_crop):
        """Start the background camera thread if it isn't running yet."""
        # self.source=source
        self.request = request
        self.weights = ROOT / 'minghong_v5m_110323.pt'
        self.hide_conf = hide_conf
        self.source = source
        self.save_crop = save_crop
        self.img_flag = False
        if BaseCamera.thread is not None:
            stop_thread(BaseCamera.thread)
            BaseCamera.thread = None
        self.start_thread()  # 一呼叫馬上執行

    def start_thread(self):
        BaseCamera.last_access = time.time()

        # start background frame thread
        BaseCamera.thread = threading.Thread(target=self._thread)
        BaseCamera.thread.start()

        # wait until frames are available
        while self.get_frame() is None:
            time.sleep(0)

    def get_frame(self):
        """Return the current camera frame."""
        BaseCamera.last_access = time.time()

        # wait for a signal from the camera thread
        if not self.img_flag:  # 如果不是圖片
            BaseCamera.event.wait()
            BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        """"Generator that returns frames from the camera."""
        raise RuntimeError('Must be implemented by subclasses.')

    def _thread(self):
        """Camera background thread."""
        print('Starting camera thread.')
        frames_iterator = run(self.request, weights=self.weights, hide_conf=self.hide_conf, source=self.source, save_crop=self.save_crop)
        print('frames_iterator... {}, type: {}'.format(frames_iterator, type(frames_iterator)))
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # send signal to clients
            time.sleep(0)

            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.last_access > 15:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None
