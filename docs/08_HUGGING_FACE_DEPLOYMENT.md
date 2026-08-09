# 8. Hugging Face Spaces Deployment

## Deployment design

This repository uses a **Gradio Space**. Hugging Face runs the Python UI, while Roboflow executes YOLO inference. This avoids downloading the unavailable `.pt` file and avoids requiring a GPU in the Space for the current implementation.

## Step 1 — Create an account and check Space eligibility

Create/sign in to a Hugging Face account. Hugging Face plan and hardware rules can change. At the time this project was packaged, the official Spaces overview stated that creating Gradio or Docker Spaces generally requires an eligible paid account, while personal free accounts in good standing can host up to two Gradio Spaces using the ZeroGPU allowance. Check the current **New Space** screen before relying on a free deployment.

The AgroVision application performs inference remotely on Roboflow, so it does not need a GPU for model execution. Use an available Gradio hardware option offered by your account. If the account does not permit a Gradio Space, local execution and GitHub publication still work; deployment must wait for an eligible Space or use another Python host.

## Step 2 — Create a Space

1. Select **Create new Space**.
2. Name it, for example, `agrovision-ai`.
3. Select **Gradio** as the SDK.
4. Choose appropriate visibility.
5. Select an eligible runtime offered by your account. CPU is technically sufficient; an available ZeroGPU allocation also works because this app does not request local GPU inference.

The YAML block at the top of `README.md` defines the Space title, SDK, Gradio version, Python 3.11 runtime, and `app.py` entry point.

## Step 3 — Add the project files

### Option A: browser upload

Upload all repository files except `.env`, `.venv`, test caches, and local logs. Preserve folders.

### Option B: Git push

```bash
git remote add space https://huggingface.co/spaces/YOUR_HF_USERNAME/agrovision-ai
git push space main
```

Hugging Face may ask for a write token. Use a token as a password through a credential helper; do not embed it in committed files.

## Step 4 — Configure the private secret

Open:

```text
Space → Settings → Variables and secrets → New secret
```

Create:

```text
Name:  ROBOFLOW_API_KEY
Value: your newly rotated private key
```

Do not create this as a normal variable.

## Step 5 — Optional variables

Set these only when you need to override defaults:

```text
ROBOFLOW_MODEL_ID=crop-or-weed-detection-jnmzz-1-yolo11n-t1/1
ROBOFLOW_API_URL=https://serverless.roboflow.com
MODEL_CONFIDENCE=0.50
MODEL_IOU=0.50
MAX_DETECTIONS=100
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW_SECONDS=60
```

## Step 6 — Build and launch

Hugging Face installs `requirements.txt` and runs `app.py`. Watch the build log for package or Python errors. The app can start without a key but displays a configuration warning; prediction requires the secret.

## Step 7 — Validate the deployment

1. Open the Space App tab.
2. Confirm the status card says the private model connection is configured.
3. Load an included example.
4. Run one prediction.
5. Confirm annotated output, counts, table, and JSON.
6. Open **Use via API** and confirm the `predict` endpoint appears.
7. Test from an incognito browser.

## Common build failures

### Package version unavailable

Edit the pinned version only after checking compatibility. Rebuild the Space.

### `ROBOFLOW_API_KEY` missing

Add it as a Space secret and restart the Space.

### Unauthorized/private model error

Confirm the key belongs to the workspace that owns the model and that the model ID ends in `/1`.

### Roboflow credit/quota error

Review Roboflow usage. The Space cannot bypass provider limits.

### Slow first prediction

Serverless providers can have cold-start/network latency. Retry and monitor repeated latency.

## GitHub-to-Hugging-Face synchronization

The repository includes `.github/workflows/sync-huggingface.yml`.

Configure GitHub:

- repository secret: `HF_TOKEN` with write access;
- repository variable: `HF_SPACE_ID`, for example `username/agrovision-ai`.

Every push to `main` can then mirror the repository to the Space. The Roboflow key remains only in Hugging Face Secrets and is not transferred by Git.

## Public demo abuse protection

A public Space can consume Roboflow credits whenever visitors submit images. The app includes a small per-process rolling limiter and a Gradio queue, but these are not a substitute for provider quotas or an authenticated gateway. Keep the Space private/protected during testing, monitor usage, and lower `RATE_LIMIT_REQUESTS` when credits are limited.
