# 17. End-to-End Runbook

This is the exact execution order for the final project. Model-training commands are intentionally absent because the selected YOLO11 Nano model was already trained on Roboflow and is accessed through its hosted inference API.

## Stage 0 — Revoke the exposed credential

A private Roboflow key appeared in an earlier screenshot. Before using this repository:

1. Open the Roboflow workspace API-key settings.
2. Revoke or roll the exposed private key.
3. Generate a new private key.
4. Do not paste the new value into chat, source code, screenshots, GitHub, or normal Hugging Face variables.

## Stage 1 — Extract the project

Recommended Windows location:

```powershell
New-Item -ItemType Directory -Force C:\data | Out-Null
Expand-Archive .\agrovision-ai-roboflow-hf-final.zip -DestinationPath C:\data
Set-Location C:\data\agrovision-ai-roboflow-hf-final
```

## Stage 2 — Install the supported Python version

Use 64-bit Python 3.11. The pinned Roboflow Inference SDK supports Python 3.10–3.12 and does not support Python 3.13.

Verify:

```powershell
py -3.11 --version
```

## Stage 3 — Create the local environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

For Command Prompt instead of PowerShell:

```bat
.venv\Scripts\activate.bat
```

## Stage 4 — Configure the private key

```powershell
Copy-Item .env.example .env
notepad .env
```

Change only this line:

```env
ROBOFLOW_API_KEY=YOUR_NEW_PRIVATE_KEY
```

Keep the model ID:

```env
ROBOFLOW_MODEL_ID=crop-or-weed-detection-jnmzz-1-yolo11n-t1/1
```

Do not add the workspace prefix to the direct model ID.

## Stage 5 — Run offline checks

These checks do not call Roboflow and do not consume inference credits:

```powershell
python -m compileall -q app.py src scripts tests
python scripts\check_secrets.py
pytest
python scripts\smoke_test.py
```

Expected project-build result:

```text
20 passed
Smoke test passed: 29 UI components loaded.
```

The exact duration may differ.

## Stage 6 — Run environment preflight

```powershell
python scripts\preflight.py --require-key
```

A pass confirms the supported Python version, dependencies, required files, settings, model ID, and configured key. It does not prove the remote model is reachable.

## Stage 7 — Perform one real hosted inference

```powershell
python scripts\live_inference_test.py examples\weed_example.jpeg
```

This command uses one real provider request. A successful result is normalized JSON containing fields such as `success`, `model_id`, `count`, `class_counts`, `latency_ms`, and `detections`.

If Roboflow reports an authorization, quota, model-ID, or network error, use `docs/09_TROUBLESHOOTING.md` before continuing.

### Optional latency benchmark

After the one-request test works, you may run:

```powershell
python scripts\benchmark_latency.py --runs 5 --warmup 1
```

This consumes six provider requests. Save the output only as measured deployment evidence for the same environment and date.

## Stage 8 — Run the web application

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:7860
```

Validate all of the following:

1. The status card says the private model connection is configured.
2. An included example loads.
3. The Predict button returns an annotated image.
4. Crop and weed counts appear.
5. The table and normalized JSON are populated.
6. Clear resets the interface.
7. No private key appears in the browser, logs, or JSON.

## Stage 9 — Create the GitHub repository

Create an empty GitHub repository named `agrovision-ai`. Do not ask GitHub to generate another README, license, or `.gitignore`.

Then run:

```powershell
git init
git add .
git status
```

Before committing, confirm `.env` is absent from staged files. Then:

```powershell
git commit -m "Initial production-ready AgroVision AI project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agrovision-ai.git
git push -u origin main
```

## Stage 10 — Create the Hugging Face Space

1. Create a new Space.
2. Choose **Gradio**.
3. Choose visibility suitable for the portfolio.
4. Select an eligible hardware/runtime offered by the account. Inference runs remotely, so local GPU execution is not required.
5. Push or upload the same repository while preserving directories.

Git option:

```powershell
git remote add space https://huggingface.co/spaces/YOUR_HF_USERNAME/agrovision-ai
git push space main
```

## Stage 11 — Add the production secret

In the Space, open:

```text
Settings → Variables and secrets → New secret
```

Create:

```text
Name: ROBOFLOW_API_KEY
Value: your newly rotated private key
```

Never create the private key as a normal variable.

Optional normal variables are listed in `deploy/HUGGING_FACE_SETTINGS.md`.

## Stage 12 — Verify the public deployment

1. Wait for the build status to become **Running**.
2. Open the App tab.
3. Confirm the configured status card.
4. Run an included example.
5. Review annotated output, counts, table, JSON, and latency.
6. Open **Use via API** and confirm `/predict` exists.
7. Test in an incognito browser.
8. Confirm the repository view does not contain `.env` or a key.

## Stage 13 — Connect GitHub updates to the Space

Manual workflow:

```powershell
git add .
git commit -m "Describe change"
git push origin main
git push space main
```

Automated workflow:

- GitHub secret: `HF_TOKEN`
- GitHub variable: `HF_SPACE_ID`, for example `username/agrovision-ai`

The included workflow `.github/workflows/sync-huggingface.yml` mirrors `main` to the Space. The Roboflow key remains only in Hugging Face Secrets.

## Stage 14 — Final portfolio evidence

Add these only after they exist:

- GitHub repository URL;
- live Hugging Face Space URL;
- one screenshot without credentials;
- actual live prediction output;
- measured p50/p95 latency from repeated requests if tested;
- known model limitations.

Do not claim an independent test result, exact mAP50–95, confusion matrix, or per-class precision/recall because those were not exported for this model.
