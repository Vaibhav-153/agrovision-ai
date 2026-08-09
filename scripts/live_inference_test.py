"""Run one real hosted prediction after the private key is configured."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from agrovision.config import Settings
from agrovision.service import AgroVisionService


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image",
        nargs="?",
        default=str(ROOT / "examples" / "weed_example.jpeg"),
        help="Path to an image used for the live API test.",
    )
    parser.add_argument("--confidence", type=float, default=None)
    parser.add_argument("--iou", type=float, default=None)
    args = parser.parse_args()

    settings = Settings.from_env()
    if not settings.inference_configured:
        print("ROBOFLOW_API_KEY is missing. Add it to .env or the hosting secret store.")
        return 2

    image_path = Path(args.image).expanduser().resolve()
    if not image_path.is_file():
        print(f"Image not found: {image_path}")
        return 2

    image = Image.open(image_path)
    service = AgroVisionService(settings)
    _, _, _, payload = service.analyze(
        image,
        args.confidence if args.confidence is not None else settings.default_confidence,
        args.iou if args.iou is not None else settings.default_iou,
        min(50, settings.max_detections),
    )
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
