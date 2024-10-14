class Settings:
    # API基本資料設定
    PROJECT_NAME_zh_TW: str = "FastAPI 物件偵測"
    PROJECT_NAME_EN_US: str = "FastAPI Object-Detection (by YOLOv8)"
    VERSION: str = "0.0.1"

    # router設定
    ROUTER_NAME_Object_Detection, ROUTER_Description_Object_Detection = ('Detection', 'Yolov8物件偵測')

settings = Settings()