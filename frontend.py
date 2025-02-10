import streamlit as st
import requests

st.title("Hromadné nahrávání faktur")

uploaded_files = st.file_uploader("Vyber faktury", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    files = [("files", (file.name, file.getvalue())) for file in uploaded_files]
    response = requests.post("https://ocr-faktury.onrender.com/upload-multiple/", files=files)

    if response.status_code == 200:
        st.success("Faktury úspěšně zpracovány!")
        st.text_area("Výstupní XML:", response.json().get("xml", ""), height=300)
    else:
        st.error("Chyba při zpracování faktur")
