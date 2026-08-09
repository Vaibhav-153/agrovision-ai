# 10. Study Notes

## What problem are we solving?

We are detecting and localizing crops and weeds in agricultural images. This requires object detection because one image may contain multiple objects at different positions.

## Why use a pre-trained model?

Training a detector from random initialization requires more data and compute. A COCO-pretrained checkpoint already contains general visual features such as edges, textures, shapes, and object boundaries. Fine-tuning adapts those features to crop and weed classes.

## What is transfer learning?

Transfer learning starts from weights learned on a large source dataset and updates them for a new target task. Here, the source checkpoint is MS COCO and the target classes are crop and weed.

## Why YOLO?

YOLO performs detection in a single forward pass and is widely used for real-time applications. The Nano model favors speed and low resource use. That does not automatically mean it is the most accurate; larger variants must be evaluated before making that claim.

## How does preprocessing work?

The app decodes the image, corrects orientation, validates size, converts it to RGB, and writes a fresh JPEG. This standardizes input and removes metadata before the image leaves the application server.

## How does inference work?

The backend sends the temporary image to Roboflow with model ID and thresholds. Roboflow runs the trained detector and returns boxes/classes/confidences. The app does not possess the model weights.

## How is output generated?

Each center-format box is converted to corner coordinates. Class IDs become human-readable names. Boxes are drawn with class-specific colors. Counts and average confidence are calculated from the final detections.

## Important libraries

- **Gradio:** builds the web interface and API endpoint.
- **Pillow:** decodes, validates, sanitizes, and annotates images.
- **inference-sdk:** communicates with Roboflow hosted inference.
- **python-dotenv:** loads local environment variables from `.env`.
- **pytest:** tests behavior without provider calls.

## Evaluation strategy

Object-detection evaluation should emphasize mAP50–95, class precision/recall, F1, confusion matrix, and latency. For this use case, weed recall and crop precision are particularly important.

## Advantages

- no local GPU required for deployment;
- clean secret management;
- simple Hugging Face hosting;
- modular response normalization;
- testable without API usage;
- clear measured-versus-unavailable metrics.

## Limitations

- internet and Roboflow availability required;
- provider credits/quotas apply;
- no downloadable model weights in the current plan;
- exact mAP50–95 and confusion matrix unavailable;
- possible duplicate/leakage issues in the underlying dataset;
- field conditions beyond the training distribution may reduce performance.

## Resume wording

> Built and deployed AgroVision AI, a two-class crop/weed object-detection application using a COCO-pretrained YOLO11 Nano model trained and hosted on Roboflow. Implemented secure server-side inference, image validation and metadata removal, configurable confidence/IoU controls, bounding-box visualization, normalized prediction APIs, automated tests, GitHub CI, Docker support, and Hugging Face Spaces deployment.

Add metric values only with the qualifier “Roboflow validation” and do not describe them as independent real-world test results.
