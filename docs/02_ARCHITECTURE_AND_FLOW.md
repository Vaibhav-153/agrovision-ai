# 2. Architecture and Data Flow

![Architecture](../assets/architecture.svg)

## Deployment architecture

```text
User browser
   │
   │ image + confidence + IoU + max detections
   ▼
Hugging Face Gradio Space / local Python process
   │
   ├─ validate input and limits
   ├─ correct EXIF orientation
   ├─ convert to RGB
   └─ create a fresh temporary JPEG without metadata
   │
   ▼
Roboflow Serverless Cloud API
   │
   ▼
Private YOLO11 Nano model
   │
   │ center-format boxes + class + confidence
   ▼
AgroVision post-processing
   │
   ├─ map 0 → crop, 1 → weed
   ├─ filter by confidence
   ├─ clamp boxes to image boundaries
   ├─ sort and limit detections
   └─ calculate counts and latency
   │
   ▼
Annotated image + table + KPI cards + JSON
```

## Internal pipeline step by step

### 1. User input

`gr.Image(type="pil")` provides a Pillow image. The user also selects confidence, IoU, and maximum detections.

### 2. Validation

`validate_image()` checks that an image exists, Pillow can decode it, dimensions are positive, the longest side is within the configured limit, and total pixels do not exceed the safety limit.

### 3. Privacy-oriented preprocessing

`ImageOps.exif_transpose()` applies camera orientation. Converting to RGB and saving a new temporary JPEG removes EXIF/GPS metadata from the file sent to the hosted model.

### 4. Model request

`RoboflowHostedModel` lazily creates `InferenceHTTPClient`. The client uses `InferenceConfiguration` for confidence, IoU, maximum detections, and disabled active-learning upload. The private key is read from the server environment.

### 5. YOLO inference

Roboflow runs the YOLO11 Nano checkpoint on managed infrastructure. The local or Hugging Face CPU does not execute the neural network.

### 6. Post-processing

Roboflow returns object predictions using box center, width, and height. `parse_predictions()` converts each box to corner coordinates, maps the class, filters malformed/unknown results, clamps coordinates, and sorts by confidence.

### 7. Visualization

`annotate_image()` draws class-specific boxes and labels using Pillow. Crop boxes are green; weed boxes are orange.

### 8. UI result

The application displays the annotated image, crop/weed counts, average confidence, round-trip latency, detection table, and normalized JSON.

## Trust boundaries

- **Browser:** receives images and results, never the private key.
- **Space/backend:** holds the key in an environment variable and prepares the request.
- **Roboflow:** receives the sanitized image for hosted inference.
- **Repository:** contains configuration names and model ID but no private credentials.
