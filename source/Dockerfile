# 使用帶有 CUDA 支持的 NVIDIA 基礎映像
FROM nvidia/cuda:12.5.0-runtime-ubuntu22.04

# 安裝系統依賴項
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 設置 Python 環境
RUN python3 -m pip install --upgrade pip

# 設置工作目錄
WORKDIR /app

# 複製當前目錄中的所有內容到工作目錄中
COPY . .

# 安裝 Python 依賴項，並啟用 CUDA 支持
RUN pip install --no-cache-dir torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117

# 安裝需要的Python package
RUN pip install --no-cache-dir wheel fastapi uvicorn pillow python-multipart

# 安裝 Real-ESRGAN
RUN pip install --no-cache-dir git+https://github.com/sberbank-ai/Real-ESRGAN.git

# 使用 ENTRYPOINT 指定啟動應用的命令
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]