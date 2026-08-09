# 3. Model and Parameter Guide

## Model record

| Item | Value |
|---|---|
| Model family | YOLO11 object detection |
| Variant | Nano |
| Initialization | MS COCO public checkpoint |
| Classes | crop, weed |
| Model ID | `crop-or-weed-detection-jnmzz-1-yolo11n-t1/1` |
| Training | Roboflow-managed |
| Inference | Roboflow Serverless Cloud API |
| Local weight file | Not available / not required |

## Architecture overview

YOLO is a single-stage object detector. An image passes through a feature-extraction backbone, multi-scale feature aggregation, and a detection head that predicts boxes, object confidence, and class scores. The Nano variant reduces parameters and computation relative to larger variants, trading some potential accuracy for speed and lower resource use.

The exact exported checkpoint size and layer-by-layer model summary were not downloaded, so this repository does not claim a measured file size or local VRAM requirement.

## Input and output

### Input

- one RGB image;
- provider-side resizing handled by Roboflow/Inference SDK;
- project preprocessing was displayed as approximately 640×640 in the Roboflow dataset version UI;
- configurable confidence and IoU thresholds.

### Provider output

Roboflow returns predictions containing fields such as:

```json
{
  "x": 325,
  "y": 266.5,
  "width": 264,
  "height": 291,
  "confidence": 0.764,
  "class": "1",
  "class_id": 1
}
```

The application converts this to:

```json
{
  "class_id": 1,
  "class_name": "weed",
  "confidence": 0.764,
  "bbox": {
    "x1": 193.0,
    "y1": 121.0,
    "x2": 457.0,
    "y2": 412.0
  }
}
```

## Inference parameters

| Parameter | Recommended start | Meaning | Increase effect | Decrease effect | Change when |
|---|---:|---|---|---|---|
| `MODEL_CONFIDENCE` | `0.50` | Minimum accepted detection confidence | Fewer detections, usually higher precision | More detections, usually higher recall and more false positives | Lower it when weeds are being missed; raise it when false detections dominate |
| `MODEL_IOU` | `0.50` | IoU threshold used during non-maximum suppression | Allows more overlapping boxes to remain | Suppresses overlapping boxes more aggressively | Adjust when duplicate boxes appear or nearby plants are incorrectly merged/suppressed |
| `MAX_DETECTIONS` | `100` config; `50` UI default | Maximum returned boxes | Supports dense scenes but increases UI/output load | Limits clutter but may truncate true objects | Increase for highly dense plots; lower for demos or rate control |
| `MAX_UPLOAD_MB` | `10` | Upload-size protection | Accepts larger files | Reduces abuse and transfer time | Keep below provider limit and practical browser limits |
| `MAX_IMAGE_PIXELS` | `25,000,000` | Decompression-bomb protection | Accepts higher resolution | Rejects oversized images sooner | Change only after memory testing |
| `MAX_IMAGE_SIDE` | `8,000` | Longest accepted side | Accepts very large dimensions | Reduces memory/latency risk | Keep conservative for public demos |
| Gradio concurrency | `4` | Parallel prediction jobs | More throughput, more simultaneous provider calls/credit use | Less load, longer queue | Raise only after monitoring quotas and stability |
| `RATE_LIMIT_REQUESTS` | `30` | Requests allowed per process/window | More public capacity and credit exposure | Stronger protection, more rejections | Lower when provider credits are scarce |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` | Rolling limiter window | Longer protection window | Faster quota recovery | Change together with request budget |

## Training parameters

Training was performed inside Roboflow. The following are known:

- YOLO11 Nano architecture;
- MS COCO public checkpoint;
- approximately 1,300 images;
- two classes;
- Roboflow-managed training completed in about 17 minutes.

The exact optimizer, learning rate, batch size, warmup schedule, loss weights, early-stopping configuration, and exact final epoch were not exported. They must be recorded from Roboflow before claiming reproducibility of training. This deployment repository therefore focuses on reproducible inference rather than pretending those values are known.

## Runtime resources

The Hugging Face Space runs input processing and UI rendering on CPU. Neural-network inference occurs on Roboflow infrastructure. Local RAM use depends mainly on image size and Gradio, not on loading YOLO weights. Network latency and Roboflow cold starts are the main runtime variables.
