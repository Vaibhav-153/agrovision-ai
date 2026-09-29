"""AgroVision AI entry point for local execution and Render deployment."""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
CSS_FILE = PROJECT_ROOT / "assets" / "custom.css"


# Make the src package available when app.py is executed
# directly by Render or during local development.
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from agrovision.config import Settings  # noqa: E402
from agrovision.ui import create_demo  # noqa: E402


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

settings = Settings.from_env()

demo = create_demo(settings=settings)


# ---------------------------------------------------------
# Local / Render startup
# ---------------------------------------------------------

if __name__ == "__main__":
    launch_options = {
        "server_name": settings.server_name,
        "server_port": settings.port,
        "show_error": False,
        "max_file_size": f"{settings.max_upload_mb}mb",
        "footer_links": ["api", "gradio"],
    }

    # Load the custom stylesheet when it exists.
    if CSS_FILE.exists():
        launch_options["css_paths"] = CSS_FILE

    demo.launch(**launch_options)
