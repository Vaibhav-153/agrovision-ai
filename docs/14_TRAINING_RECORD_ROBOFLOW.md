# 14. Roboflow Training Record

## Confirmed settings

| Field | Confirmed value |
|---|---|
| Task | Object detection |
| Model family | YOLO11 |
| Model size | Nano |
| Initialization | Public MS COCO checkpoint |
| Classes | crop, weed |
| Dataset size shown | about 1,300 images |
| Training platform | Roboflow |
| Duration | 17 minutes |
| Model ID | `vaibhav-admane/crop-or-weed-detection-jnmzz-1-yolo11n-t1` |

## Reported metrics

- mAP50 / AP50: 83.1%
- precision: 75.9%
- recall: 80.2%
- derived F1: about 78.0%
- crop AP50: 78%
- weed AP50: 88%
- strict chart point: mAP50–95 0.5155 at epoch 135

## Chart observations

- Performance curves improve quickly in early epochs.
- The curves plateau around the middle/later training stage.
- Box and class losses stabilize at lower values.
- Object loss shows a small late increase.
- The best checkpoint should come from validation performance near the peak, not automatically from the last epoch.

## Unknown training details

The platform did not export the exact:

- optimizer;
- batch size;
- learning rate;
- weight decay;
- augmentation settings;
- image size used by the fine-tuned run;
- early-stopping logic;
- selected checkpoint epoch.

These fields must remain unknown unless Roboflow exposes them later.
