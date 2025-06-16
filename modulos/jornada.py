import streamlit as st
import psycopg2.extras
from utils.banners import exibir_banner
from utils.conexao import conectar

def carregar():
    exibir_banner("banner_jornada")
    st.markdown("<h2 style='color:#1f538d;'>Jornada de Relacionamento</h2>", unsafe_allow_html=True)
    
    st.markdown('''
    <div class='caixa-branca'>
    <p>Esta aba apresenta a <strong>linha do tempo da negociação</strong> de cada escola com o Education. Acompanhe a evolução das interações, estágios, potenciais e encaminhamentos ao longo do tempo.</p>
    <ul>
        <li><strong>Objetivo:</strong> auxiliar no acompanhamento estratégico da jornada comercial e pedagógica.</li>
        <li><strong>Aplicações:</strong> diagnóstico de maturidade do lead, gargalos de negociação e visualização de histórico completo.</li>
        <li><strong>Métricas exibidas:</strong> resumo do contato, responsável, meio de contato, interesse, prontidão, abertura, encaminhamento, potencial financeiro, classificação e probabilidade.</li>
    </ul>
    </div>
    ''', unsafe_allow_html=True)

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome_escola FROM escolas")
        escolas = cursor.fetchall()
        conn.close()
    except Exception as e:
        st.error(f"Erro ao carregar escolas: {e}")
        return

    escola_dict = {nome: id_ for id_, nome in escolas}
    escola_selecionada = st.selectbox("Selecione a escola para visualizar a jornada", [""] + list(escola_dict.keys()))
    
    if escola_selecionada:
        try:
            conn = conectar()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM registros WHERE id_escola = %s ORDER BY data_contato ASC", (escola_dict[escola_selecionada],))
            registros = cursor.fetchall()
            conn.close()

            if not registros:
                st.info("Nenhum registro encontrado para esta escola.")
                return

            for registro in registros:
                encaminhamentos = (
                    ", ".join([e.strip() for e in registro["encaminhamento"].split(",")])
                    if registro["encaminhamento"] else "Nenhum"
                )

                st.markdown(f"""
                    <div class="jornada-card">
                        <strong>Data:</strong> {registro['data_contato'].strftime('%d/%m/%Y')}<br>
                        <strong>Resumo:</strong> {registro['resumo']}<br>
                        <strong>Contato:</strong> {registro['contato']} ({registro['cargo']})<br>
                        <strong>Responsável:</strong> {registro['responsavel']}<br>
                        <strong>Interesse:</strong> {registro['interesse']}<br>
                        <strong>Prontidão:</strong> {registro['prontidao']}<br>
                        <strong>Abertura:</strong> {registro['abertura']}<br>
                        <strong>Encaminhamentos:</strong> {encaminhamentos}<br>
                        <strong>Potencial Financeiro:</strong> R$ {registro['potencial_financeiro']:,.2f}<br>
                        <strong>Classificação do Lead:</strong> {registro['classificacao_lead']}<br>
                        <strong>Probabilidade:</strong> {registro['probabilidade']}%
                    </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro ao carregar registros: {e}")
