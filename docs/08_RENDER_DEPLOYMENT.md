# 8. Render Deployment

## Current live URL

https://agrovision-ai-0-1.onrender.com/

## Create the service

1. Sign in to Render with GitHub.
2. Select **New → Web Service**.
3. Connect the `agrovision-ai` repository.
4. Select branch `main`.
5. Use Python runtime.
6. Leave root directory blank.
7. Build command: `pip install -r requirements.txt`.
8. Start command: `python app.py`.
9. Select the free instance for a personal demonstration.

## Environment settings

Add the exact values from `deploy/RENDER_SETTINGS.md`.

Important secret:

```text
ROBOFLOW_API_KEY
```

Do not add `PORT`; Render supplies it automatically. The app binds to `0.0.0.0` and reads `PORT` from the environment.

## Python version

Use `PYTHON_VERSION=3.11.11`. The repository also includes `.python-version`.

## Automatic deployment

Each push to GitHub `main` causes Render to build and deploy the latest commit.

## Free-instance behavior

A free service can sleep after inactivity. The first request after sleep can take longer. This cold start is different from model inference latency.

## Troubleshooting

- Build failure: inspect dependency and Python-version logs.
- No open port: confirm `python app.py` and environment-provided `PORT`.
- Prediction 401/403: check the private key.
- Prediction 404: check the model ID.
- Prediction 429: provider quota or rate limit.
- Out of memory: reduce dependencies or image limits before upgrading.

## Blueprint

`render.yaml` contains the service definition. The private key is marked `sync: false` and must be entered manually.
