# 13. Final Verification Checklist

## Code

- [x] All required source files exist.
- [x] Imports compile.
- [x] Paths are derived from the repository location.
- [x] Configuration is environment-based.
- [x] API key is not hard-coded.
- [x] Model ID and class map are consistent.
- [x] Image validation and metadata removal are implemented.
- [x] Provider response parsing is implemented.
- [x] Bounding-box drawing is implemented.
- [x] UI calls the inference service.
- [x] User-safe errors are implemented.

## Tests

- [x] Configuration tests.
- [x] Secret-omission test.
- [x] Image-validation tests.
- [x] Invalid-input tests.
- [x] Response-parser tests.
- [x] Service output test.
- [x] Gradio smoke test.
- [x] Rate-limit behavior tests.
- [x] Local HTTP launch and `/predict` registration check.
- [ ] Live private-model test — requires the user's newly rotated key and network.

## GitHub

- [x] README.
- [x] `.gitignore`.
- [x] MIT license.
- [x] Security and contribution documents.
- [x] CI workflow.
- [x] Secret scanner.
- [x] Optional Hugging Face sync workflow.
- [ ] Public repository URL added after creation.

## Hugging Face

- [x] Gradio SDK metadata in README.
- [x] `app.py` at repository root.
- [x] Pinned `requirements.txt`.
- [x] Port-compatible local launch.
- [x] Space secret documentation.
- [ ] `ROBOFLOW_API_KEY` added as a Space Secret.
- [ ] Space build completed.
- [ ] Public example prediction verified.
- [ ] Space URL added to README and GitHub.

## ML claims

- [x] Recorded metrics are labeled as Roboflow validation results.
- [x] Exact mAP50–95 is marked unavailable.
- [x] Per-class precision/recall are marked unavailable.
- [x] Confusion matrix is marked unavailable.
- [x] No independent test-set claim is fabricated.
