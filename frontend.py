import streamlit as st
import requests

# Nastavení URL backendu
BACKEND_URL = "https://ocr-faktury.onrender.com/upload-multiple/"

st.title("Nahrávání více faktur")

# Pole pro nahrání více souborů
uploaded_files = st.file_uploader("Vyberte faktury", type=["pdf", "jpg", "png"], accept_multiple_files=True)

if st.button("Nahrát faktury"):
    if uploaded_files:
        files = [("files", (file.name, file.getvalue())) for file in uploaded_files]
        response = requests.post(BACKEND_URL, files=files)

        if response.status_code == 200:
            st.success("Faktury úspěšně nahrány!")
            st.json(response.json())  # Zobrazíme odpověď backendu
        else:
            st.error(f"Chyba při nahrávání: {response.status_code}")
    else:
        st.warning("Prosím vyberte soubory k nahrání.")
