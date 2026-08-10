"""Roboflow Serverless inference adapter and response normalization."""
from __future__ import annotations

import logging
import threading
import time
from typing import Any, Iterable, Protocol

from PIL import Image

from .config import Settings
from .errors import ConfigurationError, InferenceServiceError
from .image_utils import temporary_jpeg
from .schemas import BoundingBox, Detection, PredictionResult

LOGGER = logging.getLogger(__name__)


class _ClientProtocol(Protocol):
    def use_configuration(self, configuration: Any): ...

    def infer(self, inference_input: str, model_id: str) -> Any: ...


def find_prediction_payload(value: Any) -> dict[str, Any] | None:
    """Find an object-detection payload in direct or nested provider output."""
    if isinstance(value, dict):
        if isinstance(value.get("predictions"), list):
            return value
        for nested in value.values():
            found = find_prediction_payload(nested)
            if found is not None:
                return found
    elif isinstance(value, list):
        for nested in value:
            found = find_prediction_payload(nested)
            if found is not None:
                return found
    return None


def _normalise_class(
    prediction: dict[str, Any], class_map: dict[int, str]
) -> tuple[int, str] | None:
    raw_id = prediction.get("class_id")
    raw_name = prediction.get("class")

    class_id: int | None = None
    try:
        if raw_id is not None:
            class_id = int(raw_id)
        elif raw_name is not None and str(raw_name).strip().isdigit():
            class_id = int(str(raw_name).strip())
    except (TypeError, ValueError):
        class_id = None

    if class_id is not None and class_id in class_map:
        return class_id, class_map[class_id]

    text = str(raw_name).strip().lower() if raw_name is not None else ""
    reverse = {name.lower(): key for key, name in class_map.items()}
    if text in reverse:
        return reverse[text], text
    return None


def parse_predictions(
    payload: dict[str, Any],
    *,
    image_width: int,
    image_height: int,
    confidence_threshold: float,
    max_detections: int,
    class_map: dict[int, str],
) -> tuple[Detection, ...]:
    """Convert Roboflow center-format boxes into application detections."""
    detections: list[Detection] = []
    raw_predictions: Iterable[Any] = payload.get("predictions", []) or []

    for raw in raw_predictions:
        if not isinstance(raw, dict):
            continue
        class_info = _normalise_class(raw, class_map)
        if class_info is None:
            continue
        try:
            score = float(raw["confidence"])
            center_x = float(raw["x"])
            center_y = float(raw["y"])
            box_width = float(raw["width"])
            box_height = float(raw["height"])
        except (KeyError, TypeError, ValueError):
            continue

        if score < confidence_threshold or box_width <= 0 or box_height <= 0:
            continue

        class_id, class_name = class_info
        x1 = max(0.0, center_x - box_width / 2.0)
        y1 = max(0.0, center_y - box_height / 2.0)
        x2 = min(float(image_width), center_x + box_width / 2.0)
        y2 = min(float(image_height), center_y + box_height / 2.0)
        if x2 <= x1 or y2 <= y1:
            continue

        detections.append(
            Detection(
                class_id=class_id,
                class_name=class_name,
                confidence=round(score, 6),
                bbox=BoundingBox(
                    x1=round(x1, 2),
                    y1=round(y1, 2),
                    x2=round(x2, 2),
                    y2=round(y2, 2),
                ),
            )
        )

    detections.sort(key=lambda item: item.confidence, reverse=True)
    return tuple(detections[:max_detections])


class RoboflowHostedModel:
    """Lazy client for the private hosted YOLO11 Nano model."""

    provider_name = "roboflow-serverless"

    def __init__(
        self,
        settings: Settings,
        *,
        client: _ClientProtocol | None = None,
        configuration_factory: Any | None = None,
    ) -> None:
        self.settings = settings
        self._client = client
        self._configuration_factory = configuration_factory
        self._lock = threading.Lock()

    @property
    def ready(self) -> bool:
        return self.settings.inference_configured or self._client is not None

    def _ensure_client(self) -> tuple[_ClientProtocol, Any]:
        if self._client is not None and self._configuration_factory is not None:
            return self._client, self._configuration_factory
        if not self.settings.inference_configured:
            raise ConfigurationError(
                "Roboflow inference is not configured. Add ROBOFLOW_API_KEY to "
                "your local .env file or the Render environment settings."
            )
        try:
            from inference_sdk import InferenceConfiguration, InferenceHTTPClient
        except ImportError as exc:
            raise ConfigurationError(
                "inference-sdk is not installed. Run pip install -r requirements.txt."
            ) from exc

        self._client = InferenceHTTPClient(
            api_url=self.settings.roboflow_api_url,
            api_key=self.settings.roboflow_api_key,
        )
        self._configuration_factory = InferenceConfiguration
        return self._client, self._configuration_factory

    def predict(
        self,
        image: Image.Image,
        *,
        confidence: float,
        iou: float,
        max_detections: int,
    ) -> PredictionResult:
        client, configuration_factory = self._ensure_client()
        configuration = configuration_factory(
            confidence_threshold=confidence,
            iou_threshold=iou,
            max_detections=max_detections,
            disable_active_learning=True,
            source="agrovision-render",
        )

        width, height = image.size
        started = time.perf_counter()
        try:
            with temporary_jpeg(image) as path:
                with self._lock:
                    with client.use_configuration(configuration):
                        raw_result = client.infer(
                            str(path), model_id=self.settings.roboflow_model_id
                        )
        except ConfigurationError:
            raise
        except Exception as exc:
            LOGGER.warning("Roboflow inference failed: %s", type(exc).__name__)
            raise InferenceServiceError(
                "The hosted model could not process this image. Check your key, model ID, "
                "Roboflow credits, and network connection, then retry."
            ) from exc

        payload = find_prediction_payload(raw_result)
        if payload is None:
            raise InferenceServiceError(
                "Roboflow returned a response without object-detection predictions."
            )

        detections = parse_predictions(
            payload,
            image_width=width,
            image_height=height,
            confidence_threshold=confidence,
            max_detections=max_detections,
            class_map=self.settings.class_map,
        )
        latency_ms = (time.perf_counter() - started) * 1000.0
        return PredictionResult(
            provider=self.provider_name,
            model_id=self.settings.roboflow_model_id,
            image_width=width,
            image_height=height,
            latency_ms=latency_ms,
            detections=detections,
            confidence_threshold=confidence,
            iou_threshold=iou,
            class_names=tuple(self.settings.class_map.values()),
        )
