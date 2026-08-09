# Quality-Assurance Report

## Package scope

This report covers the deployment repository only. The YOLO11 Nano model was trained externally on Roboflow; no local training script, downloadable checkpoint, or dataset is included.

## Checks executed in the build environment

| Check | Result |
|---|---|
| Python source compilation | Passed |
| Secret-pattern scan | Passed |
| Unit/integration tests with fake provider | **20 passed** |
| Gradio construction smoke test | Passed; **29 components** |
| Local Markdown target check | Passed |
| `pyproject.toml` parsing | Passed |
| Bundled example-image verification | Passed |
| Local Gradio HTTP start without API key | Passed; HTTP 200 in the build environment |
| Live Roboflow inference | **Not executed**; no new private key was available in the build environment |
| Docker image build | **Not executed**; Docker was unavailable in the build environment |
| Hugging Face build | **Not executed**; it requires the user's Space and secret |

## Environment note

The build environment used Python 3.13 for code-only checks. `inference-sdk==1.3.9` requires Python below 3.13, so the final project explicitly selects Python 3.11 for local, Docker, GitHub CI, and Hugging Face execution. The preflight script correctly rejects Python 3.13.

## What is verified

- imports and module paths for the application code;
- configuration validation and key omission from public summaries;
- image input validation and EXIF-removal path;
- Roboflow response parsing with representative direct and nested payloads;
- crop/weed class mapping;
- center-box to corner-box conversion and clamping;
- service orchestration using a fake hosted provider;
- bounding-box rendering and normalized output generation;
- Gradio UI construction and `/predict` event registration;
- repository secret scanning and ignored `.env` policy.

## What the user must verify with the new key

1. `python scripts/live_inference_test.py` returns a real prediction.
2. The exact model ID is authorized for the newly rotated key.
3. Available Roboflow credits permit requests.
4. The local web app predicts successfully.
5. The Hugging Face Space can make outbound HTTPS requests and receives predictions.
6. The live app's status, examples, output table, and JSON all work.

No live-provider result, latency value, deployment success, or new evaluation metric is claimed until those checks are performed.
