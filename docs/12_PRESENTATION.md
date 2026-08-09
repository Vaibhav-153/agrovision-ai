# 12. Project Presentation — 12 Slides

## Slide 1 — Title

- AgroVision AI: Crop and Weed Detection
- YOLO11 Nano + Roboflow + Gradio
- Name, course, institution, date

## Slide 2 — Problem Statement

- Manual weed scouting is slow and inconsistent.
- Crop and weed appearance varies with lighting, age, soil, and overlap.
- Crop-as-weed errors can be harmful; missed weeds reduce effectiveness.

## Slide 3 — Objective

- Detect and localize crop/weed objects.
- Provide confidence, counts, boxes, and latency.
- Build a secure, deployable, portfolio-quality application.

## Slide 4 — Proposed Solution

- Fine-tuned YOLO11 Nano hosted on Roboflow.
- Gradio application on Hugging Face.
- Server-side secret and response normalization.

## Slide 5 — Technology Stack

- Python, Gradio, Pillow
- Roboflow Inference SDK / Serverless Cloud API
- Pytest, Docker, GitHub Actions
- Hugging Face Spaces

## Slide 6 — Model Architecture

- Single-stage YOLO detector
- Backbone → multi-scale features → detection head
- COCO pretraining and transfer learning
- Two output classes: crop and weed

## Slide 7 — System Workflow

- Upload image
- Validate and remove metadata
- Send to hosted YOLO model
- Normalize predictions
- Draw boxes and display results

## Slide 8 — Implementation

- Modular settings, inference, service, and UI layers
- Configurable confidence/IoU/max detections
- Secure environment variables
- Tests with a fake provider

## Slide 9 — Recorded Results

- Roboflow validation mAP50/AP50: 83.1%
- Precision: 75.9%
- Recall: 80.2%
- Crop AP50: 78%; Weed AP50: 88%
- State clearly that exact mAP50–95/confusion matrix were not exported

## Slide 10 — Deployment

- Source code on GitHub
- Gradio Space on Hugging Face
- Private `ROBOFLOW_API_KEY` in Space Secrets
- Remote GPU inference on Roboflow

## Slide 11 — Limitations and Future Scope

- Hosted API and credit dependency
- Dataset leakage/label-quality concerns
- Missing per-class precision/recall and independent test evaluation
- Future: clean split, threshold optimization, compare larger models, local/edge inference

## Slide 12 — Conclusion

- Complete end-to-end inference application
- Secure and reproducible deployment configuration
- Honest metric reporting
- Strong base for further agricultural CV research
