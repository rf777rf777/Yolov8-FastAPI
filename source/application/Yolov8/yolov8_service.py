import torch, io
from application.Yolov8.Yolov8DetectionResult import Yolov8DetectionItem, Yolov8DetectionResult
from ultralytics import YOLO
from typing import List
from PIL import Image

# 檢查是否有可用的GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def __detect(contents: bytes, conf: float):
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    # Load the YOLO model
    model = YOLO("source/application/Yolov8/yolov8n.pt").to(device)
    results = model.predict(image, conf=conf) 

    # 確保數據被從 GPU 移動到 CPU
    result = results[0].cpu()

    # 刪除模型以釋放資源
    del model    
    # 清理 GPU 緩存
    torch.cuda.empty_cache()

    return  result 

def get_detect_result_img(contents: bytes, conf=0.5) -> Image.Image:

    result = __detect(contents, conf)

    # 取得預測結果的圖像 (PIL圖片格式)
    result_image_array = result.plot()  # 繪製 YOLO 的預測結果圖

    # 如果 result_image_array 是 BGR, 則轉換為 RGB
    if result_image_array.shape[-1] == 3:  # 檢查最後層是否為3個(彩色圖片有3個通道)
        result_image_array = result_image_array[:, :, ::-1]  # BGR to RGB

    # 確保數據範圍是 0-255，且數據類型是 uint8
    #result_image_array = np.clip(result_image_array, 0, 255).astype(np.uint8)

    # 將 numpy array 轉換為 PIL 圖片
    return Image.fromarray(result_image_array)

def get_detect_result_info(contents: bytes, conf=0.5) -> Yolov8DetectionResult:
    result = __detect(contents, conf)
    detections = []
    for box in result.boxes:
        detections.append(
            Yolov8DetectionItem(
                className=result.names[int(box.cls)], 
                confidence=float(box.conf), 
                box=box.xywh.tolist()))
    return Yolov8DetectionResult(detections=detections)