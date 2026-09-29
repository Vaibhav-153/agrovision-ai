# AgroVision YOLO11 Nano model card

## Summary

| Field | Value |
|---|---|
| Task | Two-class object detection |
| Classes | `crop`, `weed` |
| Model | YOLO11 Nano (`YOLO11n`) |
| Training method | Transfer learning |
| Starting checkpoint | MS COCO pretrained checkpoint |
| Training platform | Roboflow |
| Hosted model ID | `vaibhav-admane/crop-or-weed-detection-jnmzz-1-yolo11n-t1` |
| Serving provider | Roboflow Serverless API |
| Local checkpoint | Not included |

The model returns crop and weed detections with confidence scores and bounding boxes. Roboflow returns center-based boxes; the application converts them to `x1, y1, x2, y2` coordinates before rendering the result.

## Recorded validation values

The project material records the following Roboflow values:

| Metric | Value |
|---|---:|
| mAP50 / AP50 | 83.1% |
| Precision | 75.9% |
| Recall | 80.2% |
| Derived aggregate F1 | about 78.0% |
| Crop AP50 | 78% |
| Weed AP50 | 88% |
| Training time | 17 minutes |

A Roboflow chart in the earlier project material also recorded mAP50-95 of 0.5155 at epoch 135. The exact selected checkpoint epoch, optimizer, batch size, learning rate, augmentation settings, per-class precision/recall, and confusion matrix were not exported, so they are not claimed here.

## Intended use

This model is suitable for an educational crop/weed detection demo and for studying a hosted object-detection inference pipeline.

It should not be used as the only decision source for autonomous chemical spraying, cutting, crop removal, or machinery control.

## Limitations

- The public project does not include the trained `.pt` checkpoint.
- The dataset is small and may include near-duplicate or conflicting examples.
- Performance on unseen farms, crops, seasons, cameras, and lighting conditions has not been established.
- Inference depends on the Roboflow API, provider credits, and network availability.
