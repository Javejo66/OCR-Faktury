#!/usr/bin/env bash

# Aktualizace balíčků a instalace Tesseract OCR
apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-all

# Ověření instalace
which tesseract || echo "Tesseract stále NENÍ nainstalován!"

# Nastavení proměnné prostředí
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Spuštění aplikace
uvicorn main:app --host 0.0.0.0 --port 10000

