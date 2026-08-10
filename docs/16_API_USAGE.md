# 16. API Usage

The Gradio application registers its prediction function with:

```python
api_name="predict"
```

Open the running application and select **Use via API** to view generated client code for the deployed version.

## Inputs

1. image;
2. confidence threshold;
3. IoU threshold;
4. maximum detections.

## Outputs

1. annotated image;
2. HTML summary cards;
3. HTML detection table;
4. normalized JSON.

## JSON example shape

```json
{
  "success": true,
  "provider": "roboflow-serverless",
  "model_id": "vaibhav-admane/crop-or-weed-detection-jnmzz-1-yolo11n-t1",
  "image_width": 1280,
  "image_height": 720,
  "latency_ms": 910.0,
  "count": 1,
  "class_counts": {"crop": 1, "weed": 0},
  "average_confidence": 0.62,
  "thresholds": {"confidence": 0.5, "iou": 0.5},
  "detections": [
    {
      "class_id": 0,
      "class_name": "crop",
      "confidence": 0.62,
      "bbox": {"x1": 10, "y1": 48, "x2": 505, "y2": 419}
    }
  ]
}
```

The values above illustrate the structure. Actual values depend on the image and live model.
