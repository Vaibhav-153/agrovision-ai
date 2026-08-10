# 6. Testing and Evaluation

## Offline software tests

```bash
python -m compileall -q app.py src scripts tests
python scripts/check_secrets.py
python -m pytest
python scripts/smoke_test.py
```

These tests use fake predictions and do not contact Roboflow.

## Live integration test

```bash
python scripts/live_inference_test.py examples/weed_example.jpeg
```

This checks the API key, model ID, network, provider quota, response format, parsing, and JSON output.

## Latency benchmark

```bash
python scripts/benchmark_latency.py --runs 5 --warmup 1
```

This consumes real requests and reports mean, median/p50, p95, minimum, and maximum round-trip latency.

## ML evaluation metrics

- mAP50–95: primary model-comparison metric.
- mAP50: easier detection-quality metric.
- weed recall: important for missed weeds.
- crop precision: important for avoiding crop-as-weed actions.
- confusion matrix: shows crop/weed mistakes.
- latency: important for user experience and automation.

## Suggested manual test set

Test at least:

- one clear crop;
- one clear weed;
- mixed crop/weed image;
- small weeds;
- overlap;
- low light;
- blur;
- shadows;
- background vegetation;
- images from a different farm or camera.

Record results instead of relying only on three bundled examples.
