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
        title = "Private model connection configured"
        message = "The hosted detector is ready for crop and weed inference."
    else:
        state = "warning"
        title = "Live inference needs configuration"
        message = "Add ROBOFLOW_API_KEY on Render before running a prediction."

    return f"""
    <section class="status-card {state}">
      <span class="status-dot" aria-hidden="true"></span>
      <div class="status-copy">
        <strong>{title}</strong>
        <span>{message}</span>
        <small>Roboflow Serverless &middot; {settings.roboflow_model_id}</small>
      </div>
      <span class="status-chip">{'READY' if state == 'ready' else 'SETUP'}</span>
    </section>
    """


def _section_heading(number: str, title: str, subtitle: str) -> str:
    return f"""
    <div class="section-heading">
      <span class="step-number">{number}</span>
      <div>
        <h2>{title}</h2>
        <p>{subtitle}</p>
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
        elem_classes=["agrovision-app"],
    ) as demo:
        gr.HTML(
            """
            <section class="hero-shell">
              <div class="hero-copy">
                <div class="hero-kicker">
                  <span class="kicker-dot"></span>
                  AGRICULTURAL COMPUTER VISION
                </div>
                <h1>AgroVision <span>AI</span></h1>
                <p class="hero-text">
                  Upload a field image, run crop and weed detection, and review
                  annotated results with confidence and bounding-box details.
                </p>
                <div class="hero-meta">
                  <span>YOLO11 Nano</span>
                  <span>2 classes</span>
                  <span>Roboflow Serverless</span>
                </div>
              </div>
              <div class="hero-visual" aria-hidden="true">
                <div class="hero-orbit orbit-one"></div>
                <div class="hero-orbit orbit-two"></div>
                <div class="hero-model-card">
                  <span>DETECTION MODEL</span>
                  <strong>YOLO11n</strong>
                  <small>crop <b>/</b> weed</small>
                </div>
              </div>
            </section>
            """
        )

        gr.HTML(_model_status(settings))

        with gr.Row(equal_height=False, elem_classes=["workspace-grid"]):
            with gr.Column(
                scale=5,
                min_width=320,
                elem_classes=["workspace-card", "upload-workspace"],
            ):
                gr.HTML(
                    _section_heading(
                        "01",
                        "Upload field image",
                        "Choose a clear JPG, PNG, or camera image from the field.",
                    )
                )

                input_image = gr.Image(
                    type="pil",
                    image_mode="RGB",
                    sources=["upload", "webcam", "clipboard"],
                    label="Input image",
                    height=420,
                    elem_classes=["image-panel", "input-panel"],
                    elem_id="input-image",
                )

                with gr.Column(elem_classes=["control-card"]):
                    gr.HTML(
                        """
                        <div class="control-heading">
                          <div>
                            <strong>Inference controls</strong>
                            <span>Fine-tune how detections are filtered.</span>
                          </div>
                          <span class="control-badge">TUNE</span>
                        </div>
                        """
                    )

                    confidence = gr.Slider(
                        0.05,
                        0.95,
                        value=settings.default_confidence,
                        step=0.05,
                        label="Confidence threshold",
                        info="Higher values keep only stronger predictions.",
                        elem_classes=["control-slider"],
                    )
                    iou = gr.Slider(
                        0.10,
                        0.90,
                        value=settings.default_iou,
                        step=0.05,
                        label="IoU threshold",
                        info="Controls suppression of overlapping detections.",
                        elem_classes=["control-slider"],
                    )
                    max_detections = gr.Slider(
                        1,
                        settings.max_detections,
                        value=min(50, settings.max_detections),
                        step=1,
                        label="Maximum detections",
                        info="Caps the number of highest-confidence boxes returned.",
                        elem_classes=["control-slider"],
                    )

                with gr.Row(elem_classes=["action-row"]):
                    analyze_button = gr.Button(
                        "Analyze field image",
                        variant="primary",
                        scale=3,
                        elem_classes=["analyze-button"],
                    )
                    clear_button = gr.Button(
                        "Clear",
                        variant="secondary",
                        scale=1,
                        elem_classes=["clear-button"],
                    )

            with gr.Column(
                scale=7,
                min_width=420,
                elem_classes=["workspace-card", "result-workspace"],
            ):
                gr.HTML(
                    _section_heading(
                        "02",
                        "Review model output",
                        "Inspect the annotated image and prediction summary.",
                    )
                )

                output_image = gr.Image(
                    type="pil",
                    label="Annotated result",
                    height=420,
                    interactive=False,
                    buttons=["download", "fullscreen"],
                    elem_classes=["image-panel", "output-panel"],
                    elem_id="output-image",
                )
                summary = gr.HTML(
                    empty_summary_html(),
                    elem_classes=["summary-panel"],
                )

        gr.HTML(
            """
            <div class="results-heading">
              <div>
                <span class="results-kicker">PREDICTION DETAILS</span>
                <h2>Detection results</h2>
              </div>
              <p>Switch between the table, normalized response, and model notes.</p>
            </div>
            """
        )

        with gr.Tabs(elem_id="result-tabs", elem_classes=["result-tabs"]):
            with gr.Tab("Detections"):
                detection_table = gr.HTML(
                    value=detection_table_html(),
                    elem_id="detections-table",
                    elem_classes=["detections-panel"],
                )

            with gr.Tab("Normalized JSON"):
                raw_json = gr.JSON(
                    value={},
                    label="Prediction response",
                    elem_classes=["json-panel"],
                )

            with gr.Tab("Model notes"):
                gr.HTML(
                    """
                    <section class="model-notes-card">
                      <div class="notes-grid">
                        <div class="note-item">
                          <span>Task</span>
                          <strong>Object detection</strong>
                        </div>
                        <div class="note-item">
                          <span>Model</span>
                          <strong>YOLO11 Nano</strong>
                        </div>
                        <div class="note-item">
                          <span>Classes</span>
                          <strong>crop / weed</strong>
                        </div>
                        <div class="note-item">
                          <span>Serving</span>
                          <strong>Roboflow Serverless</strong>
                        </div>
                      </div>
                      <div class="note-copy">
                        <h3>Recorded validation values</h3>
                        <p>
                          Project material records mAP50 83.1%, precision 75.9%, recall 80.2%,
                          crop AP50 78%, and weed AP50 88%. The dataset is small, so performance
                          on unseen farms, crops, seasons, and cameras has not been established.
                        </p>
                        <p class="note-warning">
                          Educational demonstration only. Do not use these predictions as the sole
                          control signal for autonomous spraying, cutting, or crop removal.
                        </p>
                      </div>
                    </section>
                    """
                )

        with gr.Accordion(
            "How the pipeline works",
            open=False,
            elem_classes=["info-accordion"],
        ):
            gr.HTML(
                """
                <div class="accordion-copy">
                  <div class="pipeline-flow">
                    <span>Image upload</span><b>→</b>
                    <span>Validation</span><b>→</b>
                    <span>EXIF removal</span><b>→</b>
                    <span>Roboflow inference</span><b>→</b>
                    <span>Normalized detections</span><b>→</b>
                    <span>Annotated output</span>
                  </div>
                  <p>
                    The browser never receives the private Roboflow API key. On Render,
                    keep it in the <code>ROBOFLOW_API_KEY</code> environment variable.
                  </p>
                </div>
                """
            )

        with gr.Accordion(
            "Inference controls",
            open=False,
            elem_classes=["info-accordion"],
        ):
            gr.HTML(
                """
                <div class="accordion-copy control-explainer">
                  <div>
                    <strong>Confidence</strong>
                    <span>Minimum score required before a detection is shown.</span>
                  </div>
                  <div>
                    <strong>IoU</strong>
                    <span>Controls non-maximum suppression for overlapping boxes.</span>
                  </div>
                  <div>
                    <strong>Maximum detections</strong>
                    <span>Limits the number of highest-confidence boxes returned.</span>
                  </div>
                </div>
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
