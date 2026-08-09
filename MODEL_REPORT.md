# Model Performance Report

## Baseline/deployed model

| Field | Recorded value |
|---|---|
| Model | YOLO11 Nano |
| Pretrained checkpoint | MS COCO public checkpoint |
| Dataset size | Approximately 1,300 images |
| Classes | crop, weed |
| Training platform | Roboflow |
| Training time | 17 minutes reported |
| Validation mAP50/AP50 | 83.1% |
| Precision | 75.9% |
| Recall | 80.2% |
| Derived F1 | ~78.0% |
| Crop AP50 | 78.0% |
| Weed AP50 | 88.0% |
| Exact mAP50–95 | Not exported |
| Crop precision/recall | Not exported |
| Weed precision/recall | Not exported |
| Confusion matrix | Not exported |
| Independent test result | Not established |
| Hosted model ID | `crop-or-weed-detection-jnmzz-1-yolo11n-t1/1` |

## Interpretation

The available Roboflow validation summary indicates that the model learned the two-class task and that class-1 AP50 was higher than class-0 AP50. Precision is lower than recall, suggesting false positives deserve attention. These metrics are not sufficient to quantify crop-as-weed versus weed-as-crop errors because the confusion matrix and per-class precision/recall were not exported.

## Deployment performance

The application measures round-trip latency for each live request. No fixed latency value is reported because it depends on network conditions, provider cold starts, image size, and quota state.

## Improvement claims

No improvement over another model is claimed. YOLO11 Small/Medium, RF-DETR, alternative image resolutions, augmentations, and confidence thresholds were not compared using the same controlled validation split.

## Required future report

A stronger final report should include a cleaned leakage-safe split, exact mAP50–95, class precision/recall/F1/AP, confusion matrix, error-analysis examples, threshold sweep, p50/p95 latency, and one untouched test-set evaluation.
