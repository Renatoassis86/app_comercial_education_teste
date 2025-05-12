import streamlit as st
import base64
from pathlib import Path

def exibir_banner(nome_base):
    extensoes = ['.jpeg', '.jpg', '.png']
    for ext in extensoes:
        caminho = Path(f"{nome_base}{ext}")
        if caminho.exists():
            with open(caminho, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f'<img class="banner-img" src="data:image/{ext[1:]};base64,{encoded}">',
                unsafe_allow_html=True
            )
            return
    st.warning(f"Banner '{nome_base}' não encontrado.")

# utils/helpers.py

def limpar_formulario():
    import streamlit as st
    st.session_state["form_limpar"] = True
