#!/usr/bin/env bash

# Kontrola a instalace Tesseract OCR
if ! command -v tesseract &> /dev/null
then
    echo "Tesseract není nainstalován, instaluji..."
    apt update && apt install -y tesseract-ocr
else
    echo "Tesseract je již nainstalován."
fi

# Spuštění aplikace
uvicorn main:app --host 0.0.0.0 --port 10000
