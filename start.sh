#!/usr/bin/env bash

# Rozbalení Tesseractu z našeho repozitáře
tar -xzf bin/tesseract-5.5.0.tar.gz -C bin/

# Nastavení cesty k Tesseractu
export PATH=$PWD/bin/tesseract-5.5.0:$PATH
export TESSDATA_PREFIX=$PWD/bin/tesseract-5.5.0/tessdata

# Kontrola, jestli je Tesseract dostupný
which tesseract || echo "Tesseract stále NENÍ dostupný!"

# Spuštění aplikace
uvicorn main:app --host 0.0.0.0 --port 10000
