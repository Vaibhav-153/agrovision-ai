# 10. Study Notes

## One-minute explanation

AgroVision AI is a two-class object-detection web application. A user uploads a field image. The app validates it, fixes orientation, removes metadata, and sends a temporary JPEG to a YOLO11 Nano model hosted by Roboflow. The response is converted into crop/weed detections, corner coordinates, counts, confidence, latency, a light HTML table, and JSON. Gradio provides the interface, Render hosts the application, and GitHub stores and tests the code.

## Important concepts

### Object detection

Object detection predicts both **what** an object is and **where** it is.

### YOLO

YOLO is a one-stage detector. It predicts boxes and classes in one forward pass, making it suitable for fast applications.

### Transfer learning

The model began from a COCO checkpoint instead of random weights. Existing visual features were fine-tuned for crop and weed.

### Confidence

Confidence represents how strongly the model supports a detection. It is not a guarantee of correctness.

### IoU

Intersection over Union measures overlap between two boxes. It is used during evaluation and duplicate suppression.

### Non-maximum suppression

NMS removes repeated boxes that describe the same object.

### Precision and recall

Precision focuses on false positives. Recall focuses on missed objects. In agriculture, weed recall and crop precision are both important.

### mAP50–95

This is the best general comparison metric in the project because it evaluates box quality over several IoU thresholds.

## Why the project uses remote inference

The trained `.pt` file is unavailable on the current Roboflow plan. Remote inference allows the working model to be used without downloading weights. The trade-off is dependence on network connectivity, provider availability, and credits.

## Resume description

> Built and deployed AgroVision AI, a secure crop/weed object-detection application using YOLO11 Nano, Roboflow Serverless Inference, Gradio, Render, Python, GitHub Actions, and automated tests. Implemented image validation, metadata removal, configurable confidence/IoU controls, bounding-box rendering, class counts, structured JSON, rate limiting, and secure environment-based credentials.
