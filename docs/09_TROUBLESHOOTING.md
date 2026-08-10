# 9. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| PowerShell blocks activation | Script policy | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |
| `pytest` not found | Only runtime requirements installed | `pip install -r requirements-dev.txt` then `python -m pytest` |
| `ModuleNotFoundError` | Wrong environment or incomplete install | Activate `.venv` and reinstall requirements |
| Local browser cannot open localhost | Antivirus/firewall policy | Use CLI tests or the Render URL |
| Roboflow 401/403 | Invalid/expired key | Rotate the key and update `.env`/Render |
| Roboflow 404 | Incorrect model ID | Use `vaibhav-admane/crop-or-weed-detection-jnmzz-1-yolo11n-t1` |
| Roboflow 429 | Credits/quota/rate limit | Wait, reduce requests, or check provider usage |
| Render build fails | Python/dependency issue | Confirm `PYTHON_VERSION=3.11.11` and inspect logs |
| Render reports no open port | App not binding correctly | Start with `python app.py`; do not override `PORT` |
| Service is slow on first visit | Free-service cold start | Wait for the service to wake, then retry |
| Prediction is slow | Network/provider latency or large image | Test a smaller image and benchmark repeated calls |
| Image rejected | Dimension/pixel limit or corrupt file | Use a valid JPEG/PNG within configured limits |
| Empty detections | Threshold too high or model missed objects | Lower confidence carefully and review the image |
| Duplicate boxes | IoU threshold too high | Lower IoU to suppress overlaps more aggressively |
| Too few nearby plants | IoU threshold too low | Raise IoU slightly |
| Secret appears in Git history | Credential exposure | Rotate key immediately and remove it from history |
| CSS appears cached | Browser cache | Hard refresh with `Ctrl+Shift+R` |
