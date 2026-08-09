# 11. Viva and Interview Questions

## 1. What is AgroVision AI?

It is a two-class object-detection application that identifies and localizes crops and weeds in field images.

## 2. Why is this object detection instead of classification?

Classification gives one label for an entire image. Object detection returns multiple labels and bounding boxes, which is required when several plants appear in one image.

## 3. Which model is used?

A YOLO11 Nano object detector fine-tuned on Roboflow for `crop` and `weed` classes.

## 4. What is the model ID?

`crop-or-weed-detection-jnmzz-1-yolo11n-t1/1`.

## 5. Why was YOLO11 Nano selected?

It was the model actually trained and evaluated, and it offers a practical speed/resource tradeoff. Larger variants were not substituted without controlled evidence.

## 6. What is a pre-trained checkpoint?

It is a set of weights learned on a source dataset. The project started from an MS COCO checkpoint instead of random initialization.

## 7. What is transfer learning?

Transfer learning adapts features learned on one dataset/task to a new task, reducing data and compute requirements.

## 8. What are the classes?

Class `0` is `crop`; class `1` is `weed`.

## 9. What does confidence mean?

It is the model's score for a specific detection. It is not a calibrated probability guarantee.

## 10. What happens when confidence threshold increases?

The system returns fewer, stricter detections. Precision may improve while recall may decrease.

## 11. What is IoU?

Intersection over Union measures overlap between two boxes: intersection area divided by union area.

## 12. How is IoU used in this application?

It controls non-maximum suppression, which removes overlapping duplicate predictions.

## 13. What is precision?

Precision is `TP / (TP + FP)`. It measures how many predicted detections are correct.

## 14. What is recall?

Recall is `TP / (TP + FN)`. It measures how many real objects are found.

## 15. Why is weed recall important?

Low weed recall means many weeds are missed, limiting the value of the system for weed monitoring.

## 16. Why is crop precision important?

Poor crop precision or crop-as-weed confusion can be dangerous in automated treatment systems.

## 17. What is mAP50?

Mean Average Precision calculated with IoU 0.50 as the match threshold, averaged across classes.

## 18. Why is mAP50–95 stricter?

It averages AP over IoU thresholds from 0.50 to 0.95 and therefore demands more accurate localization.

## 19. What measured results are available?

Roboflow reported validation mAP50/AP50 around 83.1%, precision 75.9%, recall 80.2%, crop AP50 78%, and weed AP50 88%.

## 20. Which important results are unavailable?

Exact mAP50–95, per-class precision/recall, confusion matrix, and an independently verified untouched test-set result.

## 21. Why is the API key not placed in JavaScript?

Frontend JavaScript is visible to users. A private key there would be immediately exposed and abused.

## 22. How is the key protected on Hugging Face?

It is stored as a Space Secret and read as a server-side environment variable.

## 23. How does the app protect image privacy?

It applies orientation, converts to RGB, and creates a new JPEG without EXIF/GPS metadata before sending the image to Roboflow. Images still leave the Space for cloud inference, so users must be informed.

## 24. Why can the Hugging Face Space use CPU hardware?

The Space performs UI and image processing; Roboflow runs the neural network remotely.

## 25. What are the disadvantages of hosted inference?

Internet dependency, provider latency, quotas/credits, third-party data processing, and reduced control over weights and low-level optimization.

## 26. What would change if `best.pt` became available?

A local provider could load the checkpoint with Ultralytics, eliminating the hosted API dependency but increasing CPU/GPU, memory, and deployment requirements.

## 27. How are tests run without spending credits?

The test suite injects a fake hosted model and uses synthetic predictions.

## 28. What is a cold start?

It is additional latency when a serverless service initializes resources after inactivity.

## 29. How would you scale the application?

Add request queues, provider quota monitoring, caching where appropriate, stricter rate limits, observability, and a dedicated or self-hosted inference deployment for predictable traffic.

## 30. What is the biggest scientific limitation?

The current dataset may contain near-duplicate leakage and label conflicts, so stronger evaluation on a cleaned, grouped, untouched test set is required.

## 31. Why should confidence not always be fixed at 0.5?

The best operating threshold depends on the cost of false positives and false negatives. It should be selected using validation predictions.

## 32. How would you improve generalization?

Clean labels, prevent sequence leakage, add diverse field conditions, review hard failures, compare model sizes/resolutions, and evaluate on independent farms/sessions.

## 33. What is Gradio's role?

It provides the web UI, file handling, event wiring, queue, and generated API endpoint.

## 34. What is the role of Pillow?

It decodes, validates, converts, sanitizes, and annotates images.

## 35. Why use GitHub Actions?

It automatically compiles code, scans for hard-coded keys, runs tests, and checks that the UI can be built before changes are merged.
