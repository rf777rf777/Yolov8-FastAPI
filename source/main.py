import uvicorn, re
from fastapi import FastAPI
from host.detect_routes import router as yolov8_router
from starlette.routing import Route
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME_zh_TW,
    description=settings.PROJECT_NAME_EN_US,
    version=settings.VERSION,
    openapi_tags=[
        {
            "name": settings.ROUTER_NAME_Object_Detection,
            "description": settings.ROUTER_Description_Object_Detection
        }
    ])

# 註冊路由
app.include_router(yolov8_router)

# 讓路由大小寫不敏感(case-insensitive)
for route in app.router.routes:
    if isinstance(route, Route):
        route.path_regex = re.compile(route.path_regex.pattern, re.IGNORECASE)

# 啟動API
if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=False)