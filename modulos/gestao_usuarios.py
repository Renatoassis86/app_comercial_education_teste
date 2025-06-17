import streamlit as st
import pandas as pd
import psycopg2
import psycopg2.extras
import bcrypt
from utils.conexao import conectar


def carregar():
    st.subheader("👥 Gestão de Usuários")

    conn = conectar()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # === Formulário para adicionar/editar usuários ===
    with st.expander("➕ Adicionar ou Editar Usuário", expanded=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome Completo")
        email = col2.text_input("Email")

        cargo = col1.selectbox("Cargo", ["", "gerente", "consultor", "assistente", "supervisor"])
        status = col2.selectbox("Status", ["", "ativo", "inativo"])

        senha = st.text_input("Senha", type="password")
        confirmar = st.text_input("Confirme a Senha", type="password")

        if st.button("💾 Salvar Usuário"):
            if not (nome and email and cargo and status):
                st.warning("⚠️ Preencha todos os campos obrigatórios.")
            elif senha != confirmar:
                st.error("❌ As senhas não coincidem.")
            else:
                senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode()

                try:
                    cursor.execute("""
                        INSERT INTO usuarios (nome, email, senha_hash, cargo, status)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO UPDATE SET
                            nome = EXCLUDED.nome,
                            senha_hash = EXCLUDED.senha_hash,
                            cargo = EXCLUDED.cargo,
                            status = EXCLUDED.status;
                    """, (nome, email, senha_hash, cargo, status))
                    conn.commit()
                    st.success("✅ Usuário salvo com sucesso.")
                except Exception as e:
                    st.error(f"Erro ao salvar usuário: {e}")

    st.markdown("---")

    # === Listagem de usuários ===
    st.subheader("📄 Lista de Usuários Cadastrados")

    try:
        cursor.execute("SELECT id, nome, email, cargo, status FROM usuarios ORDER BY id")
        dados = cursor.fetchall()

        if dados:
            df = pd.DataFrame(dados, columns=["ID", "Nome", "Email", "Cargo", "Status"])
            st.dataframe(df)

            # === Opção de excluir usuário ===
            lista_emails = [d['email'] for d in dados]
            email_excluir = st.selectbox("Selecione o usuário para excluir", [""] + lista_emails)

            if email_excluir:
                if st.button("🗑️ Excluir Usuário"):
                    try:
                        cursor.execute("DELETE FROM usuarios WHERE email = %s", (email_excluir,))
                        conn.commit()
                        st.success("✅ Usuário excluído com sucesso.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir: {e}")
        else:
            st.info("Nenhum usuário cadastrado.")

    except Exception as e:
        st.error(f"Erro ao carregar usuários: {e}")

    cursor.close()
    conn.close()
