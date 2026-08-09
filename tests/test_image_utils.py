from __future__ import annotations

import pytest
from PIL import Image

from agrovision.errors import InputValidationError
from agrovision.image_utils import validate_image, validate_max_detections, validate_threshold


def test_valid_image_returns_metadata_free_rgb_copy(sample_image):
    result = validate_image(sample_image, max_pixels=100_000, max_side=1_000)
    assert result.mode == "RGB"
    assert result.size == (80, 60)
    assert result is not sample_image
    assert result.getexif() == {}


def test_missing_image_rejected():
    with pytest.raises(InputValidationError):
        validate_image(None, max_pixels=100_000, max_side=1_000)


def test_large_side_rejected():
    image = Image.new("RGB", (2_001, 10))
    with pytest.raises(InputValidationError):
        validate_image(image, max_pixels=100_000, max_side=2_000)


def test_threshold_validation():
    assert validate_threshold("confidence", 0.5) == 0.5
    with pytest.raises(InputValidationError):
        validate_threshold("confidence", 1.1)


def test_max_detections_validation():
    assert validate_max_detections(10, 100) == 10
    with pytest.raises(InputValidationError):
        validate_max_detections(101, 100)
