from __future__ import annotations

import pytest

from agrovision.errors import InputValidationError


def test_service_returns_annotated_image_table_and_json(service, sample_image):
    annotated, summary, table, payload = service.analyze(sample_image, 0.45, 0.55, 50)
    assert annotated.size == sample_image.size
    assert "Total detections" in summary
    assert len(table) == 2
    assert table[0][1] == "crop"
    assert payload["success"] is True
    assert payload["class_counts"] == {"crop": 1, "weed": 1}
    assert payload["thresholds"]["confidence"] == 0.45


def test_service_rejects_missing_image(service):
    with pytest.raises(InputValidationError):
        service.analyze(None, 0.5, 0.5, 50)


def test_service_rejects_invalid_iou(service, sample_image):
    with pytest.raises(InputValidationError):
        service.analyze(sample_image, 0.5, 2.0, 50)
