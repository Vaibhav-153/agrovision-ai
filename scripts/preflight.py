"""Check the local environment before running or deploying AgroVision AI."""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from agrovision.config import Settings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-key", action="store_true", help="Fail if ROBOFLOW_API_KEY is missing.")
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []

    if sys.version_info < (3, 11) or sys.version_info >= (3, 13):
        failures.append("Use Python 3.11 or 3.12 for the pinned deployment stack.")

    for module in ("gradio", "PIL", "dotenv"):
        try:
            importlib.import_module(module)
        except ImportError:
            failures.append(f"Missing package: {module}. Run pip install -r requirements.txt.")

    try:
        importlib.import_module("inference_sdk")
    except ImportError:
        warnings.append("inference-sdk is unavailable in this environment; live Roboflow calls will fail.")

    try:
        settings = Settings.from_env()
    except Exception as exc:
        failures.append(f"Configuration error: {exc}")
        settings = None

    if settings is not None and not settings.inference_configured:
        message = "ROBOFLOW_API_KEY is not configured. The UI can start, but prediction cannot run."
        if args.require_key:
            failures.append(message)
        else:
            warnings.append(message)

    for relative in (
        "app.py",
        "requirements.txt",
        "assets/custom.css",
        "examples/crop_example.jpeg",
        "examples/weed_example.jpeg",
        "examples/mixed_example.jpeg",
    ):
        if not (ROOT / relative).is_file():
            failures.append(f"Required file missing: {relative}")

    print("AgroVision AI preflight")
    print(f"Python: {sys.version.split()[0]}")
    if settings is not None:
        public = settings.public_summary()
        print(f"Model: {public['model_id']}")
        print(f"Inference configured: {public['configured']}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for failure in failures:
        print(f"ERROR: {failure}")

    if failures:
        return 1
    print("Preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
