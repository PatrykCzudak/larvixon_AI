import torch
import cv2
import numpy as np
import base64
import matplotlib as plt
import time
import plotly.graph_objs as go
import os

def get_ai_response(vid_path="videos/GP032995_1.MP4", confidence_lvl=0.3, filename="test.png"):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=os.getcwd() + '/yolov5/runs/train/exp14/weights/best.pt')

    cap = cv2.VideoCapture(vid_path)
    
    results_frames = [] 
    trajectory = []
    start_time = time.time()
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('video.mp4', fourcc, 30.0, (1920, 540))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if time.time() - start_time > 120:
            break
        
        results = model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        for i in range(len(labels)):
            if int(labels[i]) == 0 or int(labels[i]) == 1:  
                x1, y1, x2, y2, conf = cord[i]
                ##print(conf)
                if conf > confidence_lvl:  #detekcja
                    h, w, _ = frame.shape
                    x1, y1, x2, y2 = int(x1*w), int(y1*h), int(x2*w), int(y2*h)
                    center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                    trajectory.append(center)

                    #kwadrat
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        #trajektoria
        for i in range(1, len(trajectory)):
            cv2.line(frame, trajectory[i - 1], trajectory[i], (0, 0, 255), 2)
            
        #cv2.imshow('Tracking', frame)
        out.write(frame)
        #
        #if cv2.waitKey(1) & 0xFF == 27:
        #    break

    cap.release() 
    out.release()
    cv2.destroyAllWindows()
    
    x,y = zip(*trajectory)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers+lines', name='Trajectory'))
    fig.update_layout(
    title='Trajectory of Detected Objects',
    xaxis_title='X Position',
    yaxis_title='Y Position',
    margin=dict(l=20, r=20, t=40, b=20)
    )
    fig.write_image(f"plots/{filename}")
        
    return fig

