"""Build the Gradio application without launching a network server."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from agrovision.config import Settings
from agrovision.ui import create_demo


def main() -> int:
    demo = create_demo(settings=Settings.from_env())
    config = demo.get_config_file()
    api_names = {item.get("api_name") for item in config.get("dependencies", [])}
    if "predict" not in api_names:
        print("ERROR: Gradio predict API endpoint was not registered.")
        return 1
    print(f"Smoke test passed: {len(config.get('components', []))} UI components loaded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
