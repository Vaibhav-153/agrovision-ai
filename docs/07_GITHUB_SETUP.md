# 7. GitHub Publishing Guide

## Create the repository

1. Sign in to GitHub.
2. Choose **New repository**.
3. Use a name such as `agrovision-ai`.
4. Choose Public for a portfolio project or Private while testing.
5. Do not initialize with another README, license, or `.gitignore` because they already exist here.

## Security check before the first commit

```bash
python scripts/check_secrets.py
```

Also verify:

```bash
git status --ignored
```

`.env` must appear under ignored files and must never be staged.

## Git commands

```bash
git init
git add .
git status
git commit -m "Initial production-ready AgroVision AI project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agrovision-ai.git
git push -u origin main
```

## Repository settings

- Enable branch protection for `main` when working with collaborators.
- Require the `CI` workflow before merge.
- Add a project description and topics such as `computer-vision`, `yolo11`, `roboflow`, `gradio`, `hugging-face`, `agriculture`, and `object-detection`.
- Add the public Hugging Face demo URL to the repository website field after deployment.

## What must not be pushed

- `.env`;
- Roboflow private keys;
- raw private datasets;
- model binaries unless licensing and file size are handled;
- screenshots showing credentials;
- generated user uploads.

## Large-file errors

This deployment repository is intentionally small. If a future model file exceeds GitHub limits, use Git LFS or store it in a model registry/Hugging Face Model repository. Do not add a large checkpoint to normal Git history.

## Updating the project

```bash
git checkout -b feature/improve-ui
# Make and test changes.
pytest
git add .
git commit -m "Improve prediction dashboard"
git push -u origin feature/improve-ui
```

Open a pull request, review CI, then merge.
