"""Image validation, orientation correction, and temporary serialization."""
from __future__ import annotations

import contextlib
import tempfile
from pathlib import Path
from typing import Iterator

from PIL import Image, ImageOps

from .errors import InputValidationError


def validate_image(
    image: Image.Image | None,
    *,
    max_pixels: int,
    max_side: int,
) -> Image.Image:
    """Validate a Gradio/Pillow image and return a metadata-free RGB copy."""
    if image is None:
        raise InputValidationError("Upload a crop or weed image before running prediction.")
    if not isinstance(image, Image.Image):
        raise InputValidationError("The uploaded input is not a supported image.")

    try:
        image.load()
        oriented = ImageOps.exif_transpose(image)
    except Exception as exc:  # Pillow can raise several decoder-specific errors.
        raise InputValidationError("The image is corrupt or could not be decoded.") from exc

    width, height = oriented.size
    if width < 1 or height < 1:
        raise InputValidationError("The image has invalid dimensions.")
    if max(width, height) > max_side:
        raise InputValidationError(
            f"The image is too large. Maximum side length is {max_side:,} pixels."
        )
    if width * height > max_pixels:
        raise InputValidationError(
            f"The image contains too many pixels. Maximum is {max_pixels:,}."
        )

    # Converting and copying removes EXIF/GPS metadata from the image that is sent
    # to the hosted inference service.
    return oriented.convert("RGB").copy()


def validate_threshold(name: str, value: float) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise InputValidationError(f"{name} must be a number.") from exc
    if not 0.0 <= numeric <= 1.0:
        raise InputValidationError(f"{name} must be between 0 and 1.")
    return numeric


def validate_max_detections(value: int, configured_max: int) -> int:
    try:
        numeric = int(value)
    except (TypeError, ValueError) as exc:
        raise InputValidationError("Maximum detections must be an integer.") from exc
    if not 1 <= numeric <= configured_max:
        raise InputValidationError(
            f"Maximum detections must be between 1 and {configured_max}."
        )
    return numeric


@contextlib.contextmanager
def temporary_jpeg(image: Image.Image) -> Iterator[Path]:
    """Write a sanitized image to a temporary JPEG and always remove it."""
    path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as handle:
            path = Path(handle.name)
        image.save(path, format="JPEG", quality=92, optimize=True)
        yield path
    finally:
        if path is not None:
            path.unlink(missing_ok=True)
