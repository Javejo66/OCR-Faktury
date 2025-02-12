# Použití oficiálního Python 3.9 slim obrazu
FROM python:3.9-slim

# Aktualizace a instalace Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Nastavení pracovního adresáře
WORKDIR /app

# Zkopírování souborů do kontejneru
COPY . .

# Instalace Python balíčků
RUN pip install --no-cache-dir -r requirements.txt

# Spuštění aplikace
CMD ["bash", "start.sh"]
