"""Application service that connects validation, inference, and visualization."""
from __future__ import annotations

from typing import Any

from PIL import Image

from .config import Settings
from .image_utils import validate_image, validate_max_detections, validate_threshold
from .roboflow import RoboflowHostedModel
from .schemas import PredictionResult
from .visualization import annotate_image, result_summary_html


class AgroVisionService:
    """High-level prediction service used by the Gradio UI and tests."""

    def __init__(
        self,
        settings: Settings,
        *,
        model: RoboflowHostedModel | Any | None = None,
    ) -> None:
        self.settings = settings
        self.model = model or RoboflowHostedModel(settings)

    def analyze(
        self,
        image: Image.Image | None,
        confidence: float,
        iou: float,
        max_detections: int,
    ) -> tuple[Image.Image, str, list[list[Any]], dict[str, Any]]:
        clean_image = validate_image(
            image,
            max_pixels=self.settings.max_image_pixels,
            max_side=self.settings.max_image_side,
        )
        confidence = validate_threshold("Confidence threshold", confidence)
        iou = validate_threshold("IoU threshold", iou)
        max_detections = validate_max_detections(
            max_detections, self.settings.max_detections
        )

        result: PredictionResult = self.model.predict(
            clean_image,
            confidence=confidence,
            iou=iou,
            max_detections=max_detections,
        )
        annotated = annotate_image(clean_image, result)
        table = [
            detection.to_table_row(index)
            for index, detection in enumerate(result.detections, start=1)
        ]
        return annotated, result_summary_html(result), table, result.to_dict()
