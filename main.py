from fastapi import FastAPI, File, UploadFile
from typing import List
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io

app = FastAPI()

@app.post("/upload-multiple/")
async def upload_multiple_invoices(files: List[UploadFile] = File(...)):
    faktury = []
    
    for file in files:
        contents = await file.read()
        text = extract_text_from_file(contents, file.filename)
        faktury.append({"filename": file.filename, "text": text})

    return {"message": "Faktury zpracovány", "faktury": faktury}

def extract_text_from_file(contents: bytes, filename: str) -> str:
    """OCR extrahuje text z PDF nebo obrázku."""
    if filename.endswith(".pdf"):
        images = convert_from_bytes(contents)
        text = "\n".join(pytesseract.image_to_string(img, lang="ces") for img in images)
    else:
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image, lang="ces")
    return text.strip()
