"""Environment-backed configuration for local and Render deployment."""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env", override=False)

# Current Roboflow trained-model IDs can contain two or three path segments,
# for example "workspace/model-slug" or "workspace/project/version".
_MODEL_ID_PATTERN = re.compile(
    r"^[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+){1,2}$"
)
_SECRET_PLACEHOLDERS = {
    "",
    "YOUR_PRIVATE_KEY",
    "YOUR_NEW_PRIVATE_KEY",
    "PASTE_YOUR_PRIVATE_KEY_HERE",
    "CHANGEME",
    "PLACEHOLDER",
}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return default if value in (None, "") else int(value)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return default if value in (None, "") else float(value)


def _parse_class_map() -> dict[int, str]:
    raw = os.getenv("ROBOFLOW_CLASS_MAP", '{"0":"crop","1":"weed"}')
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("ROBOFLOW_CLASS_MAP must be valid JSON.") from exc

    if not isinstance(payload, dict) or not payload:
        raise ValueError("ROBOFLOW_CLASS_MAP must be a non-empty JSON object.")

    result: dict[int, str] = {}
    for raw_id, raw_name in payload.items():
        class_id = int(raw_id)
        class_name = str(raw_name).strip().lower()
        if not class_name:
            raise ValueError("ROBOFLOW_CLASS_MAP contains an empty class name.")
        result[class_id] = class_name
    return result


def _secret_is_configured(value: str) -> bool:
    normalized = value.strip().strip("\"'").upper()
    if normalized in _SECRET_PLACEHOLDERS:
        return False
    return not normalized.startswith(("YOUR_", "PASTE_"))


@dataclass(frozen=True, slots=True)
class Settings:
    """Validated runtime settings.

    The private Roboflow API key is never included in :meth:`public_summary`.
    """

    app_name: str
    app_version: str
    port: int
    server_name: str

    roboflow_api_url: str
    roboflow_api_key: str
    roboflow_model_id: str
    class_map: dict[int, str]

    default_confidence: float
    default_iou: float
    max_detections: int
    max_upload_mb: int
    max_image_pixels: int
    max_image_side: int
    rate_limit_requests: int
    rate_limit_window_seconds: int

    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables and validate them."""
        settings = cls(
            app_name=os.getenv("APP_NAME", "AgroVision AI").strip(),
            app_version=os.getenv("APP_VERSION", "1.1.0").strip(),
            port=_env_int("PORT", 7860),
            server_name=os.getenv("SERVER_NAME", "0.0.0.0").strip(),
            roboflow_api_url=os.getenv(
                "ROBOFLOW_API_URL",
                "https://serverless.roboflow.com",
            ).strip(),
            roboflow_api_key=os.getenv("ROBOFLOW_API_KEY", "").strip(),
            roboflow_model_id=os.getenv(
                "ROBOFLOW_MODEL_ID",
                "vaibhav-admane/crop-or-weed-detection-jnmzz-1-yolo11n-t1",
            ).strip(),
            class_map=_parse_class_map(),
            default_confidence=_env_float("MODEL_CONFIDENCE", 0.50),
            default_iou=_env_float("MODEL_IOU", 0.50),
            max_detections=_env_int("MAX_DETECTIONS", 100),
            max_upload_mb=_env_int("MAX_UPLOAD_MB", 10),
            max_image_pixels=_env_int("MAX_IMAGE_PIXELS", 25_000_000),
            max_image_side=_env_int("MAX_IMAGE_SIDE", 8_000),
            rate_limit_requests=_env_int("RATE_LIMIT_REQUESTS", 30),
            rate_limit_window_seconds=_env_int("RATE_LIMIT_WINDOW_SECONDS", 60),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        """Raise ``ValueError`` when a setting is unsafe or malformed."""
        if not self.app_name:
            raise ValueError("APP_NAME cannot be empty.")
        if not 1 <= self.port <= 65_535:
            raise ValueError("PORT must be between 1 and 65535.")
        if not self.server_name:
            raise ValueError("SERVER_NAME cannot be empty.")
        if not self.roboflow_api_url.startswith("https://"):
            raise ValueError("ROBOFLOW_API_URL must use HTTPS.")
        if not _MODEL_ID_PATTERN.fullmatch(self.roboflow_model_id):
            raise ValueError(
                "ROBOFLOW_MODEL_ID must look like 'workspace/model-slug' "
                "or 'workspace/project/version'."
            )

        for name, value in {
            "MODEL_CONFIDENCE": self.default_confidence,
            "MODEL_IOU": self.default_iou,
        }.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1.")

        if self.max_detections < 1:
            raise ValueError("MAX_DETECTIONS must be at least 1.")
        if self.max_upload_mb < 1:
            raise ValueError("MAX_UPLOAD_MB must be positive.")
        if self.max_image_pixels < 1 or self.max_image_side < 1:
            raise ValueError("Image limits must be positive.")
        if self.rate_limit_requests < 1 or self.rate_limit_window_seconds < 1:
            raise ValueError("Rate-limit values must be positive integers.")

    @property
    def inference_configured(self) -> bool:
        """Return whether a non-placeholder private key is configured."""
        return _secret_is_configured(self.roboflow_api_key)

    def public_summary(self) -> dict[str, Any]:
        """Return configuration that is safe to show in the UI or logs."""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "deployment": "Render Web Service",
            "provider": "Roboflow Serverless Cloud API",
            "model_id": self.roboflow_model_id,
            "classes": self.class_map,
            "configured": self.inference_configured,
            "defaults": {
                "confidence": self.default_confidence,
                "iou": self.default_iou,
                "max_detections": self.max_detections,
            },
            "limits": {
                "max_upload_mb": self.max_upload_mb,
                "max_image_pixels": self.max_image_pixels,
                "max_image_side": self.max_image_side,
                "rate_limit_requests": self.rate_limit_requests,
                "rate_limit_window_seconds": self.rate_limit_window_seconds,
            },
        }
