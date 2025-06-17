import streamlit as st
from utils.conexao import conectar
from datetime import datetime
from utils.email_utils import enviar_email_notificacao


def carregar():
    st.title("Formulário de Cadastro")
    st.markdown("Preencha todos os campos abaixo para realizar seu cadastro.")

    # === Dados do Responsável ===
    st.subheader("Dados do Responsável pelo Preenchimento")
    email_responsavel = st.text_input("Seu Email", key="email_responsavel")

    if not email_responsavel:
        st.warning("⚠️ Por favor, insira seu email para começar.")
        st.stop()
    else:
        if 'email_confirmado' not in st.session_state:
            if st.button("➡️ Preencher Formulário"):
                st.session_state['email_confirmado'] = True

    if 'email_confirmado' not in st.session_state:
        st.stop()

    # === Dados da Escola ===
    st.subheader("Dados da Escola")
    nome_escola = st.text_input("Nome da Escola", key="nome_escola")
    cnpj = st.text_input("CNPJ", key="cnpj")

    col1, col2 = st.columns(2)
    rua = col1.text_input("Rua", key="rua")
    numero = col2.text_input("Número", key="numero")

    bairro = st.text_input("Bairro", key="bairro")

    col3, col4 = st.columns(2)
    cidade = col3.text_input("Cidade", key="cidade")
    estado = col4.selectbox(
        "Estado",
        ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
         "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
         "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"],
        key="estado"
    )

    cep = st.text_input("CEP", key="cep")

    # === Dados dos Responsáveis da Escola ===
    st.subheader("Dados dos Responsáveis pela Escola")
    nome_responsavel = st.text_input("Nome do Responsável pela Escola", key="nome_responsavel")
    cargo_responsavel = st.text_input("Cargo", key="cargo_responsavel")

    col5, col6 = st.columns(2)
    telefone = col5.text_input("Telefone", key="telefone")
    celular = col6.text_input("Celular", key="celular")

    email_escola = st.text_input("Email da Escola", key="email_escola")

    # === Dados Acadêmicos ===
    st.subheader("Dados Acadêmicos")
    infantil = st.number_input("Número de alunos na Educação Infantil", min_value=0, step=1, key="infantil")
    fund1 = st.number_input("Número de alunos no Fundamental I", min_value=0, step=1, key="fund1")
    fund2 = st.number_input("Número de alunos no Fundamental II", min_value=0, step=1, key="fund2")
    medio = st.number_input("Número de alunos no Ensino Médio", min_value=0, step=1, key="medio")

    # === Informações Complementares ===
    st.subheader("💡 Informações Complementares")
    observacoes = st.text_area("Observações adicionais", key="observacoes")

    enviado = st.button("📤 Enviar Formulário")

    if enviado:
        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO formularios (
                    data_envio, email_responsavel, nome_escola, cnpj, rua, numero, bairro, cidade, estado, cep,
                    nome_responsavel, cargo_responsavel, telefone, celular, email_escola,
                    infantil, fund1, fund2, medio, observacoes
                ) VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                email_responsavel, nome_escola, cnpj, rua, numero, bairro, cidade, estado, cep,
                nome_responsavel, cargo_responsavel, telefone, celular, email_escola,
                infantil, fund1, fund2, medio, observacoes
            ))

            conn.commit()
            cursor.close()
            conn.close()

            enviar_email_notificacao(nome_escola, email_responsavel)

            st.success("✅ Formulário enviado com sucesso! A equipe receberá seus dados em breve.")
            st.balloons()

            # Limpar a sessão após envio
            del st.session_state['email_confirmado']
            del st.session_state['email_responsavel']

        except Exception as e:
            st.error(f"❌ Erro ao enviar formulário: {e}")
