#!/usr/bin/env bash

# Kontrola a instalace Tesseract OCR
if ! command -v tesseract &> /dev/null
then
    echo "Tesseract není nainstalován! Ukončuji..."
    exit 1
fi


# Spuštění aplikace
uvicorn main:app --host 0.0.0.0 --port 10000
