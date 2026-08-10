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
from .visualization import detection_table_html, empty_summary_html

LOGGER = logging.getLogger(__name__)
TRAINING_CHARTS = PROJECT_ROOT / "assets" / "training_charts"


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
    """Build and return the complete AgroVision Gradio application."""
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
            # Internal details stay in Render logs; users get a stable message.
            LOGGER.exception("Unexpected prediction failure")
            raise gr.Error(
                "Prediction failed unexpectedly. Check the Render logs and "
                "Roboflow configuration, then retry.",
                duration=8,
            ) from exc

    def clear_ui():
        return None, None, empty_summary_html(), detection_table_html(), {}

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
                <p class="hero-text">Detect crops and weeds in field images using a Roboflow-hosted YOLO11 Nano object detector. The private API key stays on the server.</p>
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
                    elem_id="input-image",
                )

                with gr.Group():
                    confidence = gr.Slider(
                        0.05,
                        0.95,
                        value=settings.default_confidence,
                        step=0.05,
                        label="Confidence threshold",
                        info=(
                            "Lower values return more detections; higher values "
                            "accept only stronger predictions."
                        ),
                    )
                    iou = gr.Slider(
                        0.10,
                        0.90,
                        value=settings.default_iou,
                        step=0.05,
                        label="IoU threshold for non-maximum suppression",
                        info=(
                            "Lower values suppress overlapping boxes more aggressively; "
                            "higher values keep more nearby boxes."
                        ),
                    )
                    max_detections = gr.Slider(
                        1,
                        settings.max_detections,
                        value=min(50, settings.max_detections),
                        step=1,
                        label="Maximum detections",
                        info="Limits how many highest-confidence boxes are returned.",
                    )

                with gr.Row():
                    analyze_button = gr.Button(
                        "Analyze field image",
                        variant="primary",
                        scale=3,
                    )
                    clear_button = gr.Button(
                        "Clear",
                        variant="secondary",
                        scale=1,
                    )

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

            with gr.Tab("Model and evaluation notes"):
                gr.Markdown(
                    """
### Current model

- **Task:** object detection — the model identifies the class and location of each plant.
- **Algorithm:** YOLO11 Nano (`YOLO11n`).
- **Training method:** transfer learning from an MS COCO public checkpoint.
- **Classes:** `crop` and `weed`.
- **Training platform:** Roboflow Custom Training.
- **Deployment:** Gradio on Render; model inference on Roboflow Serverless.

### Recorded validation evidence

| Metric | Value | Meaning |
|---|---:|---|
| mAP50 / AP50 | **83.1%** | Detection quality at IoU 0.50; higher is better. |
| Precision | **75.9%** | Of all reported detections, how many were correct. |
| Recall | **80.2%** | Of all labelled objects, how many the model found. |
| Derived F1 | **about 78.0%** | Balance between precision and recall. |
| Crop AP50 | **78%** | Average precision for the crop class. |
| Weed AP50 | **88%** | Average precision for the weed class. |
| Training time | **17 minutes** | Platform-reported training duration. |

The provided performance chart shows a strict **mAP50–95 value of 0.5155 at epoch 135**. This stricter metric is better for comparing checkpoints because it checks box quality across many IoU thresholds. The exact Roboflow-selected checkpoint epoch, per-class precision/recall, and confusion matrix were not exported, so they are not claimed.

> **Safety:** This is a portfolio and research demonstration. Do not use it as the only control signal for autonomous spraying, cutting, or crop removal.
                    """
                )

            with gr.Tab("Training charts"):
                gr.Markdown(
                    """
### How to read the charts

- **Model performance:** higher is better. The dark curve is the easier mAP50-style score; the light curve is the stricter mAP50–95 score.
- **Box loss:** lower is better. It measures bounding-box location error.
- **Class loss:** lower is better. It measures crop-versus-weed classification error.
- **Object loss:** lower is better. It measures whether the model correctly finds an object.
- **Best checkpoint rule:** prefer the checkpoint with the highest validation **mAP50–95**, then verify weed recall and crop precision. Do not choose a model only because its training loss is the lowest.
                    """
                )
                with gr.Row():
                    gr.Image(
                        value=str(TRAINING_CHARTS / "model_performance.png"),
                        label="Model performance — higher is better",
                        interactive=False,
                        height=300,
                        buttons=["fullscreen"],
                        elem_classes="training-chart",
                    )
                    gr.Image(
                        value=str(TRAINING_CHARTS / "box_loss.png"),
                        label="Box loss — lower is better",
                        interactive=False,
                        height=300,
                        buttons=["fullscreen"],
                        elem_classes="training-chart",
                    )
                with gr.Row():
                    gr.Image(
                        value=str(TRAINING_CHARTS / "class_loss.png"),
                        label="Class loss — lower is better",
                        interactive=False,
                        height=300,
                        buttons=["fullscreen"],
                        elem_classes="training-chart",
                    )
                    gr.Image(
                        value=str(TRAINING_CHARTS / "object_loss.png"),
                        label="Object loss — lower is better",
                        interactive=False,
                        height=300,
                        buttons=["fullscreen"],
                        elem_classes="training-chart",
                    )

        gr.Markdown("### Try the included examples")
        examples = [
            [
                str(PROJECT_ROOT / "examples" / "crop_example.jpeg"),
                settings.default_confidence,
                settings.default_iou,
                50,
            ],
            [
                str(PROJECT_ROOT / "examples" / "weed_example.jpeg"),
                settings.default_confidence,
                settings.default_iou,
                50,
            ],
            [
                str(PROJECT_ROOT / "examples" / "mixed_example.jpeg"),
                settings.default_confidence,
                settings.default_iou,
                50,
            ],
        ]
        gr.Examples(
            examples=examples,
            inputs=[input_image, confidence, iou, max_detections],
            outputs=[output_image, summary, detection_table, raw_json],
            fn=predict_ui,
            run_on_click=True,
            cache_examples=False,
            example_labels=[
                "Crop example",
                "Weed example",
                "Mixed / challenging example",
            ],
        )

        with gr.Accordion("What each website feature does", open=False):
            gr.Markdown(
                """
- **Upload / webcam / clipboard:** supplies the agricultural image.
- **Confidence threshold:** controls how strong a prediction must be before it is shown.
- **IoU threshold:** controls how overlapping boxes are merged by non-maximum suppression.
- **Maximum detections:** limits the number of returned boxes.
- **Analyze field image:** validates the image, sends a sanitized copy to Roboflow, and displays the result.
- **Annotated result:** shows green crop boxes and orange weed boxes.
- **Summary cards:** show total objects, class counts, average confidence, and full request latency.
- **Detections table:** shows every class, confidence, and corner coordinates.
- **Normalized JSON:** provides a structured response for developers and API users.
- **Examples:** run three included images without selecting a local file.
- **Training charts:** explain model learning and checkpoint selection.
                """
            )

        with gr.Accordion("How the pipeline works", open=False):
            gr.Markdown(
                """
`Image upload → validation and EXIF removal → temporary JPEG → Roboflow Serverless API → YOLO11n inference → response normalization → bounding-box rendering → counts, table, and JSON`

The browser never receives the private Roboflow API key. On Render, the key is stored securely as the `ROBOFLOW_API_KEY` environment variable.

The web application runs on **Render**, while neural-network inference is performed remotely by **Roboflow Serverless**.
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
