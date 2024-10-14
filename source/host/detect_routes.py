import io
from application.Yolov8.yolov8_service import get_detect_result_img, get_detect_result_info
from application.Yolov8.Yolov8DetectionResult import Yolov8DetectionResult
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import APIRouter, UploadFile, File
from core.config import settings

# router初始化
router = APIRouter(prefix=f'/{settings.ROUTER_NAME_Object_Detection}', 
                   tags=[settings.ROUTER_NAME_Object_Detection])

@router.put('/Image', summary = '物件偵測(回傳結果圖片)', 
            description = '使用YOLOv8, 進行物件辨識, 並取得預測結果的圖片',
            response_class = StreamingResponse,
            responses = {200: {"content": {"image/png": {}}}})
async def detect(file: UploadFile = File(..., description="上傳影像檔案")):
    
    # 讀取上傳的影像檔案
    contents = await file.read()
    # image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    # 使用 yolov8 進行推論
    result_image = get_detect_result_img(contents)
    
    # 儲存影像至記憶體(bytes)
    img_byte_arr = io.BytesIO()
    result_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0) 
    
    return StreamingResponse(img_byte_arr, media_type = "image/png")

@router.put('/Image/Info', summary = '物件偵測(回傳結果資訊)', 
            description = '使用YOLOv8, 進行物件辨識, 並取得預測結果的資訊',
            response_class= JSONResponse,
            response_model=Yolov8DetectionResult)
async def detect_info(file: UploadFile = File(..., description="上傳影像檔案")):
    # 讀取上傳的影像檔案
    contents = await file.read()

    # 使用 yolov8 進行推論
    result_info = get_detect_result_info(contents)

    return result_info
