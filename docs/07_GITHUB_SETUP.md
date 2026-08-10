# 7. GitHub Setup

Create an empty repository, then run:

```bash
git init
git add .
git status
git commit -m "Initial AgroVision AI project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agrovision-ai.git
git push -u origin main
```

Before every commit, confirm `.env` is not staged.

Recommended topics:

```text
computer-vision yolo11 roboflow gradio render agriculture object-detection python
```

## CI

`.github/workflows/ci.yml` runs on pushes and pull requests. It:

1. installs Python 3.11;
2. installs development dependencies;
3. compiles source files;
4. scans for hard-coded keys;
5. runs pytest;
6. builds the Gradio UI.

## Update workflow

```bash
git add .
git commit -m "Describe the change"
git push origin main
```

Render automatically redeploys the linked branch.
