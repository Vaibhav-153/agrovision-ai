# 1. Project Overview

## Title

**AgroVision AI — Crop and Weed Detection with YOLO11 Nano and Roboflow Serverless Inference**

## Problem statement

Manual weed monitoring is time-consuming and inconsistent across large fields. A vision system can help identify plants and distinguish crops from weeds in field imagery. The difficult part is not only detecting vegetation but also reducing crop-versus-weed confusion, because treating a crop as a weed can be harmful and missing weeds can reduce intervention effectiveness.

## Objective

Build a portfolio-ready application that:

- accepts an agricultural image;
- detects objects belonging to `crop` and `weed` classes;
- returns bounding boxes, class labels, and confidence values;
- reports crop/weed counts and inference latency;
- keeps the Roboflow API key private;
- runs locally, on GitHub, and as a Hugging Face Space;
- clearly separates measured results from unavailable metrics.

## Real-world use cases

- field scouting assistance;
- agronomy dataset review;
- weed-density estimation prototypes;
- demonstration of computer-vision MLOps and deployment skills;
- decision-support research before any safety-critical automation.

This project is not a certified agricultural control system. Predictions must be reviewed by a human before spraying, cutting, or crop removal.

## ML/DL task

This is **two-class object detection**. Unlike image classification, object detection predicts both:

1. **What** each object is (`crop` or `weed`).
2. **Where** it is using a bounding box.

## Selected model

- Architecture: YOLO11 Nano (`YOLO11n`)
- Initialization: public MS COCO checkpoint
- Training platform: Roboflow
- Serving platform: Roboflow Serverless Cloud API
- Model ID: `crop-or-weed-detection-jnmzz-1-yolo11n-t1/1`
- Class mapping: `0 = crop`, `1 = weed`

## Why YOLO11 Nano was selected

YOLO11 Nano is the smallest model in the YOLO11 family. It was selected for the first deployed version because it offers low latency, a small deployment footprint, and direct compatibility with the model already trained in Roboflow. YOLO11 Small or Medium and RF-DETR may improve performance in some cases, but they were not evaluated under the same split and therefore are not claimed to be better here.

## Dataset/input requirements

The Roboflow project contains approximately 1,300 labeled field images. The current application accepts one JPEG, PNG, or WebP-style image through Gradio/Pillow. It validates image integrity, dimensions, and pixel count before inference.

## Expected input

A field image showing one or more plants. Images should be reasonably focused, well lit, and representative of the training distribution.

## Expected output

- annotated image with crop/weed boxes;
- total, crop, and weed counts;
- confidence per detection;
- bounding-box coordinates (`x1`, `y1`, `x2`, `y2`);
- round-trip inference latency;
- normalized JSON result.

## Technology stack

- Python 3.11
- Gradio
- Pillow
- Roboflow Inference SDK
- Roboflow Serverless Cloud API
- Pytest
- Docker
- GitHub Actions
- Hugging Face Spaces
