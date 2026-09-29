"""Gradio interface for local development and Render deployment."""

from __future__ import annotations

import logging
from typing import Any

import gradio as gr

from .config import Settings
from .errors import AgroVisionError
from .rate_limit import FixedWindowRateLimiter
from .service import AgroVisionService
from .visualization import detection_table_html, empty_summary_html

LOGGER = logging.getLogger(__name__)


def _model_status(settings: Settings) -> str:
    if settings.inference_configured:
        state = "ready"
        text = "Private model connection configured"
    else:
        state = "warning"
        text = "Add ROBOFLOW_API_KEY to run live inference"
    return f"""
    <div class="status-card {state}">
      <span class="status-dot"></span>
      <div>
        <strong>{text}</strong>
        <small>Provider: Roboflow Serverless | Model: {settings.roboflow_model_id}</small>
      </div>
    </div>
    """


def create_demo(
    *,
    settings: Settings | None = None,
    service: AgroVisionService | Any | None = None,
) -> gr.Blocks:
    """Build and return the AgroVision Gradio application."""
    settings = settings or Settings.from_env()
    service = service or AgroVisionService(settings)
    limiter = FixedWindowRateLimiter(
        settings.rate_limit_requests,
        settings.rate_limit_window_seconds,
    )

    def predict_ui(
        image: Any,
        confidence: float,
        iou: float,
        max_detections: int,
    ):
        try:
            limiter.check()
            return service.analyze(image, confidence, iou, max_detections)
        except AgroVisionError as exc:
            raise gr.Error(str(exc), duration=8) from exc
        except Exception as exc:
            LOGGER.exception("Unexpected prediction failure")
            raise gr.Error(
                "Prediction failed unexpectedly. Check the server logs and "
                "Roboflow configuration, then retry.",
                duration=8,
            ) from exc

    def clear_ui():
        return None, None, empty_summary_html(), detection_table_html(), {}

    with gr.Blocks(
        title="AgroVision AI - Crop and Weed Detection",
        fill_width=True,
        analytics_enabled=False,
    ) as demo:
        gr.HTML(
            """
            <section class="hero-shell">
              <div class="hero-copy">
                <p class="eyebrow">AGRICULTURAL COMPUTER VISION</p>
                <h1>AgroVision <span>AI</span></h1>
                <p class="hero-text">Detect crops and weeds in field images using a hosted
                YOLO11 Nano object detector.</p>
              </div>
              <div class="hero-badge">
                <span>MODEL</span><strong>YOLO11n</strong><small>crop / weed</small>
              </div>
            </section>
            """
        )
        gr.HTML(_model_status(settings))

        with gr.Row(equal_height=False):
            with gr.Column(scale=5, min_width=320):
                gr.Markdown("### 1. Upload field image")
                input_image = gr.Image(
                    type="pil",
                    image_mode="RGB",
                    sources=["upload", "webcam", "clipboard"],
                    label="Input image",
                    height=420,
                    elem_classes="image-panel",
                    elem_id="input-image",
                )
                confidence = gr.Slider(
                    0.05,
                    0.95,
                    value=settings.default_confidence,
                    step=0.05,
                    label="Confidence threshold",
                    info="Higher values keep only stronger predictions.",
                )
                iou = gr.Slider(
                    0.10,
                    0.90,
                    value=settings.default_iou,
                    step=0.05,
                    label="IoU threshold",
                    info="Controls suppression of overlapping detections.",
                )
                max_detections = gr.Slider(
                    1,
                    settings.max_detections,
                    value=min(50, settings.max_detections),
                    step=1,
                    label="Maximum detections",
                )
                with gr.Row():
                    analyze_button = gr.Button("Analyze field image", variant="primary", scale=3)
                    clear_button = gr.Button("Clear", variant="secondary", scale=1)

            with gr.Column(scale=7, min_width=420):
                gr.Markdown("### 2. Review model output")
                output_image = gr.Image(
                    type="pil",
                    label="Annotated result",
                    height=420,
                    interactive=False,
                    buttons=["download", "fullscreen"],
                    elem_classes="image-panel",
                    elem_id="output-image",
                )
                summary = gr.HTML(empty_summary_html())

        with gr.Tabs(elem_id="result-tabs"):
            with gr.Tab("Detections"):
                detection_table = gr.HTML(
                    value=detection_table_html(),
                    elem_id="detections-table",
                )
            with gr.Tab("Normalized JSON"):
                raw_json = gr.JSON(value={}, label="Prediction response")
            with gr.Tab("Model notes"):
                gr.Markdown(
                    """
### Model

- Task: two-class object detection
- Model: YOLO11 Nano
- Classes: `crop` and `weed`
- Training platform: Roboflow
- Serving: Roboflow Serverless API

Recorded validation values in the project material are mAP50 83.1%, precision 75.9%,
recall 80.2%, crop AP50 78%, and weed AP50 88%. The dataset is small and performance
on unseen farms, crops, seasons, and cameras has not been established.

This project is an educational demonstration. Do not use its predictions as the only
control signal for autonomous spraying, cutting, or crop removal.
                    """
                )

        with gr.Accordion("How the pipeline works", open=False):
            gr.Markdown(
                """
`Image upload -> validation and EXIF removal -> temporary JPEG -> Roboflow Serverless`

`-> YOLO11n inference -> prediction normalization -> bounding boxes -> counts, table, and JSON`

The browser does not receive the private Roboflow API key. On Render, store it as the
`ROBOFLOW_API_KEY` environment variable.
                """
            )

        with gr.Accordion("Inference controls", open=False):
            gr.Markdown(
                """
- **Confidence threshold:** minimum confidence required before a detection is shown.
- **IoU threshold:** controls non-maximum suppression for overlapping boxes.
- **Maximum detections:** caps the number of highest-confidence boxes returned.
                """
            )

        analyze_button.click(
            fn=predict_ui,
            inputs=[input_image, confidence, iou, max_detections],
            outputs=[output_image, summary, detection_table, raw_json],
            api_name="predict",
            concurrency_limit=4,
        )
        clear_button.click(
            fn=clear_ui,
            inputs=None,
            outputs=[input_image, output_image, summary, detection_table, raw_json],
            api_name=False,
        )

    demo.queue(default_concurrency_limit=4, max_size=20)
    return demo
