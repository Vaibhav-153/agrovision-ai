"""Gradio interface for local development and Render deployment."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import gradio as gr

from .config import PROJECT_ROOT, Settings
from .errors import AgroVisionError
from .rate_limit import FixedWindowRateLimiter
from .service import AgroVisionService
from .visualization import empty_summary_html

LOGGER = logging.getLogger(__name__)
TABLE_HEADERS = ["#", "Class", "Confidence %", "x1", "y1", "x2", "y2"]


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
        <small>Provider: Roboflow Serverless · Model: {settings.roboflow_model_id}</small>
      </div>
    </div>
    """


def create_demo(
    *,
    settings: Settings | None = None,
    service: AgroVisionService | Any | None = None,
) -> gr.Blocks:
    settings = settings or Settings.from_env()
    service = service or AgroVisionService(settings)
    limiter = FixedWindowRateLimiter(
        settings.rate_limit_requests, settings.rate_limit_window_seconds
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
            # Internal details stay in server logs; users receive a stable message.
            LOGGER.exception("Unexpected prediction failure")
            raise gr.Error(
                "Prediction failed unexpectedly. Check the Space logs and configuration.",
                duration=8,
            ) from exc

    def clear_ui():
        return None, None, empty_summary_html(), [], {}

    with gr.Blocks(
        title="AgroVision AI — Crop & Weed Detection",
        fill_width=True,
        analytics_enabled=False,
    ) as demo:
        gr.HTML(
            """
            <section class="hero-shell">
              <div class="hero-copy">
                <p class="eyebrow">AGRICULTURAL COMPUTER VISION</p>
                <h1>AgroVision <span>AI</span></h1>
                <p class="hero-text">Detect crops and weeds in field images using a Roboflow-hosted YOLO11 Nano object detector. The API key remains on the server.</p>
              </div>
              <div class="hero-badge">
                <span>MODEL</span><strong>YOLO11n</strong><small>2 classes · crop / weed</small>
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
                )

                with gr.Group():
                    confidence = gr.Slider(
                        0.05,
                        0.95,
                        value=settings.default_confidence,
                        step=0.05,
                        label="Confidence threshold",
                        info="Lower values return more detections; higher values are stricter.",
                    )
                    iou = gr.Slider(
                        0.10,
                        0.90,
                        value=settings.default_iou,
                        step=0.05,
                        label="IoU threshold for non-maximum suppression",
                        info="Lower values suppress overlapping boxes more aggressively.",
                    )
                    max_detections = gr.Slider(
                        1,
                        settings.max_detections,
                        value=min(50, settings.max_detections),
                        step=1,
                        label="Maximum detections",
                    )

                with gr.Row():
                    analyze_button = gr.Button(
                        "Analyze field image", variant="primary", scale=3
                    )
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
                )
                summary = gr.HTML(empty_summary_html())

        with gr.Tabs():
            with gr.Tab("Detections"):
                detection_table = gr.Dataframe(
                    headers=TABLE_HEADERS,
                    datatype=["number", "str", "number", "number", "number", "number", "number"],
                    value=[],
                    interactive=False,
                    wrap=True,
                    show_row_numbers=False,
                    max_height=420,
                )
            with gr.Tab("Normalized JSON"):
                raw_json = gr.JSON(value={}, label="Prediction response")
            with gr.Tab("Model and evaluation notes"):
                gr.Markdown(
                    """
                    **Current hosted model:** YOLO11 Nano, initialized from an MS COCO public checkpoint and trained on Roboflow for two classes (`crop`, `weed`).

                    **Recorded platform metrics:** mAP50 **83.1%**, precision **75.9%**, recall **80.2%**, crop AP50 **78%**, weed AP50 **88%**. Exact mAP50–95, per-class precision/recall, and the confusion matrix were not exported, so they are not claimed here.

                    **Safety:** This is a portfolio/research demonstration. Do not use it as the only control signal for autonomous spraying, cutting, or crop removal.
                    """
                )

        gr.Markdown("### Try the included examples")
        examples = [
            [str(PROJECT_ROOT / "examples" / "crop_example.jpeg"), settings.default_confidence, settings.default_iou, 50],
            [str(PROJECT_ROOT / "examples" / "weed_example.jpeg"), settings.default_confidence, settings.default_iou, 50],
            [str(PROJECT_ROOT / "examples" / "mixed_example.jpeg"), settings.default_confidence, settings.default_iou, 50],
        ]
        gr.Examples(
            examples=examples,
            inputs=[input_image, confidence, iou, max_detections],
            outputs=[output_image, summary, detection_table, raw_json],
            fn=predict_ui,
            run_on_click=True,
            cache_examples=False,
            example_labels=["Crop example", "Weed example", "Mixed / challenging example"],
        )

        with gr.Accordion("How the pipeline works", open=False):
            gr.Markdown(
                """
                `Image upload → validation and EXIF removal → temporary JPEG → Roboflow Serverless API → YOLO11n inference → response normalization → bounding-box rendering → counts, table, and JSON`

                The browser never receives the private Roboflow API key. In production, the key is stored securely as the `ROBOFLOW_API_KEY` environment variable on the Render web service.                """
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
