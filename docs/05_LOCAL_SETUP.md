# 5. Local Installation and Execution

## Prerequisites

- Python 3.11 recommended;
- internet access for Roboflow inference;
- a newly rotated private Roboflow API key;
- Git optional for repository operations.

## Windows PowerShell

```powershell
cd C:\data
Expand-Archive .\agrovision-ai-roboflow-hf-final.zip -DestinationPath .\agrovision-ai
cd .\agrovision-ai

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements-dev.txt

Copy-Item .env.example .env
notepad .env
```

Set only the new key:

```env
ROBOFLOW_API_KEY=YOUR_NEW_PRIVATE_KEY
```

Then verify and run:

```powershell
python scripts\preflight.py --require-key
python scripts\check_secrets.py
pytest
python scripts\smoke_test.py
python scripts\live_inference_test.py
python app.py
```

Open `http://127.0.0.1:7860`.

## Linux/macOS

```bash
unzip agrovision-ai-roboflow-hf-final.zip -d agrovision-ai
cd agrovision-ai

python3.11 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements-dev.txt

cp .env.example .env
nano .env

python scripts/preflight.py --require-key
python scripts/check_secrets.py
pytest
python scripts/smoke_test.py
python scripts/live_inference_test.py
python app.py
```

## Docker

```bash
cp .env.example .env
# Edit .env and add the private key.
docker compose up --build
```

Open `http://127.0.0.1:7860`.

## Normal local test

1. Select `examples/weed_example.jpeg`.
2. Keep confidence and IoU at `0.50`.
3. Click **Analyze field image**.
4. Confirm that an annotated image, KPI cards, a table, and JSON appear.

The exact detections can change when thresholds or provider model behavior change.
