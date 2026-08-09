# 6. Testing and Evaluation

## Automated tests

Run:

```bash
pytest
```

The suite covers:

- public configuration does not expose the API key;
- placeholder keys are not treated as valid credentials;
- invalid model IDs and thresholds are rejected;
- missing or oversized images fail safely;
- Roboflow center-format boxes convert correctly;
- unknown classes and low-confidence predictions are ignored;
- the service returns an annotated image, table, and normalized JSON;
- the Gradio application registers a public `predict` API endpoint;
- the rolling request limiter blocks bursts and recovers after its window.

These tests use a fake provider and do not spend Roboflow credits.

## Additional checks

```bash
python -m compileall -q app.py src scripts tests
python scripts/check_secrets.py
python scripts/smoke_test.py
python scripts/preflight.py --require-key
python scripts/live_inference_test.py
# Optional repeated benchmark; consumes multiple provider requests:
python scripts/benchmark_latency.py --runs 5 --warmup 1
```

The live inference and benchmark commands make real provider requests. The benchmark reports mean, p50, p95, minimum, and maximum round-trip latency.

## Object-detection metrics

### Precision

```text
Precision = TP / (TP + FP)
```

Precision answers: “Of all predicted objects, how many were correct?” It matters because a crop incorrectly detected as a weed could trigger a harmful action.

### Recall

```text
Recall = TP / (TP + FN)
```

Recall answers: “Of all real objects, how many were found?” Weed recall is important because missed weeds remain untreated.

### F1 score

```text
F1 = 2 × Precision × Recall / (Precision + Recall)
```

Using the reported aggregate precision `0.759` and recall `0.802` at the same assumed operating point gives a **derived** F1 of approximately `0.780`. This was calculated from reported values; Roboflow did not directly export it in the supplied screenshots.

### IoU

Intersection over Union measures overlap between a predicted box and a ground-truth box:

```text
IoU = area(intersection) / area(union)
```

### AP and mAP50

Average Precision is the area under the precision–recall curve for a class. `mAP50` averages AP using IoU `0.50` as the match requirement.

### mAP50–95

This stricter COCO-style metric averages AP across IoU thresholds from `0.50` to `0.95`. It rewards precise localization. The training graph visually showed a lower curve, but the exact numerical value was not exported, so this repository does not report one.

### Latency

The app measures total round-trip time from local request preparation through hosted inference and response parsing. It includes network delay and provider cold-start effects, not only neural-network execution.

## Recorded Roboflow results

| Metric | Recorded value | Source/meaning |
|---|---:|---|
| Validation mAP50/AP50 | 83.1% | Training completion summary and mAP50 class table |
| Overall precision | 75.9% | Roboflow completion summary |
| Overall recall | 80.2% | Roboflow completion summary |
| Crop AP50 (class 0) | 78.0% | Validation class AP50 table |
| Weed AP50 (class 1) | 88.0% | Validation class AP50 table |
| Derived aggregate F1 | ~78.0% | Calculated from reported precision and recall |
| Training duration | 17 minutes | Roboflow completion email |
| Exact mAP50–95 | Not exported | Do not invent |
| Crop precision/recall | Not exported | Do not invent |
| Weed precision/recall | Not exported | Do not invent |
| Confusion matrix | Not exported | Upgrade-restricted |
| Untouched independent test result | Not established | Required for stronger claims |

## Evaluation limitations

The dataset version appears to be the same approximately 1,300-image source previously audited for near-duplicate leakage and some class-label conflicts. Therefore, the displayed validation metrics are useful as a platform baseline but should not be treated as definitive real-world generalization evidence.

## Recommended future evaluation

1. Resolve label conflicts manually.
2. Group sequential or near-duplicate images before splitting.
3. Keep a final test set untouched.
4. Export raw predictions at several thresholds.
5. Calculate crop and weed precision, recall, F1, AP, and confusion matrix.
6. Review crop-as-weed and weed-as-crop errors.
7. Report p50/p95 latency and no-detection rate.
