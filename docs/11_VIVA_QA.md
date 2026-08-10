# 11. Viva and Interview Questions

## 1. What problem does AgroVision AI solve?
It detects and localizes crops and weeds in agricultural images.

## 2. Is this classification or object detection?
Object detection, because it returns a class and a bounding box for each object.

## 3. Which algorithm is used?
YOLO11 Nano, a one-stage object detector.

## 4. What does YOLO mean?
You Only Look Once.

## 5. Why use the Nano model?
It is small and fast, making it practical for a portfolio application.

## 6. What is transfer learning?
Starting from a model that already learned general visual features and fine-tuning it on a new task.

## 7. Which checkpoint was used?
A public MS COCO checkpoint.

## 8. Which classes are detected?
Crop and weed.

## 9. What is precision?
The fraction of reported detections that are correct.

## 10. What is recall?
The fraction of labelled objects that the model finds.

## 11. Why is weed recall important?
Low weed recall means weeds are missed.

## 12. Why is crop precision important?
Poor crop precision can cause non-crop predictions to be unreliable and can contribute to dangerous crop/weed decisions.

## 13. What is IoU?
A measure of overlap between two bounding boxes.

## 14. What is mAP50?
Average precision measured using IoU 0.50.

## 15. Why is mAP50–95 stricter?
It averages performance across multiple IoU thresholds from 0.50 to 0.95.

## 16. What is the best checkpoint-selection metric here?
Validation mAP50–95, checked together with weed recall and crop precision.

## 17. What does box loss show?
How much error exists in predicted box locations; lower is better.

## 18. What does class loss show?
Crop-versus-weed classification error; lower is better.

## 19. What does object loss show?
Error in learning whether an object is present; lower is better.

## 20. What does confidence threshold do?
It removes detections weaker than the selected score.

## 21. What does the IoU threshold control at inference?
How aggressively overlapping duplicate boxes are suppressed.

## 22. Why is the API key not stored in code?
Hard-coded keys can leak through GitHub and browser source. Environment variables keep it server-side.

## 23. What image-security checks are performed?
Decode validation, orientation correction, dimension/pixel limits, RGB conversion, metadata removal, and temporary-file deletion.

## 24. Why can Render use CPU?
The neural network runs on Roboflow; Render handles the web app and HTTP requests.

## 25. What is a cold start?
The delay when a sleeping free Render service starts again.

## 26. Why replace Gradio Dataframe with HTML?
The table is output-only. Custom HTML is lighter, predictable, accessible, and avoids unnecessary dark spreadsheet menus.

## 27. How are Roboflow boxes converted?
Center `x, y, width, height` becomes `x1, y1, x2, y2` and is clamped to image boundaries.

## 28. How is latency measured?
From just before the provider request until the normalized response is ready.

## 29. What is the biggest scientific limitation?
The lack of a leakage-safe independent test report with per-class metrics and a confusion matrix.

## 30. How would you improve the project?
Clean the dataset, compare model sizes, optimize thresholds, measure per-class metrics, obtain local weights, and test on unseen farms.
