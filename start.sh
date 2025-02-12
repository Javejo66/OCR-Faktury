#!/usr/bin/env bash
sudo apt-get update && sudo apt-get install -y tesseract-ocr
uvicorn main:app --host 0.0.0.0 --port 10000
