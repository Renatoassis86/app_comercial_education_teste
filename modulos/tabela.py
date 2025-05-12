
import streamlit as st
import pandas as pd
import io
from utils.conexao import conectar
from utils.banners import exibir_banner

def carregar():
    st.markdown("## 🧾 Tabela Geral de Escolas")
    exibir_banner("banner_tabela")

    conn = conectar()
    query = """
        SELECT 
            e.id,
            e.nome_escola,
            e.estado,
            e.telefone,
            e.email,
            e.cnpj,
            e.qtd_infantil,
            e.qtd_fund1,
            e.qtd_fund2,
            e.qtd_medio,
            r.data_contato,
            r.meio_contato,
            r.encaminhamento,
            r.prontidao,
            r.classificacao_lead,
            r.resumo
        FROM escolas e
        LEFT JOIN registros r ON r.id_escola = e.id
    """
    df = pd.read_sql(query, conn)

    # Agrupamento e concatenação de registros
    tabela_final = df.groupby(['id', 'nome_escola']).agg({
        'estado': 'first',
        'telefone': 'first',
        'email': 'first',
        'cnpj': 'first',
        'qtd_infantil': 'first',
        'qtd_fund1': 'first',
        'qtd_fund2': 'first',
        'qtd_medio': 'first',
        'data_contato': lambda x: "; ".join(pd.to_datetime(x.dropna()).dt.strftime('%d/%m/%Y')),
        'meio_contato': lambda x: "; ".join(x.dropna().unique()),
        'encaminhamento': lambda x: "; ".join(x.dropna().unique()),
        'prontidao': lambda x: "; ".join(x.dropna().unique()),
        'classificacao_lead': lambda x: "; ".join(x.dropna().unique()),
        'resumo': lambda x: " / ".join(x.dropna().unique())
    }).reset_index()

    # Interface para exclusão
    escola_para_excluir = st.selectbox("Selecionar escola para excluir", ["Nenhuma"] + tabela_final['nome_escola'].tolist())
    if escola_para_excluir != "Nenhuma":
        if st.button("🗑️ Excluir Escola Selecionada"):
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM registros WHERE id_escola = (SELECT id FROM escolas WHERE nome_escola = %s)", (escola_para_excluir,))
                cursor.execute("DELETE FROM escolas WHERE nome_escola = %s", (escola_para_excluir,))
                conn.commit()
            st.success(f"Escola '{escola_para_excluir}' excluída com sucesso.")
            conn.close()
            st.stop()

    st.dataframe(tabela_final)

    # Exportar para Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        tabela_final.to_excel(writer, index=False, sheet_name='Escolas')
    output.seek(0)

    st.download_button(
        label="📥 Baixar Excel",
        data=output,
        file_name="tabela_geral_escolas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
