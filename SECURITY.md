# Security Policy

## Credentials

- Store `ROBOFLOW_API_KEY` only in a local `.env`, a Hugging Face Space secret, or a GitHub Actions secret.
- Never place the key in Python, JavaScript, screenshots, notebooks, issue comments, or commit history.
- Rotate a key immediately if it appears in chat, a screenshot, a terminal recording, or a public repository.

## Upload safety

The application checks image type through Pillow decoding, corrects orientation, limits dimensions/pixel count, converts to RGB, and creates a fresh metadata-free JPEG before sending it to Roboflow. Uploaded images are not intentionally persisted by this repository.

## Reporting

Report suspected vulnerabilities privately to the repository owner. Do not include active credentials in the report.
