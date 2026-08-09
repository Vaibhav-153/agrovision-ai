# 16. API Usage

The Gradio event is registered with `api_name="predict"`. After deployment, open the Space and choose **Use via API** to copy client code for the exact generated schema.

## Python client pattern

Install:

```bash
pip install gradio_client
```

Example:

```python
from gradio_client import Client, handle_file

client = Client("YOUR_HF_USERNAME/agrovision-ai")
result = client.predict(
    image=handle_file("field.jpg"),
    confidence=0.50,
    iou=0.50,
    max_detections=50,
    api_name="/predict",
)
print(result)
```

The output contains:

1. annotated image file/result;
2. HTML KPI summary;
3. detection table;
4. normalized JSON.

## Normalized JSON contract

```json
{
  "success": true,
  "provider": "roboflow-serverless",
  "model_id": "crop-or-weed-detection-jnmzz-1-yolo11n-t1/1",
  "image_width": 1280,
  "image_height": 720,
  "latency_ms": 850.2,
  "count": 2,
  "class_counts": {
    "crop": 1,
    "weed": 1
  },
  "average_confidence": 0.86,
  "thresholds": {
    "confidence": 0.5,
    "iou": 0.5
  },
  "detections": [
    {
      "class_id": 1,
      "class_name": "weed",
      "confidence": 0.91,
      "bbox": {
        "x1": 100.0,
        "y1": 80.0,
        "x2": 250.0,
        "y2": 300.0
      }
    }
  ]
}
```

The numbers above illustrate the schema; they are not a measured prediction from the bundled example images.
