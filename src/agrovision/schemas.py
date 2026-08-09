"""Typed prediction objects shared by inference, UI, and tests."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self) -> float:
        return max(0.0, self.x2 - self.x1)

    @property
    def height(self) -> float:
        return max(0.0, self.y2 - self.y1)


@dataclass(frozen=True, slots=True)
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bbox: BoundingBox

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_table_row(self, index: int) -> list[Any]:
        return [
            index,
            self.class_name,
            round(self.confidence * 100.0, 2),
            round(self.bbox.x1, 1),
            round(self.bbox.y1, 1),
            round(self.bbox.x2, 1),
            round(self.bbox.y2, 1),
        ]


@dataclass(frozen=True, slots=True)
class PredictionResult:
    provider: str
    model_id: str
    image_width: int
    image_height: int
    latency_ms: float
    detections: tuple[Detection, ...]
    confidence_threshold: float
    iou_threshold: float
    class_names: tuple[str, ...] = ("crop", "weed")

    @property
    def count(self) -> int:
        return len(self.detections)

    @property
    def class_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {name: 0 for name in self.class_names}
        for detection in self.detections:
            counts[detection.class_name] = counts.get(detection.class_name, 0) + 1
        return counts

    @property
    def average_confidence(self) -> float:
        if not self.detections:
            return 0.0
        return sum(item.confidence for item in self.detections) / len(self.detections)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": True,
            "provider": self.provider,
            "model_id": self.model_id,
            "image_width": self.image_width,
            "image_height": self.image_height,
            "latency_ms": round(self.latency_ms, 2),
            "count": self.count,
            "class_counts": self.class_counts,
            "average_confidence": round(self.average_confidence, 6),
            "thresholds": {
                "confidence": self.confidence_threshold,
                "iou": self.iou_threshold,
            },
            "detections": [item.to_dict() for item in self.detections],
        }
