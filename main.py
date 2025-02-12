from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Ahoj, server běží!"}

@app.post("/upload/")
async def upload_files(files: list[UploadFile]):
    extracted_texts = {}

    for file in files:
        file_extension = file.filename.split(".")[-1].lower()
        file_data = await file.read()

        try:
            if file_extension == "pdf":
                images = convert_from_bytes(file_data)
                text = "\n".join([pytesseract.image_to_string(img) for img in images])
            elif file_extension in ["png", "jpg", "jpeg"]:
                image = Image.open(io.BytesIO(file_data))
                text = pytesseract.image_to_string(image)
            else:
                return JSONResponse(content={"error": f"Nepodporovaný typ souboru: {file.filename}"}, status_code=400)

            extracted_texts[file.filename] = text.strip()

        except Exception as e:
            return JSONResponse(content={"error": f"Chyba při zpracování {file.filename}: {str(e)}"}, status_code=500)

    return {"extrahovaný_text": extracted_texts}
