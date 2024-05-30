import torch
import cv2
import numpy as np

def get_ai_response(vid_path="GP032995_1.MP4", confidence_lvl=0.3, path_to_save=""):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='/mnt/c/Wojtek_larwixon/yolov5/runs/train/exp14/weights/best.pt')

    cap = cv2.VideoCapture(vid_path)

    trajectory = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        for i in range(len(labels)):
            if int(labels[i]) == 0 or int(labels[i]) == 1:  
                x1, y1, x2, y2, conf = cord[i]
                #print(conf)
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
            print(trajectory[i])


        cv2.imshow('Tracking', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()