"""Server-side bounding-box rendering and HTML result formatting."""
from __future__ import annotations

from html import escape

from PIL import Image, ImageDraw, ImageFont

from .schemas import PredictionResult

COLORS = {
    "crop": (55, 190, 104),
    "weed": (239, 142, 57),
}


def _font(size: int) -> ImageFont.ImageFont:
    """Load a readable bold font on Linux, Windows, or fallback systems."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def annotate_image(image: Image.Image, result: PredictionResult) -> Image.Image:
    """Draw color-coded bounding boxes and confidence labels."""
    canvas = image.convert("RGB").copy()
    draw = ImageDraw.Draw(canvas)
    line_width = max(2, round(max(canvas.size) / 300))
    font = _font(max(12, round(max(canvas.size) / 42)))

    for detection in result.detections:
        color = COLORS.get(detection.class_name, (80, 150, 220))
        box = detection.bbox
        xy = (box.x1, box.y1, box.x2, box.y2)
        draw.rectangle(xy, outline=color, width=line_width)

        label = f"{detection.class_name.upper()} {detection.confidence:.0%}"
        left, top, right, bottom = draw.textbbox((0, 0), label, font=font)
        text_width = right - left
        text_height = bottom - top
        label_y = max(0, box.y1 - text_height - 10)
        background = (
            box.x1,
            label_y,
            min(canvas.width, box.x1 + text_width + 12),
            label_y + text_height + 8,
        )
        draw.rectangle(background, fill=color)
        draw.text(
            (box.x1 + 6, label_y + 3),
            label,
            fill=(10, 30, 22),
            font=font,
        )
    return canvas


def result_summary_html(result: PredictionResult) -> str:
    """Return five compact summary cards for the web interface."""
    counts = result.class_counts
    crop_count = counts.get("crop", 0)
    weed_count = counts.get("weed", 0)
    return f"""
    <div class="result-kpis">
      <div class="kpi"><span>Total detections</span><strong>{result.count}</strong></div>
      <div class="kpi crop"><span>Crop</span><strong>{crop_count}</strong></div>
      <div class="kpi weed"><span>Weed</span><strong>{weed_count}</strong></div>
      <div class="kpi"><span>Average confidence</span><strong>{result.average_confidence:.1%}</strong></div>
      <div class="kpi"><span>Round-trip latency</span><strong>{result.latency_ms:.0f} ms</strong></div>
    </div>
    """


def empty_summary_html(message: str = "Upload an image to begin.") -> str:
    """Return the empty-state message used before the first prediction."""
    return f'<div class="empty-state">{escape(message)}</div>'


def detection_table_html(result: PredictionResult | None = None) -> str:
    """Render a stable light-theme HTML table for detected objects.

    A custom HTML table is used instead of Gradio's spreadsheet component. The
    result is output-only, so sorting/editing controls are unnecessary, and this
    approach avoids browser-theme-dependent dark menus and headers.
    """
    if result is None or not result.detections:
        return """
        <div class="detection-table-shell">
          <table class="detection-table" aria-label="Detected objects">
            <thead>
              <tr>
                <th>#</th><th>Class</th><th>Confidence</th>
                <th>x1</th><th>y1</th><th>x2</th><th>y2</th>
              </tr>
            </thead>
            <tbody>
              <tr class="empty-row">
                <td colspan="7">No detections to display.</td>
              </tr>
            </tbody>
          </table>
        </div>
        """

    rows: list[str] = []
    for index, detection in enumerate(result.detections, start=1):
        box = detection.bbox
        rows.append(
            "<tr>"
            f"<td>{index}</td>"
            f"<td><span class=\"class-pill {escape(detection.class_name)}\">"
            f"{escape(detection.class_name)}</span></td>"
            f"<td>{detection.confidence * 100.0:.2f}%</td>"
            f"<td>{box.x1:.1f}</td>"
            f"<td>{box.y1:.1f}</td>"
            f"<td>{box.x2:.1f}</td>"
            f"<td>{box.y2:.1f}</td>"
            "</tr>"
        )

    return f"""
    <div class="detection-table-shell">
      <table class="detection-table" aria-label="Detected objects">
        <thead>
          <tr>
            <th>#</th><th>Class</th><th>Confidence</th>
            <th>x1</th><th>y1</th><th>x2</th><th>y2</th>
          </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    """
