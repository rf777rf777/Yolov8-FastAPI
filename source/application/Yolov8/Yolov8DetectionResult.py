from pydantic import BaseModel
from typing import List

class Yolov8DetectionItem(BaseModel):
    className: str
    confidence: float
    box: List[List[float]]

class Yolov8DetectionResult(BaseModel):
    detections: List[Yolov8DetectionItem]
