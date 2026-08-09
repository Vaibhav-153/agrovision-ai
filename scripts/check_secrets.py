"""Fail CI when likely credentials are committed in tracked project files."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}
TEXT_SUFFIXES = {
    ".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".json", ".env", ".example", ".cff"
}
PLACEHOLDERS = {
    "", "YOUR_PRIVATE_KEY", "YOUR_NEW_PRIVATE_KEY", "PASTE_YOUR_PRIVATE_KEY_HERE", "CHANGEME"
}
ASSIGNMENT = re.compile(r"^\s*ROBOFLOW_API_KEY[ \t]*=[ \t]*([^\r\n#]*)", re.IGNORECASE | re.MULTILINE)
PYTHON_LITERAL = re.compile(r"api_key\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        # A local .env is expected and is excluded by .gitignore. We scan only
        # repository-safe templates and source files here.
        if path.name == ".env":
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"Dockerfile", ".gitignore", ".dockerignore"}:
            yield path


def looks_like_secret(value: str) -> bool:
    normalized = value.strip().strip("\"'")
    if normalized.upper() in PLACEHOLDERS:
        return False
    if normalized.startswith(("${", "$", "os.environ", "os.getenv")):
        return False
    lowered = normalized.lower()
    if any(marker in lowered for marker in ("fake", "test", "private-value", "example")):
        return False
    return len(normalized) >= 12


def main() -> int:
    findings: list[str] = []

    gitignore = ROOT / ".gitignore"
    if not gitignore.is_file() or not any(
        line.strip() == ".env"
        for line in gitignore.read_text(encoding="utf-8").splitlines()
    ):
        findings.append(".gitignore must contain an exact .env rule.")

    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in (ASSIGNMENT, PYTHON_LITERAL):
            for match in pattern.finditer(text):
                if looks_like_secret(match.group(1)):
                    findings.append(f"{path.relative_to(ROOT)} contains a likely hard-coded API key.")

    if findings:
        print("Potential secret exposure detected:")
        for finding in sorted(set(findings)):
            print(f"- {finding}")
        return 1
    print("Secret scan passed: no hard-coded Roboflow key pattern was detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
