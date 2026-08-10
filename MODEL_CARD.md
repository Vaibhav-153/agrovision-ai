# Model Card — AgroVision YOLO11 Nano

## Model summary

| Field | Value |
|---|---|
| Task | Two-class object detection |
| Classes | `crop`, `weed` |
| Architecture | YOLO11 Nano (`YOLO11n`) |
| Training method | Transfer learning |
| Starting checkpoint | MS COCO public checkpoint |
| Training platform | Roboflow Custom Training |
| Hosted model ID | `vaibhav-admane/crop-or-weed-detection-jnmzz-1-yolo11n-t1` |
| Serving provider | Roboflow Serverless API |
| Web deployment | Render Web Service |
| Local checkpoint | Not available |

## What the model does

The model receives one agricultural image and returns zero or more detections. Each detection contains:

- class ID;
- class name;
- confidence score;
- center-based box from Roboflow, converted by this app to `x1, y1, x2, y2` corner coordinates.

## Algorithm in simple English

YOLO means **You Only Look Once**. It is a one-stage detector: it looks at the image once, extracts visual features, and predicts object classes and boxes together. The Nano version is the smallest YOLO11 detector, selected because it offers a practical speed/size trade-off for a portfolio application.

Transfer learning was used. Instead of learning all visual features from zero, training started from a checkpoint already trained on the MS COCO dataset. The model then learned the crop and weed classes from the agricultural dataset.

## Recorded validation evidence

| Metric | Value |
|---|---:|
| Roboflow-reported mAP50 / AP50 | 83.1% |
| Precision | 75.9% |
| Recall | 80.2% |
| Derived aggregate F1 | About 78.0% |
| Crop AP50 | 78% |
| Weed AP50 | 88% |
| Best visible strict mAP50–95 tooltip | 0.5155 at epoch 135 |
| Training time | 17 minutes |

The exact selected checkpoint epoch, per-class precision, per-class recall, confusion matrix, optimizer, batch size, learning rate, and augmentation configuration were not exported. They are intentionally not guessed.

## Intended use

- educational demonstration;
- portfolio project;
- crop/weed detection experiments;
- API and MLOps deployment study;
- non-safety-critical agricultural image analysis.

## Out-of-scope use

Do not use this model as the only decision source for autonomous chemical spraying, cutting, removal, or machinery control.

## Important limitations

- small dataset;
- possible near-duplicate and label-conflict issues;
- unknown performance on unseen crops, farms, seasons, and cameras;
- cloud inference dependency;
- missing per-class recall/precision and confusion matrix;
- no downloadable local checkpoint in this repository.

## Runtime controls

- `MODEL_CONFIDENCE`: prediction acceptance threshold;
- `MODEL_IOU`: overlap threshold used for non-maximum suppression;
- `MAX_DETECTIONS`: maximum returned boxes.

These controls change inference behavior; they do not retrain the model.
