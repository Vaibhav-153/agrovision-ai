# 3. Model, Algorithm, Parameters, and Training Charts

## Which algorithm was used?

The project uses **YOLO11 Nano**, written as **YOLO11n**.

YOLO means **You Only Look Once**. It is a one-stage object detector. In simple terms:

1. the model reads the image;
2. a feature-extraction network learns shapes, edges, textures, and plant patterns;
3. features from different image scales are combined so both small and large plants can be detected;
4. the detection head predicts boxes, object presence, and crop/weed class scores;
5. non-maximum suppression removes repeated overlapping boxes.

The Nano version is the smallest YOLO11 variant. It was selected because it is fast and practical for a portfolio project. Larger variants may improve accuracy but require more compute and should be compared experimentally.

## Transfer learning

Training did not begin from random weights. It began from a public **MS COCO checkpoint**. This is transfer learning:

- the checkpoint already understands general visual patterns;
- crop/weed training adapts those features to agriculture;
- training is faster and usually more stable than random initialization.

## Known training facts

- Platform: Roboflow.
- Architecture: YOLO11 object detection.
- Size: Nano.
- Starting checkpoint: MS COCO public checkpoint.
- Classes: crop and weed.
- Dataset size shown in Roboflow: about 1,300 images.
- Training duration: 17 minutes.

The exact optimizer, learning rate, batch size, augmentation settings, and selected checkpoint epoch were not exported. They are unknown in this repository.

## Metrics

### Precision

Precision answers: **When the model reports an object, how often is it correct?**

```text
Precision = true positives / (true positives + false positives)
```

Recorded value: **75.9%**.

### Recall

Recall answers: **Of all labelled objects, how many did the model find?**

```text
Recall = true positives / (true positives + false negatives)
```

Recorded value: **80.2%**.

### F1 score

F1 balances precision and recall.

```text
F1 = 2 × precision × recall / (precision + recall)
```

Derived from the recorded values: **about 78.0%**.

### mAP50

mAP50 measures average precision when a predicted box counts as correct at IoU 0.50. Recorded value: **83.1%**.

### mAP50–95

mAP50–95 averages performance over IoU thresholds from 0.50 to 0.95. It is stricter and should be the primary model-comparison metric. The supplied chart shows **0.5155 at epoch 135**.

## Training charts

### Model performance — higher is better

![Model performance](../assets/training_charts/model_performance.png)

- Dark purple: mAP50-style score.
- Light purple: mAP50–95.
- Rapid early improvement means the model learned quickly.
- The plateau means additional epochs produced smaller improvements.
- The visible strict peak near epoch 135 is more useful than simply using the final epoch.

### Box loss — lower is better

![Box loss](../assets/training_charts/box_loss.png)

This measures box-position error. It falls from about 2.9 to about 1.2–1.3, indicating better localization.

### Class loss — lower is better

![Class loss](../assets/training_charts/class_loss.png)

This measures crop/weed classification error. It falls from about 3.7 to about 0.8–0.9.

### Object loss — lower is better

![Object loss](../assets/training_charts/object_loss.png)

This measures whether the model detects object presence. It falls from about 3.8 to about 1.6–1.8. A small late rise suggests training had mostly converged.

## Which result is best?

For checkpoint selection:

1. highest validation mAP50–95;
2. strong weed recall;
3. strong crop precision;
4. low crop/weed confusion;
5. acceptable latency.

Do not choose a checkpoint only because its training loss is lowest.

## Inference parameters used by the website

| Parameter | Default | Lower value | Higher value |
|---|---:|---|---|
| Confidence | 0.50 | More detections, more false positives possible | Fewer, stronger detections |
| IoU | 0.50 | More aggressive duplicate suppression | Keeps more nearby boxes |
| Maximum detections | 50 in UI | Smaller output | More boxes and larger response |

These parameters change prediction filtering; they do not retrain the model.
