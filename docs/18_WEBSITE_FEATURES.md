# 18. Website Features

## Header

Shows the project name, task, YOLO11n model, and two supported classes.

## Model connection status

Shows whether a private Roboflow key is configured and displays the safe model ID. The key itself is never shown.

## Input image

Supports upload, webcam, and clipboard. The server validates and sanitizes the image before inference.

## Confidence threshold

Controls how strong a prediction must be. Lower values can find more weeds but may create more false positives. Higher values are stricter.

## IoU threshold

Controls non-maximum suppression. Lower values remove overlapping boxes more aggressively. Higher values keep more nearby boxes.

## Maximum detections

Limits the returned boxes to protect the interface and provider response size.

## Analyze field image

Runs the complete validation, inference, normalization, rendering, and output pipeline.

## Clear

Resets input, output image, summary cards, table, and JSON.

## Annotated result

Green boxes represent crop. Orange boxes represent weed. Each label includes class and confidence.

## KPI cards

- Total detections
- Crop count
- Weed count
- Average confidence
- Round-trip latency

## Detections table

Shows row number, class, confidence percentage, and corner coordinates. It is a custom output-only HTML table to keep the interface light and predictable.

## Normalized JSON

Shows structured developer output independent of the provider’s raw response format.

## Model and evaluation notes

Explains algorithm, transfer learning, classes, metrics, safety, and unavailable evidence.

## Training charts

Displays model performance, box loss, class loss, and object loss with clear higher/lower-is-better labels.

## Included examples

Provides crop, weed, and mixed/challenging samples for quick demonstration.

## Help accordions

Explain every control and the full data flow from image upload to final results.
