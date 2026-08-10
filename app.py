"""AgroVision AI entry point for local execution and Render deployment."""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agrovision.config import Settings  # noqa: E402
from agrovision.ui import create_demo  # noqa: E402

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
        allowed_paths=[str(PROJECT_ROOT / "examples")],
        footer_links=["api", "gradio"],
        css_paths=PROJECT_ROOT / "assets" / "custom.css",
    )
