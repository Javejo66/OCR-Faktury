import streamlit as st
import requests

# Backend URL
BACKEND_URL = "https://ocr-faktury.onrender.com/upload-multiple/"

st.title("Hromadné nahrávání faktur")

uploaded_files = st.file_uploader(
    "Vyber faktury", 
    type=["pdf", "png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"🔄 Odesílám {len(uploaded_files)} souborů na server...")
    
    files = [("files", (file.name, file.getvalue())) for file in uploaded_files]

    try:
        response = requests.post(BACKEND_URL, files=files, timeout=30)
        
        if response.status_code == 200:
            st.success("✅ Faktury úspěšně zpracovány!")
            st.text_area("📜 Výstupní XML:", response.json().get("xml", ""), height=300)
        else:
            st.error(f"❌ Chyba při zpracování faktur: {response.status_code}")
            st.text(f"Server odpověděl: {response.text}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"⛔ Chyba připojení k serveru: {e}")

