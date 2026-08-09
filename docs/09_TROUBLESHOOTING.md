# 9. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Virtual environment inactive or requirements missing | Activate `.venv`; run `pip install -r requirements.txt` |
| Python version error | Unsupported Python version | Use Python 3.11 or 3.12 |
| UI starts but prediction fails | Missing API key | Add `ROBOFLOW_API_KEY` to `.env` or Space Secrets |
| Unauthorized Roboflow response | Wrong, revoked, or workspace-incompatible key | Generate a new private key and update the secret |
| Model not found | Incorrect model ID | Use `crop-or-weed-detection-jnmzz-1-yolo11n-t1/1` |
| Credit/quota failure | Roboflow plan usage exhausted | Review usage, wait for reset, or change provider plan/deployment |
| Network timeout | Connectivity, cold start, provider issue | Retry; check service status; increase timeout only after diagnosis |
| Invalid image | Corrupt/non-image upload | Use a valid JPEG/PNG/WebP image |
| Image too large | Dimension or pixel limit | Resize the image before upload |
| No detections | High threshold, domain shift, poor image, real absence | Lower confidence gradually; inspect image quality; do not assume failure |
| Duplicate boxes | IoU threshold too high | Reduce IoU threshold |
| Nearby plants suppressed | IoU threshold too low | Increase IoU threshold carefully |
| False positives | Confidence too low or domain shift | Raise confidence and collect representative negative examples |
| Missed weeds | Confidence too high or model weakness | Lower confidence and review weed recall on labeled data |
| Slow inference | Network/provider cold start, large image | Resize input; repeat test; measure p50/p95 |
| Hugging Face build fails | Dependency/version issue | Inspect build logs and reproduce in a clean Python 3.11 environment |
| Space shows configuration warning | Secret not set or restart pending | Add secret and restart/rebuild Space |
| Git push rejected | Wrong remote/auth or protected branch | Verify remote, token, and branch rules |
| GitHub large-file error | Dataset/checkpoint committed | Remove from history; use `.gitignore`, Git LFS, or a model repository |
| Port unavailable locally | Another process uses 7860 | Set `PORT=7861` in `.env` |
| Docker cannot read secret | `.env` missing | Copy `.env.example` to `.env` and add the key |
| API key exposed | Key appears in screenshot/chat/commit | Revoke/rotate immediately and remove it from history |

## Diagnostic sequence

```bash
python scripts/preflight.py --require-key
python scripts/check_secrets.py
pytest
python scripts/smoke_test.py
python scripts/live_inference_test.py
python app.py
```

Run these in order. The first failing step narrows the problem.
