# 1. Project Overview

## Title

**AgroVision AI — Crop and Weed Detection**

## Problem

A field image can contain crops, weeds, soil, shadows, overlap, blur, and background vegetation. The system must find each plant and decide whether it is a crop or weed.

## Objective

Provide a simple web application that:

1. accepts an agricultural image;
2. validates and sanitizes it;
3. sends it to a trained detector;
4. shows crop/weed boxes, counts, confidence, latency, a table, and JSON;
5. keeps credentials on the server;
6. can be studied, tested, pushed to GitHub, and deployed on Render.

## Task type

This is **object detection**, not simple image classification. The output contains both a class and a bounding box for every detected object.

## Current implementation

- Model: YOLO11 Nano.
- Classes: crop and weed.
- Training: Roboflow Custom Training from an MS COCO checkpoint.
- Inference: Roboflow Serverless API.
- UI: Gradio.
- Hosting: Render Web Service.
- Source control and CI: GitHub and GitHub Actions.

## Real-world value

The project demonstrates precision-agriculture concepts, but it is not a safety-certified control system. It is useful for education, portfolio demonstration, API integration, and further agricultural-computer-vision research.
