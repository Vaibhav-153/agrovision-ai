# Start Here

1. Use Python **3.11**.
2. Create and activate `.venv`.
3. Install `requirements-dev.txt`.
4. Copy `.env.example` to `.env`.
5. Add the current private `ROBOFLOW_API_KEY` only to `.env` or Render Environment settings.
6. Run `python scripts/preflight.py --require-key`.
7. Run `python -m pytest` and `python scripts/smoke_test.py`.
8. Run one real test: `python scripts/live_inference_test.py examples/weed_example.jpeg`.
9. Start locally with `python app.py`.
10. Deploy from GitHub to Render using `docs/08_RENDER_DEPLOYMENT.md`.

Live application: https://agrovision-ai-0-1.onrender.com/
