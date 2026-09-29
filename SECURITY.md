# Security Policy

## Credentials

Store `ROBOFLOW_API_KEY` only in a local `.env` file or in the hosting provider's secret settings. Do not place the key in Python, JavaScript, screenshots, notebooks, issue comments, or commit history.

The repository includes `.env.example` only. The real `.env` file is ignored by Git.

## Image handling

Uploaded images are decoded with Pillow, orientation-corrected, checked against size limits, converted to RGB, and written to a temporary JPEG before hosted inference. The temporary file is removed after the request.

## Public demo

The app uses a small in-memory request limiter. It is intended as burst protection for a portfolio demo, not as a replacement for provider quotas or a distributed rate-limiting service.
