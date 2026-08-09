from __future__ import annotations

from agrovision.ui import create_demo


def test_gradio_app_builds_with_predict_api(settings, service):
    demo = create_demo(settings=settings, service=service)
    config = demo.get_config_file()
    api_names = {item.get("api_name") for item in config.get("dependencies", [])}
    assert "predict" in api_names
    assert len(config.get("components", [])) >= 20
