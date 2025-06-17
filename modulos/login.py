import streamlit as st
import psycopg2
import psycopg2.extras
import bcrypt
from utils.conexao import conectar


def login_usuario():
    st.subheader("Login")
    st.markdown("Acesse sua conta para entrar no sistema.")

    col1, col2 = st.columns(2)

    with col1:
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

    with col2:
        st.markdown("### Preencher Formulário")
        st.write("Caso você esteja aqui para preencher apenas o **formulário**, clique abaixo.")
        if st.button("Acessar Formulário"):
            st.session_state['autenticado'] = True
            st.session_state['usuario_nome'] = "Usuário Formulário"
            st.session_state['usuario_email'] = ""
            st.session_state['usuario_cargo'] = "formulario"
            st.success("Acesso liberado para formulário!")
            st.rerun()

    if st.button("Entrar"):
        try:
            conn = conectar()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cursor.execute("""
                SELECT nome, email, senha_hash, cargo, status 
                FROM usuarios 
                WHERE email = %s
            """, (email,))
            resultado = cursor.fetchone()

            if resultado:
                senha_db = resultado['senha_hash']
                if bcrypt.checkpw(senha.encode('utf-8'), senha_db.encode('utf-8')):
                    if resultado['status'] == 'ativo':
                        st.session_state['autenticado'] = True
                        st.session_state['usuario_nome'] = resultado['nome']
                        st.session_state['usuario_email'] = resultado['email']
                        st.session_state['usuario_cargo'] = resultado['cargo']
                        st.success(f"Bem-vindo, {resultado['nome']}!")
                        st.rerun()
                    else:
                        st.error("Usuário inativo. Entre em contato com o administrador.")
                else:
                    st.error("Email ou senha incorretos.")
            else:
                st.error("Email ou senha incorretos.")

            cursor.close()
            conn.close()

        except Exception as e:
            st.error(f"Erro no login: {e}")
