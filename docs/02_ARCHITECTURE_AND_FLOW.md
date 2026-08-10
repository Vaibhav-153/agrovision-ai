# 2. Architecture and Data Flow

## Deployment architecture

```text
GitHub repository
      ↓ automatic deploy
Render Web Service
      ↓
Gradio user interface and Python backend
      ↓
Roboflow Serverless API
      ↓
Hosted YOLO11 Nano model
```

## Prediction flow

```text
User image
  ↓
Gradio converts it to a Pillow image
  ↓
validate_image()
  ├─ confirm image exists
  ├─ decode pixels
  ├─ apply EXIF orientation
  ├─ enforce side and pixel limits
  └─ convert to metadata-free RGB copy
  ↓
temporary_jpeg()
  ├─ save sanitized JPEG
  └─ delete it after request
  ↓
RoboflowHostedModel.predict()
  ├─ apply confidence, IoU, and maximum detections
  ├─ call the hosted model
  └─ receive center-format predictions
  ↓
parse_predictions()
  ├─ map class IDs to crop/weed
  ├─ filter confidence
  ├─ convert x/y/width/height to x1/y1/x2/y2
  ├─ clamp boxes to image boundaries
  └─ sort by confidence
  ↓
AgroVisionService.analyze()
  ├─ draw boxes
  ├─ build KPI cards
  ├─ build a light HTML detection table
  └─ build normalized JSON
  ↓
Web result
```

## File connection map

```text
app.py
  ├─ Settings.from_env()             → config.py
  └─ create_demo(settings)           → ui.py

ui.py
  ├─ FixedWindowRateLimiter          → rate_limit.py
  ├─ AgroVisionService               → service.py
  └─ error classes                   → errors.py

service.py
  ├─ validation                      → image_utils.py
  ├─ hosted inference                → roboflow.py
  └─ drawing/table/summary           → visualization.py

roboflow.py
  ├─ Settings                        → config.py
  ├─ temporary_jpeg                  → image_utils.py
  ├─ typed result objects            → schemas.py
  └─ safe exceptions                 → errors.py
```

## Why Render does not need a GPU

Render hosts the web interface and sends an HTTPS request. The neural network runs on Roboflow infrastructure, so the Render service only needs CPU and memory for Gradio, Pillow, request handling, and visualization.
