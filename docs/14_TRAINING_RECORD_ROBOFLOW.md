# 14. Roboflow Training Record

This document records what was actually selected in the Roboflow interface. It is not a local training script.

## Dataset

- Project: Crop or Weed Detection
- Task: Object Detection
- Reported images: approximately 1,300
- Classes used by deployment: `0 = crop`, `1 = weed`
- Dataset/source split was provided by the Roboflow project.

## Model setup

- Training engine: Custom Training
- Architecture: YOLO11
- Model size: Nano
- Initialization: Train from Public Checkpoint
- Public model: MS COCO
- Checkpoint: Best / Common Objects
- Training platform: Roboflow cloud

## Completion record

- Reported training duration: 17 minutes
- Reported mAP: 83.1%
- Reported precision: 75.9%
- Reported recall: 80.2%
- Validation AP50 by class: crop/class 0 = 78%, weed/class 1 = 88%
- Hosted model ID: `crop-or-weed-detection-jnmzz-1-yolo11n-t1/1`

## Information not exported

- exact optimizer;
- learning rate and schedule;
- batch size;
- weight decay and momentum;
- augmentation settings;
- exact completed epoch and early-stopping state;
- exact mAP50–95 value;
- class-specific precision and recall;
- confusion matrix;
- downloadable checkpoint.

## Why local training code is not included

The project goal is to deploy the already trained hosted model. Including unverified local training scripts would imply reproducibility that the available Roboflow configuration does not support. Future training work should be added only when the dataset and full configuration are available.

## Recommended evidence to save next time

- exported dataset/version hash;
- complete training configuration screenshot/export;
- metrics CSV/JSON;
- best checkpoint or registered model version;
- validation and test predictions;
- confusion matrix and class-level metrics;
- threshold sweep results.
