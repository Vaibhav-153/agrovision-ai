# Cleanup Summary — Version 1.1.0

## Deployment

- Standardized the repository on **Render**.
- Removed obsolete deployment workflow and settings files for the previous hosting attempt.
- Added `render.yaml`, `.python-version`, and `deploy/RENDER_SETTINGS.md`.
- Updated all source comments, errors, documentation, diagrams, and security notes.

## Frontend

- Replaced duplicate/conflicting CSS with one clean light-theme stylesheet.
- Replaced the output-only Gradio spreadsheet with a custom HTML detection table.
- Removed the dark table header and sort/filter popup problem.
- Added class pills, responsive styling, accessible contrast, and chart cards.
- Added a training-charts tab and feature-help accordion.

## Model documentation

- Explained YOLO11 Nano and transfer learning in simple English.
- Added precision, recall, F1, mAP50, mAP50–95, and IoU explanations.
- Added all four supplied training charts with clear labels.
- Explained which metric should select the best checkpoint.
- Marked unknown Roboflow training parameters as unknown instead of guessing.

## Code quality

- Cleaned configuration formatting and expanded safe model-ID validation.
- Updated error messages for Render.
- Kept inference logic modular and provider secrets server-side.
- Added a visualization test for the custom detection table.
- Updated preflight checks for charts and Render files.

## Verification

- Secret scan: passed.
- Tests: 22 passed.
- Gradio smoke test: 39 components and `/predict` endpoint.
- Local startup: HTTP 200.
