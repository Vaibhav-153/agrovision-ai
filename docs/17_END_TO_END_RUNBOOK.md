# 17. End-to-End Runbook

## Stage 1 — Get the source

Clone or download the GitHub repository.

## Stage 2 — Create Python environment

Use Python 3.11 and install `requirements-dev.txt`.

## Stage 3 — Configure secret

Copy `.env.example` to `.env` and add the current private Roboflow key. Never commit `.env`.

## Stage 4 — Run checks

```bash
python scripts/preflight.py --require-key
python scripts/check_secrets.py
python -m pytest
python scripts/smoke_test.py
```

## Stage 5 — Verify live inference

```bash
python scripts/live_inference_test.py examples/weed_example.jpeg
```

## Stage 6 — Run locally

```bash
python app.py
```

Open `http://127.0.0.1:7860`.

## Stage 7 — Test website features

- upload one image;
- test all three examples;
- test confidence 0.30, 0.50, and 0.70;
- test IoU changes;
- verify boxes, counts, table, JSON, charts, and clear button;
- test an invalid file and oversized image.

## Stage 8 — Push to GitHub

Commit only source-safe files and ensure `.env` is absent.

## Stage 9 — Deploy to Render

Connect GitHub `main`, use the documented build/start commands, set Python 3.11.11, add environment variables, and add `ROBOFLOW_API_KEY` privately.

## Stage 10 — Validate production

- wait until deployment is live;
- hard refresh;
- run crop, weed, and mixed examples;
- check Render logs;
- record real latency;
- verify no key appears in browser source or repository.

## Stage 11 — Maintain

Every push to GitHub `main` triggers a new Render deployment. Run CI before merging changes.
