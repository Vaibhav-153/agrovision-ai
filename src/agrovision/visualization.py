"""Server-side bounding-box rendering and result formatting."""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from .schemas import PredictionResult

COLORS = {
    "crop": (55, 190, 104),
    "weed": (239, 142, 57),
}


def _font(size: int) -> ImageFont.ImageFont:
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
    return f'<div class="empty-state">{message}</div>'
