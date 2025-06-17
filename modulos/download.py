import streamlit as st
import pandas as pd
from utils.conexao import conectar
from datetime import datetime
import io


def carregar():
    st.title("⬇️Download dos Documentos e Formulários")

    # === Bloco de documentos ===
    st.subheader("Documentos Oficiais")

    col1, col2 = st.columns(2)

    with col1:
        try:
            with open("documentos/Ficha Cadastral - Cidade Viva Education.docx", "rb") as f:
                st.download_button(
                    label="Baixar Ficha Cadastral",
                    data=f,
                    file_name="Ficha_Cadastral.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except FileNotFoundError:
            st.error("❌ Arquivo Ficha Cadastral não encontrado na pasta 'documentos'.")

    with col2:
        try:
            with open("documentos/Minuta - Cidade Viva Education.pdf", "rb") as f:
                st.download_button(
                    label="Baixar Minuta do Contrato",
                    data=f,
                    file_name="Minuta_Contrato.pdf",
                    mime="application/pdf"
                )
        except FileNotFoundError:
            st.error("❌ Arquivo Minuta do Contrato não encontrado na pasta 'documentos'.")

    # === Bloco dos formulários preenchidos ===
    st.subheader("Formulários Preenchidos")

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM formularios ORDER BY data_envio DESC")
        colunas = [desc[0] for desc in cursor.description]
        dados = cursor.fetchall()

        df = pd.DataFrame(dados, columns=colunas)

        if df.empty:
            st.info("Nenhum formulário preenchido encontrado.")
        else:
            st.dataframe(df)

            # Gerar planilha Excel em memória
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Formularios")

            buffer.seek(0)  # Volta o cursor para o início do arquivo

            data_atual = datetime.now().strftime("%Y-%m-%d")
            nome_arquivo = f"formularios_{data_atual}.xlsx"

            st.download_button(
                label="Baixar Planilha de Formulários",
                data=buffer,
                file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados dos formulários: {e}")
