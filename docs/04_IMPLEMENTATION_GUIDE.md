# 4. Complete Implementation Guide

## Phase 1 — Requirements

The project needed a two-class crop/weed detector, secure cloud inference, a simple web interface, GitHub support, tests, and free personal deployment.

## Phase 2 — Model selection

YOLO11 Nano was selected on Roboflow. It is a small real-time object detector and matches the available hosted model.

## Phase 3 — Configuration

`config.py` reads environment variables, validates thresholds and limits, confirms HTTPS, validates the model ID, parses the class map, and prevents the private key from appearing in public summaries.

## Phase 4 — Image preprocessing

`image_utils.py`:

1. rejects missing or unsupported input;
2. decodes the image;
3. fixes camera orientation;
4. rejects excessive dimensions/pixels;
5. converts to RGB;
6. removes metadata;
7. writes a temporary JPEG;
8. deletes it after inference.

## Phase 5 — Hosted inference

`roboflow.py` creates the client lazily. It sends confidence, IoU, maximum detections, and the model ID. It normalizes direct or nested responses and converts center boxes to corner boxes.

## Phase 6 — Application service

`service.py` is the main orchestration layer. It calls validation, inference, annotation, summary generation, table generation, and JSON generation.

## Phase 7 — User interface

`ui.py` creates:

- hero and model status;
- image inputs;
- inference sliders;
- analyze and clear buttons;
- annotated output;
- KPI cards;
- detections table;
- JSON tab;
- model notes;
- labelled training charts;
- examples;
- feature and pipeline help.

## Phase 8 — Styling

`assets/custom.css` defines one clean light theme. The detection result uses a custom HTML table instead of an editable spreadsheet component, removing unnecessary sort/filter menus and dark-theme conflicts.

## Phase 9 — Testing

Unit tests use a fake hosted model. They verify settings, image validation, parsing, service output, table generation, rate limiting, and UI construction without spending provider credits.

## Phase 10 — GitHub

GitHub stores the source. CI compiles code, scans for secrets, runs tests, and builds the UI.

## Phase 11 — Render

Render connects to the GitHub `main` branch, installs `requirements.txt`, runs `python app.py`, and supplies environment variables. The API key is stored only in Render Environment settings.

## Phase 12 — Validation and future work

The live app must be tested on crop, weed, mixed, difficult, blurred, low-light, and unseen field images. Future scientific validation should include leakage-safe splits, per-class precision/recall, confusion matrix, and an untouched test set.
