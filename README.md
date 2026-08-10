# AgroVision AI — Crop and Weed Detection

[![CI](https://github.com/Vaibhav-153/agrovision-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Vaibhav-153/agrovision-ai/actions/workflows/ci.yml)

**Live demo:** https://agrovision-ai-0-1.onrender.com/

AgroVision AI is an end-to-end agricultural object-detection application. It identifies and localizes two classes in an uploaded field image:

- `crop`
- `weed`

The web application runs on **Render**. The trained **YOLO11 Nano** model runs through the **Roboflow Serverless API**. The repository contains the application, tests, security controls, example images, training evidence, deployment configuration, and study documentation. It intentionally does not contain a local `.pt` checkpoint because Roboflow does not currently provide the trained weights on the selected plan.

> **Safety notice:** this is an educational and portfolio demonstration. Do not use its output as the only decision signal for autonomous spraying, cutting, or crop removal.

## Project status

| Component | Status |
|---|---|
| YOLO11 Nano model | Trained on Roboflow |
| Render live deployment | Working |
| Secure server-side Roboflow integration | Implemented |
| Image validation and EXIF removal | Implemented |
| Bounding boxes, counts, table, and JSON | Implemented |
| Training charts and metric explanation | Implemented |
| Automated offline tests | Implemented |
| GitHub CI and secret scan | Implemented |
| Local model checkpoint | Not available / not required |

## Main features

- Upload an image, use a webcam, or paste from the clipboard.
- Configure confidence, IoU, and maximum detections.
- Draw green crop boxes and orange weed boxes.
- Show crop count, weed count, total detections, average confidence, and round-trip latency.
- Show a clean output-only detection table with box coordinates.
- Return normalized JSON for API users.
- Include crop, weed, and mixed/challenging examples.
- Validate dimensions and pixel count before inference.
- Correct EXIF orientation and remove EXIF/GPS metadata.
- Store the Roboflow API key only on the server.
- Apply a small in-memory rate limit to reduce accidental credit usage.
- Explain the algorithm, metrics, charts, and each interface feature in simple English.

## Live architecture

```text
User browser
    ↓
Gradio interface on Render
    ↓
Image validation and EXIF removal
    ↓
Temporary sanitized JPEG
    ↓
Roboflow Serverless API
    ↓
YOLO11 Nano object detector
    ↓
Prediction normalization
    ↓
Bounding boxes + counts + HTML table + JSON
```

![Architecture](assets/architecture.svg)

## Model and algorithm

The detector uses **YOLO11 Nano (`YOLO11n`)**, a small one-stage object-detection model. “YOLO” means **You Only Look Once**: the network processes an image in one forward pass and predicts object classes and bounding boxes together.

The model was trained with **transfer learning**:

1. Start from a public model checkpoint trained on the MS COCO dataset.
2. Keep the useful visual features learned from general objects.
3. Fine-tune the model on the crop/weed dataset.
4. Produce a two-class detector for `crop` and `weed`.

The exact optimizer, batch size, learning rate, augmentation settings, and selected checkpoint epoch were not exported by the Roboflow plan, so this repository does not invent them.

## Recorded model evidence

| Metric | Recorded value | Interpretation |
|---|---:|---|
| mAP50 / AP50 | **83.1%** | Detection quality at IoU 0.50; higher is better. |
| Precision | **75.9%** | How many reported detections were correct. |
| Recall | **80.2%** | How many labelled objects the model found. |
| Derived F1 | **about 78.0%** | Balance between precision and recall. |
| Crop AP50 | **78%** | Average precision for crop. |
| Weed AP50 | **88%** | Average precision for weed. |
| Visible strict mAP50–95 | **0.5155 at epoch 135** | Best visible tooltip in the supplied chart. |
| Training time | **17 minutes** | Reported by the Roboflow completion email. |

The strict **mAP50–95** metric is the best primary metric for comparing checkpoints because it checks box quality over many IoU thresholds. For this agricultural use case, it should be reviewed together with **weed recall** and **crop precision**. Per-class precision/recall and the confusion matrix were not exported, so they are not claimed.

## Training charts

| Chart | How to read it |
|---|---|
| ![Model performance](assets/training_charts/model_performance.png) | Higher is better. Dark purple is the easier mAP50-style curve; light purple is the stricter mAP50–95 curve. |
| ![Box loss](assets/training_charts/box_loss.png) | Lower is better. The drop shows improving box placement. |
| ![Class loss](assets/training_charts/class_loss.png) | Lower is better. The drop shows improving crop/weed classification. |
| ![Object loss](assets/training_charts/object_loss.png) | Lower is better. The drop shows improving object-presence learning; the late increase suggests training had mostly converged. |

## Important inference controls

| Control | Default | Effect |
|---|---:|---|
| Confidence threshold | `0.50` | Lower returns more boxes and can improve recall; higher removes weak detections and can improve precision. |
| IoU threshold | `0.50` | Lower suppresses overlapping boxes more aggressively; higher keeps more nearby boxes. |
| Maximum detections | `50` in UI | Caps the number of highest-confidence detections returned. |

These values are useful operating defaults, not scientifically optimized thresholds.

## Project structure

```text
agrovision-ai/
├── app.py
├── render.yaml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── assets/
│   ├── custom.css
│   ├── architecture.svg
│   └── training_charts/
├── examples/
├── src/agrovision/
├── scripts/
├── tests/
├── deploy/RENDER_SETTINGS.md
├── docs/
└── .github/workflows/ci.yml
```

See [PROJECT_MANIFEST.md](PROJECT_MANIFEST.md) and [FILE_TREE.txt](FILE_TREE.txt) for every file.

## Local installation

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
notepad .env
```

Add the current private Roboflow key to `.env`:

```env
ROBOFLOW_API_KEY=YOUR_PRIVATE_KEY
```

Run checks:

```powershell
python scripts\preflight.py --require-key
python scripts\check_secrets.py
python -m pytest
python scripts\smoke_test.py
python scripts\live_inference_test.py examples\weed_example.jpeg
```

Run the application:

```powershell
python app.py
```

Open `http://127.0.0.1:7860`.

### Linux/macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
cp .env.example .env
python scripts/preflight.py --require-key
python -m pytest
python app.py
```

## Render deployment

The deployed service uses:

```text
Runtime: Python
Build command: pip install -r requirements.txt
Start command: python app.py
Python version: 3.11.11
```

Required secret:

```text
ROBOFLOW_API_KEY
```

Required normal variables are listed in [deploy/RENDER_SETTINGS.md](deploy/RENDER_SETTINGS.md). The included `render.yaml` can also be used as a Render Blueprint.

See [docs/08_RENDER_DEPLOYMENT.md](docs/08_RENDER_DEPLOYMENT.md) for the complete procedure.

## Testing

```bash
python -m compileall -q app.py src scripts tests
python scripts/check_secrets.py
python -m pytest
python scripts/smoke_test.py
```

Offline tests use a fake hosted model, so they do not consume Roboflow credits. A live API test is separate.

## API

Gradio registers the prediction endpoint as `/predict`. Use the **Use via API** link shown in the running application to view the client code generated for the current deployment.

Normalized JSON contains:

- image width and height;
- provider and model ID;
- total count and per-class counts;
- average confidence;
- confidence and IoU thresholds;
- latency;
- detection class, confidence, and bounding-box coordinates.

See [docs/16_API_USAGE.md](docs/16_API_USAGE.md).

## Documentation index

- [Project overview](docs/01_PROJECT_OVERVIEW.md)
- [Architecture and data flow](docs/02_ARCHITECTURE_AND_FLOW.md)
- [Model, algorithm, parameters, and charts](docs/03_MODEL_AND_PARAMETERS.md)
- [Implementation guide and file connections](docs/04_IMPLEMENTATION_GUIDE.md)
- [Local setup](docs/05_LOCAL_SETUP.md)
- [Testing and evaluation](docs/06_TESTING_AND_EVALUATION.md)
- [GitHub setup](docs/07_GITHUB_SETUP.md)
- [Render deployment](docs/08_RENDER_DEPLOYMENT.md)
- [Troubleshooting](docs/09_TROUBLESHOOTING.md)
- [Study notes](docs/10_STUDY_NOTES.md)
- [Viva questions](docs/11_VIVA_QA.md)
- [Presentation content](docs/12_PRESENTATION.md)
- [Final checklist](docs/13_FINAL_CHECKLIST.md)
- [Roboflow training record](docs/14_TRAINING_RECORD_ROBOFLOW.md)
- [Official references](docs/15_OFFICIAL_REFERENCES.md)
- [API usage](docs/16_API_USAGE.md)
- [End-to-end runbook](docs/17_END_TO_END_RUNBOOK.md)
- [Website features](docs/18_WEBSITE_FEATURES.md)

## Limitations

- The local `.pt` weights are unavailable.
- Inference depends on Roboflow availability, credits, and network access.
- The dataset is small and may contain near-duplicate or conflicting examples.
- Per-class recall, per-class precision, and a confusion matrix were not exported.
- Performance on unseen farms, crops, seasons, and cameras is not established.
- Render free services can sleep after inactivity, causing a cold start.
- The in-memory rate limiter is per process, not distributed.

## Future work

- obtain/export the trained checkpoint;
- rebuild leakage-safe train/validation/test splits;
- compare YOLO11 Nano, Small, and Medium;
- optimize thresholds using validation predictions;
- measure weed recall and crop precision;
- add independent field-image testing;
- add persistent monitoring and provider-independent inference.

## License

MIT License. See [LICENSE](LICENSE).

## Author

**Vaibhav Admane**
