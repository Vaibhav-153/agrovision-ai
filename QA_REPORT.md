# Quality Assurance Report

## Verified project

AgroVision AI 1.1.0 — Render deployment edition.

## Executed checks

| Check | Result |
|---|---|
| Python compilation | Passed |
| Secret scan | Passed |
| Automated tests | **22 passed** |
| Gradio UI construction | Passed |
| Registered prediction endpoint | `/predict` present |
| UI components loaded | **39** |
| Local HTTP startup | **HTTP 200** |
| Obsolete hosting references | None found in text source/docs |
| Custom HTML detection table test | Passed |
| Training chart files | Present |
| Render configuration files | Present |
| Live Roboflow inference | Not executed here because the private key is not available |
| Final public prediction regression | Must be run by the repository owner after deployment |

## Commands used

```bash
python -m compileall -q app.py src scripts tests
python scripts/check_secrets.py
python -m pytest
python scripts/smoke_test.py
```

Local HTTP startup was tested on a temporary port and returned status `200`.

## External dependencies for a live prediction

- valid `ROBOFLOW_API_KEY`;
- permission to the hosted model ID;
- provider quota/credits;
- outbound network access;
- Roboflow service availability.

## Remaining owner verification

After pushing the cleaned repository to GitHub and Render:

1. wait until Render reports **Live**;
2. hard-refresh the browser;
3. run crop, weed, and mixed examples;
4. verify boxes, counts, HTML table, JSON, and training charts;
5. check Render logs for errors;
6. confirm no secret is visible in source or browser output.
