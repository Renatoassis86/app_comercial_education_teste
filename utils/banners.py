import mysql.connector
from pathlib import Path
import base64
import streamlit as st

def verificar_conexao():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="Rairooha123@", database="comercialcve"
        )
        conn.close()
        return '<span style="color:green;">🟢 Banco Conectado</span>'
    except:
        return '<span style="color:red;">🔴 Falha na Conexão</span>'


def exibir_banner(nome_base):
    extensoes = ['.jpg', '.jpeg', '.png']
    for ext in extensoes:
        caminho = Path(f"imagens/{nome_base}{ext}")
        if caminho.exists():
            with open(caminho, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f'<img class="banner-img" src="data:image/{ext[1:]};base64,{encoded}">',
                unsafe_allow_html=True
            )
            return
    st.warning(f"Banner 'imagens/{nome_base}' não encontrado.")

