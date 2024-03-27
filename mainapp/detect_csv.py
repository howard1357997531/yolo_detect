import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn
from models.experimental import attempt_load
from utils.general import non_max_suppression
import pandas as pd
import datetime
import os

# yolov5s.pt :　yolo權重pt模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = attempt_load('yolov5s.pt', device=device)  # model weight here, replace yolov5s.pt
stride = int(model.stride.max())
cudnn.benchmark = True

names = model.module.names if hasattr(model, 'module') else model.names

cap = cv2.VideoCapture(0)  # source: replace the 0 for other source.

Class_name = []

Confidence = []

Time_det = []

detection_area = []

df = pd.DataFrame()

while(cap.isOpened()):
    
    ret, frame = cap.read()
    if ret == True:

        img = torch.from_numpy(frame)
        img = img.permute(2, 0, 1).float().to(device)
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = model(img, augment=False)[0]
        
        pred = non_max_suppression(pred, 0.50, 0.45)  # img, conf, iou
        
        for i, det in enumerate(pred):

            if len(det):

                for d in det:
                    # d = (x1, y1, x2, y2, conf, cls)
                    x1 = int(d[0].item())
                    y1 = int(d[1].item())
                    x2 = int(d[2].item())
                    y2 = int(d[3].item())
                    
                    conf = round(d[4].item(), 2)
                    
                    time_ref = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                    
                    c = int(d[5].item())
                    
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # box
                    
                    frame = cv2.putText(frame, names[c], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 0, 255), 2, cv2.LINE_AA)  # object name
                    
                    object_name = names[int(c)]
                    
                    data_base = {'class_name': {}, 'Confidence': {}, 'Time':{}}
                    
                    Coordinates = x1, x2, y1, y2
                    
                    Class_name.append(object_name)
                    
                    Confidence.append(conf)
                    
                    Time_det.append(time_ref)
                    
                    detection_area.append(Coordinates)
                    
                    #print(f'The corridinates are:{x1} {x2} {y1} {y2}')
                    
                    #print(f'The Corrdinates are:{Coordinates}')
                    
                    #print (f'The Confidence score is:{conf}')
                           
                    #print(f'The class name is:{object_name}') # print (x1, y1, x2, y2, conf, cls)
  
                df = pd.DataFrame(list(zip(Class_name, Confidence, Time_det, detection_area)),columns=['Class_name','Confidence','Time','Detection_Box']) 
    
        #print(data_base)     
        cv2.namedWindow('Text Detection', cv2.WINDOW_NORMAL)
        time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        cv2.imwrite( f'static/frame_output.jpg', frame)
        cv2.imshow('Text Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

df.to_csv(f'postgres_database/{datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%H-%M-%S")}.csv', index=False)

cap.release()
cv2.destroyAllWindows()
