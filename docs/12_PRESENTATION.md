# 12. Presentation Content

## Slide 1 — Title
- AgroVision AI
- Crop and Weed Detection
- Author and institution

## Slide 2 — Problem statement
- Weeds compete with crops.
- Manual inspection is slow.
- Crop/weed confusion is risky.

## Slide 3 — Objective
- Detect and localize crop and weed plants.
- Show confidence, counts, boxes, table, and JSON.
- Deploy a secure public demonstration.

## Slide 4 — Proposed solution
- YOLO11 Nano detector.
- Roboflow-hosted inference.
- Gradio web interface.
- Render deployment.

## Slide 5 — Technology stack
- Python, Pillow, Gradio
- Roboflow Inference SDK
- Render
- GitHub Actions and pytest

## Slide 6 — Algorithm
- YOLO means You Only Look Once.
- One-stage object detection.
- Transfer learning from MS COCO.
- Two classes: crop and weed.

## Slide 7 — Data flow
- Upload → validation → metadata removal → Roboflow → normalization → annotation → results.

## Slide 8 — Website features
- Upload/webcam/clipboard
- Confidence, IoU, max detections
- Annotated result and KPI cards
- HTML table, JSON, examples, charts

## Slide 9 — Training results
- mAP50 83.1%
- Precision 75.9%
- Recall 80.2%
- Strict chart point 51.55% at epoch 135
- Explain all four charts

## Slide 10 — Deployment
- GitHub source
- Render auto-deploy
- Server-side API key
- Roboflow Serverless model

## Slide 11 — Limitations and future work
- No local weights
- Missing per-class recall/precision and confusion matrix
- Dataset quality and generalization concerns
- Future local model and independent test set

## Slide 12 — Conclusion
- Complete end-to-end working application
- Secure deployment and documented ML pipeline
- Suitable for further agricultural AI research
