#!/usr/bin/env bash
apt-get update && apt-get install -y tesseract-ocr
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
uvicorn main:app --host 0.0.0.0 --port 10000
