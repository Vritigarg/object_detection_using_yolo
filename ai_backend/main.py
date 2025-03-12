from fastapi import FastAPI, File, UploadFile

from pydantic import BaseModel
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List


app = FastAPI()

class DetectionResult(BaseModel):
    boxes: List[List[float]]
    labels: List[str]
    scores: List[float]



# Load the YOLOv8 model
model = YOLO("yolov8n.pt")



@app.post("/detect", response_model=DetectionResult)
async def detect_objects(file: UploadFile = File(...)):
    # Read and decode the uploaded image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)  
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    
    results = model.predict(img)

    # Extract predictions
    predictions = results[0]
    boxes = predictions.boxes.xyxy.cpu().numpy().tolist()
    scores = predictions.boxes.conf.cpu().numpy().tolist()
    labels = [model.names[int(cls)] for cls in predictions.boxes.cls.cpu().numpy()]

   
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        label = f"{labels[i]}: {scores[i]:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    
    output_image_path = "output.jpg"
    cv2.imwrite(output_image_path, img)

    
    return DetectionResult(boxes=boxes, labels=labels, scores=scores)










