from __future__ import annotations

from agrovision.roboflow import find_prediction_payload, parse_predictions


def test_direct_prediction_is_normalized():
    payload = {
        "predictions": [
            {
                "x": 50,
                "y": 40,
                "width": 20,
                "height": 10,
                "confidence": 0.9,
                "class": "1",
                "class_id": 1,
            }
        ]
    }
    detections = parse_predictions(
        payload,
        image_width=100,
        image_height=80,
        confidence_threshold=0.5,
        max_detections=10,
        class_map={0: "crop", 1: "weed"},
    )
    assert len(detections) == 1
    assert detections[0].class_name == "weed"
    assert detections[0].bbox.x1 == 40.0
    assert detections[0].bbox.y2 == 45.0


def test_nested_workflow_style_payload_is_found():
    nested = [{"outputs": {"model_predictions": {"predictions": []}}}]
    assert find_prediction_payload(nested) == {"predictions": []}


def test_confidence_filter_clamping_and_unknown_class():
    payload = {
        "predictions": [
            {
                "x": 0,
                "y": 0,
                "width": 30,
                "height": 30,
                "confidence": 0.8,
                "class": "crop",
            },
            {
                "x": 50,
                "y": 50,
                "width": 10,
                "height": 10,
                "confidence": 0.2,
                "class": "weed",
            },
            {
                "x": 50,
                "y": 50,
                "width": 10,
                "height": 10,
                "confidence": 0.99,
                "class": "other",
                "class_id": 2,
            },
        ]
    }
    detections = parse_predictions(
        payload,
        image_width=100,
        image_height=100,
        confidence_threshold=0.5,
        max_detections=10,
        class_map={0: "crop", 1: "weed"},
    )
    assert len(detections) == 1
    assert detections[0].bbox.x1 == 0.0
