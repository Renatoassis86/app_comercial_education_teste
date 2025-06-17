import streamlit as st
import bcrypt

st.title("🔐 Gerador de Senha Criptografada")

senha = st.text_input("Digite a senha que deseja criptografar", type="password")

if st.button("Gerar hash"):
    if senha:
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        st.success("Hash gerado:")
        st.code(senha_hash.decode())
    else:
        st.warning("Digite uma senha para gerar o hash.")


