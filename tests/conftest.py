from __future__ import annotations

import sys
from pathlib import Path

import pytest
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agrovision.config import Settings
from agrovision.schemas import BoundingBox, Detection, PredictionResult
from agrovision.service import AgroVisionService


class FakeHostedModel:
    ready = True

    def predict(self, image: Image.Image, *, confidence: float, iou: float, max_detections: int):
        width, height = image.size
        detections = (
            Detection(
                class_id=0,
                class_name="crop",
                confidence=0.91,
                bbox=BoundingBox(4, 5, min(40, width), min(42, height)),
            ),
            Detection(
                class_id=1,
                class_name="weed",
                confidence=0.82,
                bbox=BoundingBox(min(42, width - 1), 8, min(62, width), min(45, height)),
            ),
        )[:max_detections]
        return PredictionResult(
            provider="fake-roboflow",
            model_id="fake-project/1",
            image_width=width,
            image_height=height,
            latency_ms=12.34,
            detections=detections,
            confidence_threshold=confidence,
            iou_threshold=iou,
        )


@pytest.fixture()
def settings() -> Settings:
    return Settings(
        app_name="AgroVision AI",
        app_version="test",
        port=7860,
        server_name="127.0.0.1",
        roboflow_api_url="https://serverless.roboflow.com",
        roboflow_api_key="",
        roboflow_model_id="fake-project/1",
        class_map={0: "crop", 1: "weed"},
        default_confidence=0.5,
        default_iou=0.5,
        max_detections=100,
        max_upload_mb=10,
        max_image_pixels=1_000_000,
        max_image_side=2_000,
        rate_limit_requests=30,
        rate_limit_window_seconds=60,
    )


@pytest.fixture()
def service(settings: Settings) -> AgroVisionService:
    return AgroVisionService(settings, model=FakeHostedModel())


@pytest.fixture()
def sample_image() -> Image.Image:
    return Image.new("RGB", (80, 60), (72, 110, 62))
