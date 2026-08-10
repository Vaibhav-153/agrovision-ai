# Project Manifest

## Entry and deployment files

| File | Purpose |
|---|---|
| `app.py` | Loads settings, builds the Gradio UI, and launches the server. |
| `render.yaml` | Optional Render Blueprint for build, start, and environment settings. |
| `.python-version` | Pins Python 3.11.11 for compatible deployment. |
| `.env.example` | Safe environment-variable template without credentials. |
| `requirements.txt` | Runtime dependencies. |
| `requirements-dev.txt` | Runtime dependencies plus pytest. |
| `Dockerfile` | Optional container build. |
| `docker-compose.yml` | Optional local Docker Compose start. |

## Application package

| File | Purpose |
|---|---|
| `src/agrovision/config.py` | Reads and validates environment variables. |
| `src/agrovision/errors.py` | Defines user-safe application exceptions. |
| `src/agrovision/image_utils.py` | Validates images, fixes orientation, removes metadata, and writes temporary JPEGs. |
| `src/agrovision/rate_limit.py` | Adds simple per-process request limiting. |
| `src/agrovision/roboflow.py` | Calls Roboflow and normalizes provider predictions. |
| `src/agrovision/schemas.py` | Defines typed boxes, detections, and prediction results. |
| `src/agrovision/service.py` | Joins validation, inference, rendering, table, and JSON generation. |
| `src/agrovision/visualization.py` | Draws boxes and builds summary/table HTML. |
| `src/agrovision/ui.py` | Defines all website components, events, examples, charts, and help text. |

## Assets and examples

| Path | Purpose |
|---|---|
| `assets/custom.css` | Complete light-theme visual design. |
| `assets/architecture.svg` | Current Render/Roboflow architecture diagram. |
| `assets/training_charts/` | Supplied Roboflow performance and loss graphs. |
| `examples/` | Crop, weed, and mixed demonstration images. |

## Quality files

| Path | Purpose |
|---|---|
| `tests/` | Offline unit and smoke tests that do not consume Roboflow credits. |
| `scripts/preflight.py` | Checks Python, packages, files, settings, and key presence. |
| `scripts/check_secrets.py` | Detects likely committed API keys. |
| `scripts/smoke_test.py` | Builds the UI and verifies the `/predict` API registration. |
| `scripts/live_inference_test.py` | Performs one real provider request. |
| `scripts/benchmark_latency.py` | Measures round-trip latency over repeated requests. |
| `.github/workflows/ci.yml` | Runs compile, secret scan, tests, and UI smoke checks. |

## Documentation

`README.md`, `START_HERE.md`, `MODEL_CARD.md`, `MODEL_REPORT.md`, `SECURITY.md`, `QA_REPORT.md`, and `docs/01_...` through `docs/18_...` explain the project, algorithm, features, code, evaluation, GitHub, Render, troubleshooting, study material, API, and deployment.
