# Project Manifest

## Root files

| File | Purpose |
|---|---|
| `app.py` | Local and Hugging Face entry point; builds and launches Gradio |
| `README.md` | GitHub/Hugging Face landing page and main instructions |
| `START_HERE.md` | Shortest safe path from download to deployment |
| `requirements.txt` | Pinned runtime dependencies |
| `requirements-dev.txt` | Runtime plus test dependencies |
| `pyproject.toml` | Package metadata and pytest configuration |
| `.env.example` | Safe environment-variable template without credentials |
| `.gitignore` | Excludes secrets, environments, data, model binaries, and output |
| `.dockerignore` | Reduces container context and excludes secrets/tests/docs |
| `Dockerfile` | Optional container deployment using Python 3.11 |
| `docker-compose.yml` | Optional local container launch |
| `LICENSE` | MIT license |
| `MODEL_CARD.md` | Intended use, metrics, limitations, and safety |
| `MODEL_REPORT.md` | Recorded model results and missing evidence |
| `SECURITY.md` | Credential and upload-security policy |
| `CONTRIBUTING.md` | Contribution workflow |
| `CODE_OF_CONDUCT.md` | Collaboration expectations |
| `CHANGELOG.md` | Release history |
| `CITATION.cff` | Academic/software citation metadata |
| `QA_REPORT.md` | Executed checks, verified scope, and untested external integrations |
| `FILE_TREE.txt` | Snapshot of the distributable repository structure |

## Source package

| File | Purpose |
|---|---|
| `src/agrovision/__init__.py` | Package version |
| `src/agrovision/config.py` | Environment parsing, validation, public config |
| `src/agrovision/errors.py` | Stable expected exception types |
| `src/agrovision/schemas.py` | Typed boxes, detections, and prediction result |
| `src/agrovision/image_utils.py` | Input validation, EXIF handling, temporary JPEG |
| `src/agrovision/rate_limit.py` | Dependency-free rolling request limiter for provider-credit protection |
| `src/agrovision/roboflow.py` | Hosted SDK client and response normalization |
| `src/agrovision/visualization.py` | Bounding-box drawing and KPI HTML |
| `src/agrovision/service.py` | End-to-end analysis orchestration |
| `src/agrovision/ui.py` | Complete Gradio interface and API event |

## Tests

| File | Purpose |
|---|---|
| `tests/conftest.py` | Fixtures and fake hosted model |
| `tests/test_config.py` | Settings, key omission, model ID, thresholds |
| `tests/test_image_utils.py` | Image and parameter validation |
| `tests/test_roboflow_parser.py` | Provider response and box conversion |
| `tests/test_service.py` | End-to-end service output using fake model |
| `tests/test_ui.py` | Gradio build and predict API registration |
| `tests/test_rate_limit.py` | Request-budget enforcement and window recovery |

## Scripts

| File | Purpose |
|---|---|
| `scripts/preflight.py` | Environment, dependency, file, model, and key checks |
| `scripts/check_secrets.py` | Detect likely committed API keys |
| `scripts/smoke_test.py` | Build UI without opening a server |
| `scripts/live_inference_test.py` | One real provider request after key setup |
| `scripts/benchmark_latency.py` | Optional repeated live latency benchmark; explicitly consumes credits |

## Assets and examples

| Path | Purpose |
|---|---|
| `assets/custom.css` | Responsive agriculture-themed Gradio design |
| `assets/architecture.svg` | Deployment/data-flow diagram |
| `assets/screenshots/training_performance.png` | Supplied Roboflow training graph |
| `examples/*.jpeg` | Crop, weed, and mixed UI examples |

## Documentation

Documents `docs/01_...` through `docs/17_...` cover overview, architecture, model parameters, implementation, setup, evaluation, GitHub, Hugging Face, troubleshooting, study notes, viva, presentation, checklist, Roboflow training record, official references, and API usage.

## Automation

| File | Purpose |
|---|---|
| `.github/workflows/ci.yml` | Compile, secret scan, tests, and smoke test |
| `.github/workflows/sync-huggingface.yml` | Optional mirror from GitHub `main` to a Space |
| `deploy/HUGGING_FACE_SETTINGS.md` | Exact Space secret and variable names |
