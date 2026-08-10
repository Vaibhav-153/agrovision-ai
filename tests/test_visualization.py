from __future__ import annotations

from agrovision.schemas import BoundingBox, Detection, PredictionResult
from agrovision.visualization import detection_table_html


def test_detection_table_uses_light_theme_custom_markup() -> None:
    result = PredictionResult(
        provider="fake",
        model_id="workspace/model",
        image_width=100,
        image_height=80,
        latency_ms=10.0,
        detections=(
            Detection(
                class_id=0,
                class_name="crop",
                confidence=0.91,
                bbox=BoundingBox(1, 2, 20, 30),
            ),
        ),
        confidence_threshold=0.5,
        iou_threshold=0.5,
    )
    html = detection_table_html(result)
    assert 'class="detection-table"' in html
    assert "91.00%" in html
    assert "crop" in html
    assert "Sort ascending" not in html


def test_empty_detection_table_has_clear_message() -> None:
    html = detection_table_html()
    assert "No detections to display" in html
