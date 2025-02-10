import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/upload-multiple/"

st.set_page_config(page_title="OCR Faktury", page_icon="📄", layout="wide")

st.title("📄 Hromadné nahrávání faktur pro Money S3")
st.write("Nahrajte faktury (PDF, JPG, PNG) a aplikace automaticky extrahuje důležité údaje.")

uploaded_files = st.file_uploader("📂 Nahrajte více faktur najednou", type=["pdf", "jpg", "png"], accept_multiple_files=True)

if uploaded_files:
    files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
    with st.spinner("Zpracovávám faktury..."):
        response = requests.post(BACKEND_URL, files=files)

    if response.status_code == 200:
        st.success("✅ Faktury byly úspěšně zpracovány!")
        st.text_area("📄 XML Výstup:", response.json()["xml"], height=300)
        st.download_button("📥 Stáhnout XML", response.json()["xml"], file_name="hromadne_faktury.xml")
    else:
        st.error("❌ Chyba při zpracování faktur. Zkuste to znovu.")
