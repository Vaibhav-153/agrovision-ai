# Hugging Face Space settings

## Secret

Create this under **Space → Settings → Variables and secrets → New secret**:

| Name | Value |
|---|---|
| `ROBOFLOW_API_KEY` | Your newly rotated private Roboflow API key |

Never add the key as a normal variable because normal variables may be visible in Space configuration.

## Optional variables

| Name | Recommended value |
|---|---|
| `ROBOFLOW_MODEL_ID` | `crop-or-weed-detection-jnmzz-1-yolo11n-t1/1` |
| `ROBOFLOW_API_URL` | `https://serverless.roboflow.com` |
| `ROBOFLOW_CLASS_MAP` | `{"0":"crop","1":"weed"}` |
| `MODEL_CONFIDENCE` | `0.50` |
| `MODEL_IOU` | `0.50` |
| `MAX_DETECTIONS` | `100` |
| `MAX_UPLOAD_MB` | `10` |
| `RATE_LIMIT_REQUESTS` | `30` |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` |

The app reads each setting from the process environment. The secret is never returned by the UI.
