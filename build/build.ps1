# COMMON PATHS

$buildFolder = (Get-Item -Path "./" -Verbose).FullName
$slnFolder = Join-Path $buildFolder "../"
$outputFolder = Join-Path $buildFolder "outputs"
$appFolder = Join-Path $slnFolder "source"  # FastAPI 應用的文件夾
$containerName = "yolov8-fastapi"
$accountName = "rf777rf777"
$version = ":1.0.1"
$latest = ":latest"

## CLEAR ######################################################################

# 刪除舊的 outputs 文件夾
Remove-Item $outputFolder -Force -Recurse -ErrorAction Ignore
# 創建新的 outputs 文件夾
New-Item -Path $outputFolder -ItemType Directory

## COPY APP FILES #############################################################

# 將 app 目錄的內容複製到 outputs/Host 目錄
$outputHostFolder = Join-Path $outputFolder "Host"
New-Item -Path $outputHostFolder -ItemType Directory -Force
Copy-Item -Path $appFolder/* -Destination $outputHostFolder -Recurse -Force

## REMOVE __pycache__ #########################################################

# 刪除 outputs/Host 中的 __pycache__ 文件夾（遞歸刪除）
Remove-Item -Path "$outputHostFolder\__pycache__" -Recurse -Force -ErrorAction Ignore

## CREATE DOCKER IMAGES #######################################################

# 切換到 Host 文件夾，準備 Docker 映像構建
Set-Location $outputHostFolder

# 構建 Docker 映像
docker build -t $accountName/$containerName$version .

# 替 Docker 映像標記版號
#docker tag $accountName/$containerName$version $accountName/$containerName$version
docker tag $accountName/$containerName$version $accountName/$containerName$latest

# 推送 Docker 映像到Docker hub
docker push $accountName/$containerName$version
docker push $accountName/$containerName$latest

## FINALIZE ###################################################################

# 返回初始的工作目錄
Set-Location $buildFolder