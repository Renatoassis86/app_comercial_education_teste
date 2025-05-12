import streamlit as st
from datetime import datetime

def carregar():
    st.title("🔐 Acesso Restrito - Área Administrativa")

    with st.form("form_login"):
        email = st.text_input("Usuário (email)")
        senha = st.text_input("Senha", type="password")
        login = st.form_submit_button("Entrar")

    if login:
        if email.strip().lower() == "administrativo.education@cidadeviva.org" and senha == "Education@2024#":
            st.success("✅ Login realizado com sucesso!")
            mostrar_area_contrato()
        else:
            st.error("❌ Usuário ou senha incorretos. Tente novamente.")

def mostrar_area_contrato():
    st.markdown("### 📑 Documentos Contratuais")

    st.write("""
    Nesta seção você pode baixar:
    - 📄 Ficha cadastral para preenchimento da escola
    - 📘 Minuta genérica de contrato
    """)

    col1, col2 = st.columns(2)

    with col1:
        with open("documentos/Ficha Cadastral - Cidade Viva Education (3) (1).docx", "rb") as f:
            st.download_button("📥 Baixar Ficha Cadastral", f, file_name="ficha_cadastral.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    with col2:
        with open("documentos/Minuta - Cidade Viva Education.pdf", "rb") as f:
            st.download_button("📘 Baixar Minuta do Contrato", f, file_name="minuta_contrato_generica.pdf", mime="application/pdf")
