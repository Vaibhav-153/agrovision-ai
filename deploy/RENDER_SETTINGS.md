# Render Web Service Settings

## Service

```text
Type: Web Service
Repository: Vaibhav-153/agrovision-ai
Branch: main
Runtime: Python
Root directory: blank
Build command: pip install -r requirements.txt
Start command: python app.py
Plan: Free for personal demonstration
```

## Environment variables

```text
PYTHON_VERSION=3.11.11
APP_NAME=AgroVision AI
APP_VERSION=1.1.0
LOG_LEVEL=INFO
ROBOFLOW_API_URL=https://serverless.roboflow.com
ROBOFLOW_MODEL_ID=vaibhav-admane/crop-or-weed-detection-jnmzz-1-yolo11n-t1
ROBOFLOW_CLASS_MAP={"0":"crop","1":"weed"}
MODEL_CONFIDENCE=0.50
MODEL_IOU=0.50
MAX_DETECTIONS=100
MAX_UPLOAD_MB=10
MAX_IMAGE_PIXELS=25000000
MAX_IMAGE_SIDE=8000
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW_SECONDS=60
```

Add this as a private secret value:

```text
ROBOFLOW_API_KEY=YOUR_PRIVATE_KEY
```

Do not manually set `PORT`.
