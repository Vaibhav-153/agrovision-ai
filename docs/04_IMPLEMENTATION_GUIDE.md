# 4. Complete Implementation Guide

## Phase 1 — Requirement analysis

The system had to use the already trained Roboflow model, avoid downloading unavailable weights, protect credentials, expose an understandable user interface, and deploy to GitHub and Hugging Face. Local model-training modules were deliberately excluded.

## Phase 2 — Environment setup

Python 3.11 was selected for compatibility with the pinned Gradio and Roboflow SDK stack. Runtime and development dependencies were separated into `requirements.txt` and `requirements-dev.txt`.

## Phase 3 — Model selection

The deployed checkpoint is YOLO11 Nano trained from an MS COCO public checkpoint. Nano was retained because it is the model actually trained and evaluated. Larger models were not substituted without evidence.

## Phase 4 — Model integration

`src/agrovision/roboflow.py` implements a lazy `InferenceHTTPClient`. It only imports/creates the provider client when prediction is requested, allowing the UI and tests to start without a key. `InferenceConfiguration` carries confidence, IoU, maximum detections, and the decision not to upload images for active learning.

## Phase 5 — Preprocessing

`src/agrovision/image_utils.py` validates the image, corrects orientation, limits dimensions/pixels, converts to RGB, and writes a temporary metadata-free JPEG. The temporary file is deleted in a `finally` block.

## Phase 6 — Application development

`src/agrovision/ui.py` builds the Gradio application. A small rolling-window limiter protects the shared hosted-inference budget from accidental request bursts; provider quotas and private/protected deployment remain the stronger controls. It includes upload/webcam/clipboard input, parameter controls, examples, an annotated output, KPI cards, a detection table, and normalized JSON. The `predict` event is also exposed as a Gradio API endpoint.

## Phase 7 — Post-processing

`parse_predictions()` accepts direct or nested response payloads. It maps class IDs, filters low-confidence or malformed boxes, converts center-format coordinates to corners, clamps coordinates, sorts by confidence, and applies the maximum result limit.

## Phase 8 — Testing

Tests use a fake hosted model and synthetic images, so CI never consumes Roboflow credits. Tests cover settings, secret omission, invalid inputs, response parsing, class mapping, bounding boxes, service output, and Gradio app construction.

## Phase 9 — Performance analysis

The application returns round-trip latency. Production monitoring should additionally record provider errors, p50/p95 latency, request rate, image sizes, and no-detection rate without storing private images.

## Phase 10 — GitHub deployment

The repository includes `.gitignore`, MIT license, contribution/security documents, CI, and a secret scanner. Model binaries, datasets, `.env`, and generated files are ignored.

## Phase 11 — Hugging Face deployment

The `README.md` YAML selects the Gradio SDK and `app.py`. The private key is created as a Space Secret. Since inference is remote, CPU hardware is enough for the application layer.

## Phase 12 — Validation

Verification includes Python compilation, unit tests, UI construction, secret scan, local launch, one live inference test, Hugging Face build logs, and public Space testing.

## Phase 13 — Future enhancement

Future work should clean label conflicts and duplicate leakage, evaluate an untouched test set, export per-class precision/recall and confusion matrices, compare YOLO11n/s/m under the same split, optimize class-aware thresholds, and optionally self-host a verified checkpoint.

## Important functions

| Function/class | File | Responsibility |
|---|---|---|
| `Settings.from_env()` | `config.py` | Read and validate environment configuration |
| `validate_image()` | `image_utils.py` | Validate, orient, sanitize, and convert the image |
| `FixedWindowRateLimiter.check()` | `rate_limit.py` | Enforce the configured per-process request budget |
| `temporary_jpeg()` | `image_utils.py` | Safely create/delete provider input |
| `find_prediction_payload()` | `roboflow.py` | Locate detection output in provider responses |
| `parse_predictions()` | `roboflow.py` | Normalize class/box/confidence data |
| `RoboflowHostedModel.predict()` | `roboflow.py` | Call the hosted model and time the request |
| `AgroVisionService.analyze()` | `service.py` | Orchestrate validation, inference, and output formatting |
| `annotate_image()` | `visualization.py` | Draw crop/weed labels and boxes |
| `create_demo()` | `ui.py` | Build the complete Gradio interface |
