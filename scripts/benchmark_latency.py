"""Measure repeated live round-trip inference latency (consumes provider credits)."""
from __future__ import annotations

import argparse
import statistics
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from agrovision.config import Settings
from agrovision.service import AgroVisionService


def percentile(values: list[float], percent: float) -> float:
    """Return a linearly interpolated percentile for a non-empty list."""
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * percent
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run repeated real Roboflow requests and report latency statistics."
    )
    parser.add_argument(
        "image",
        nargs="?",
        default=str(ROOT / "examples" / "weed_example.jpeg"),
    )
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--confidence", type=float, default=None)
    parser.add_argument("--iou", type=float, default=None)
    args = parser.parse_args()

    if not 1 <= args.runs <= 100:
        parser.error("--runs must be between 1 and 100.")
    if not 0 <= args.warmup <= 20:
        parser.error("--warmup must be between 0 and 20.")

    settings = Settings.from_env()
    if not settings.inference_configured:
        print("ROBOFLOW_API_KEY is missing. Configure .env before benchmarking.")
        return 2

    image_path = Path(args.image).expanduser().resolve()
    if not image_path.is_file():
        print(f"Image not found: {image_path}")
        return 2

    with Image.open(image_path) as opened:
        image = opened.convert("RGB").copy()

    confidence = (
        args.confidence if args.confidence is not None else settings.default_confidence
    )
    iou = args.iou if args.iou is not None else settings.default_iou
    service = AgroVisionService(settings)

    print(
        f"WARNING: this will make {args.warmup + args.runs} real provider requests "
        "and may consume Roboflow credits."
    )

    for _ in range(args.warmup):
        service.analyze(image, confidence, iou, min(50, settings.max_detections))

    latencies: list[float] = []
    counts: list[int] = []
    for index in range(1, args.runs + 1):
        _, _, _, payload = service.analyze(
            image, confidence, iou, min(50, settings.max_detections)
        )
        latency = float(payload["latency_ms"])
        latencies.append(latency)
        counts.append(int(payload["count"]))
        print(f"Run {index:02d}: {latency:.2f} ms, detections={payload['count']}")

    print("\nLatency summary (round trip)")
    print(f"Runs: {len(latencies)}")
    print(f"Mean: {statistics.fmean(latencies):.2f} ms")
    print(f"Median/p50: {statistics.median(latencies):.2f} ms")
    print(f"p95: {percentile(latencies, 0.95):.2f} ms")
    print(f"Min: {min(latencies):.2f} ms")
    print(f"Max: {max(latencies):.2f} ms")
    print(f"Detection counts: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
