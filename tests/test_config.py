from __future__ import annotations

import pytest

from agrovision.config import Settings


def clone(settings: Settings, **changes):
    values = {name: getattr(settings, name) for name in settings.__dataclass_fields__}
    values.update(changes)
    return Settings(**values)


def test_public_summary_omits_private_key(settings):
    configured = clone(settings, roboflow_api_key="private-value-that-must-not-leak")
    public = configured.public_summary()
    assert "private-value" not in str(public)
    assert "api_key" not in str(public).lower()
    assert public["model_id"] == "fake-project/1"


def test_placeholder_key_is_not_configured(settings):
    placeholder = clone(settings, roboflow_api_key="YOUR_PRIVATE_KEY")
    assert placeholder.inference_configured is False


def test_real_key_is_configured(settings):
    configured = clone(settings, roboflow_api_key="fake-configured-key-123")
    assert configured.inference_configured is True


def test_invalid_model_id_rejected(settings):
    broken = clone(settings, roboflow_model_id="workspace/project/version")
    with pytest.raises(ValueError):
        broken.validate()


def test_invalid_threshold_rejected(settings):
    broken = clone(settings, default_confidence=1.5)
    with pytest.raises(ValueError):
        broken.validate()
