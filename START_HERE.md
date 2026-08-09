# Start Here

This repository is the final deployment project for the crop-and-weed detector trained on Roboflow. It intentionally **does not include a local training pipeline or model weight file** because the selected YOLO11 Nano model was trained and is served by Roboflow.

## Fast path

1. Rotate any Roboflow key that has appeared in a screenshot or chat.
2. Copy `.env.example` to `.env`.
3. Put the new private key in `ROBOFLOW_API_KEY`.
4. Install Python 3.11 and run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python scripts\preflight.py --require-key
pytest
python scripts\live_inference_test.py
python app.py
```

5. Open `http://127.0.0.1:7860`.
6. Push the repository to GitHub.
7. Create a Hugging Face **Gradio Space** and add `ROBOFLOW_API_KEY` as a **Secret**. Current Hugging Face account/hardware eligibility may affect whether a free Space can be created; see `docs/08_HUGGING_FACE_DEPLOYMENT.md`.

Read the documents in `docs/` in numeric order for the full implementation and study guide.
