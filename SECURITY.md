# Security Policy

## Credentials

- Store `ROBOFLOW_API_KEY` only in a local `.env` file or Render Environment settings.
- Never place the key in Python, JavaScript, screenshots, notebooks, issue comments, or commit history.
- Rotate the key immediately if it appears in chat, a screenshot, terminal output, or a public repository.
- `.env` is excluded by `.gitignore`; only `.env.example` belongs in Git.

## Upload safety

The application decodes images with Pillow, corrects orientation, limits dimensions and pixel count, converts to RGB, removes EXIF/GPS metadata, writes a temporary sanitized JPEG, and deletes it after inference.

## Public-demo protection

The app applies a small per-process rate limit. Roboflow provider quotas and Render access controls are still important. This limiter is not a distributed API gateway.

## Reporting

Report suspected vulnerabilities privately to the repository owner. Never include active credentials in a report.
