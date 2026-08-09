# Model Card — AgroVision YOLO11 Nano

## Model summary

- **Task:** two-class object detection
- **Classes:** crop (`0`), weed (`1`)
- **Architecture:** YOLO11 Nano
- **Initialization:** MS COCO public checkpoint
- **Training platform:** Roboflow
- **Serving platform:** Roboflow Serverless Cloud API
- **Model ID:** `crop-or-weed-detection-jnmzz-1-yolo11n-t1/1`
- **Weights included:** no

## Intended use

Educational, portfolio, and research demonstrations involving agricultural image analysis. The output can support human review and field-scouting prototypes.

## Out-of-scope use

Do not use the model as the only control signal for autonomous herbicide application, cutting, crop removal, or other safety-critical operations. Do not use it for plant species identification beyond the two configured labels.

## Recorded evaluation

| Metric | Value |
|---|---:|
| Roboflow validation mAP50/AP50 | 83.1% |
| Overall precision | 75.9% |
| Overall recall | 80.2% |
| Crop AP50 | 78.0% |
| Weed AP50 | 88.0% |
| Derived aggregate F1 | ~78.0% |
| Exact mAP50–95 | Not exported |
| Per-class precision/recall | Not exported |
| Confusion matrix | Not exported |
| Independent untouched test result | Not established |

The F1 value is derived from reported aggregate precision and recall; it was not directly exported.

## Training data

The Roboflow project reported approximately 1,300 annotated images. The underlying data may contain near-duplicate split leakage and some label conflicts identified during a previous audit. This limits how strongly validation results can be generalized.

## Input

An agricultural RGB image. The application supports upload, webcam, or clipboard input and applies image validation, orientation correction, RGB conversion, and metadata removal before inference.

## Output

Bounding boxes, class IDs/names, confidence scores, counts, latency, and normalized JSON.

## Limitations

- performance may degrade on new farms, cameras, growth stages, lighting, soil, blur, overlap, or background vegetation;
- hosted inference requires internet, a valid key, and available provider credits;
- thresholds are configurable but not yet optimized from exported validation predictions;
- exact model size and local memory requirements are unavailable because weights were not downloaded;
- the current class names are broad and do not identify plant species.

## Ethical and safety notes

False crop-as-weed predictions could cause damage if connected to automation. Human review and additional safety systems are mandatory for real-world control applications.
