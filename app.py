"""AgroVision AI entry point for local execution and Render deployment."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from agrovision.config import Settings
from agrovision.ui import create_demo

PROJECT_ROOT = Path(__file__).resolve().parent
CSS_FILE = PROJECT_ROOT / "assets" / "custom.css"

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

settings = Settings.from_env()
demo = create_demo(settings=settings)

if __name__ == "__main__":
    demo.launch(
        server_name=settings.server_name,
        server_port=settings.port,
        show_error=False,
        max_file_size=f"{settings.max_upload_mb}mb",
        footer_links=["api", "gradio"],
        css_paths=[str(CSS_FILE)],
    )
