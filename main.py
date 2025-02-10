from fastapi import FastAPI, File, UploadFile
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import xml.etree.ElementTree as ET
import io
import re
from typing import List

app = FastAPI()

# Regulární výrazy pro extrakci údajů
REGEX_PATTERNS = {
    "ico": r"IČO[:\s]*(\d{8})",
    "dic": r"DIČ[:\s]*([A-Z]{2}\d+)",
    "datum_vystaveni": r"Datum vystavení[:\s]*(\d{1,2}\.\d{1,2}\.\d{4})",
    "datum_splatnosti": r"Splatnost[:\s]*(\d{1,2}\.\d{1,2}\.\d{4})",
    "cislo_faktury": r"Faktura č\.[:\s]*(\d+)",
    "var_symbol": r"Var\s*symbol[:\s]*(\d+)",
    "celkova_castka": r"Celkem k úhradě[:\s]*([\d\s,]+)",
    "zaklad_dph": r"Základ DPH (\d{1,2})%\s*[:\s]*([\d\s,]+)",
    "dph_castka": r"DPH (\d{1,2})%\s*[:\s]*([\d\s,]+)"
}

@app.post("/upload-multiple/")
async def upload_multiple_invoices(files: List[UploadFile] = File(...)):
    faktury = []

    for file in files:
        contents = await file.read()
        text = extract_text_from_file(contents, file.filename)
        faktura_data = extract_invoice_data(text)
        xml_data = generate_xml(file.filename, faktura_data)
        faktury.append(xml_data)

    combined_xml = generate_combined_xml(faktury)
    return {"message": "Faktury zpracovány", "xml": combined_xml}

def extract_text_from_file(contents: bytes, filename: str) -> str:
    """OCR extrahuje text z PDF nebo obrázku."""
    try:
        if filename.endswith(".pdf"):
            images = convert_from_bytes(contents)
            text = "\n".join(pytesseract.image_to_string(img, lang="ces") for img in images)
        else:
            image = Image.open(io.BytesIO(contents))
            text = pytesseract.image_to_string(image, lang="ces")
        return text.strip()
    except Exception as e:
        return f"Chyba při zpracování souboru {filename}: {e}"

def extract_invoice_data(text: str) -> dict:
    """Vytěží klíčové údaje z textu faktury."""
    data = {}

    for key, pattern in REGEX_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if key in ["zaklad_dph", "dph_castka"]:
                sazba = match.group(1)  # Např. 21 nebo 12
                hodnota = match.group(2)  # Částka
                data.setdefault(key, {})[sazba] = hodnota.strip()
            else:
                data[key] = match.group(1).strip()

    return data

def generate_xml(filename: str, faktura_data: dict) -> str:
    """Vytvoří XML přesně podle hodnot na faktuře."""
    faktura = ET.Element("Faktura")
    ET.SubElement(faktura, "Soubor").text = filename
    ET.SubElement(faktura, "ICO").text = faktura_data.get("ico", "N/A")
    ET.SubElement(faktura, "DIC").text = faktura_data.get("dic", "N/A")
    ET.SubElement(faktura, "DatumVystaveni").text = faktura_data.get("datum_vystaveni", "N/A")
    ET.SubElement(faktura, "DatumSplatnosti").text = faktura_data.get("datum_splatnosti", "N/A")
    ET.SubElement(faktura, "CisloFaktury").text = faktura_data.get("cislo_faktury", "N/A")
    ET.SubElement(faktura, "VarSymbol").text = faktura_data.get("var_symbol", "N/A")
    ET.SubElement(faktura, "CelkovaCastka").text = faktura_data.get("celkova_castka", "N/A")

    polozky = ET.SubElement(faktura, "Polozky")
    
    for sazba, hodnota in faktura_data.get("zaklad_dph", {}).items():
        polozka = ET.SubElement(polozky, "Polozka")
        ET.SubElement(polozka, "SazbaDPH").text = sazba + "%"
        ET.SubElement(polozka, "ZakladDPH").text = hodnota
        ET.SubElement(polozka, "DPH").text = faktura_data.get("dph_castka", {}).get(sazba, "0")

    return ET.tostring(faktura, encoding="utf-8").decode("utf-8")

def generate_combined_xml(faktury: list) -> str:
    """Vytvoří XML pro více faktur."""
    root = ET.Element("HromadnyExport")
    for faktura in faktury:
        faktura_elem = ET.fromstring(faktura)
        root.append(faktura_elem)

    return ET.tostring(root, encoding="utf-8").decode("utf-8")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
