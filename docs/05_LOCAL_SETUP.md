# 5. Local Setup

## Windows

```powershell
cd C:\data\agrovision-ai
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
notepad .env
```

Set:

```env
ROBOFLOW_API_KEY=YOUR_PRIVATE_KEY
```

Run:

```powershell
python scripts\preflight.py --require-key
python -m pytest
python scripts\smoke_test.py
python scripts\live_inference_test.py examples\weed_example.jpeg
python app.py
```

Open `http://127.0.0.1:7860`.

## Linux/macOS

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

## Browser or firewall issue

If localhost is blocked, the command-line inference test still verifies the provider integration. Use the Render URL for browser testing.
