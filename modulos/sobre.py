import streamlit as st
from utils.banners import exibir_banner

def carregar():

    # Exibe o banner correspondente à página inicial
    exibir_banner("banner_sobre")

    st.markdown("<h2 style='color:#1f538d;'>Aplicativo de Gerenciamento Comercial Cidade Viva Education</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Sobre o Aplicativo</h3>
        <p>O Aplicativo de Gerenciamento Comercial Cidade Viva Education foi desenvolvido para atender às necessidades estratégicas da equipe comercial, oferecendo uma plataforma prática, segura e eficiente para organizar, controlar e analisar o relacionamento com as escolas e instituições parceiras.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Propósito do Aplicativo</h3>
        <p>Seu principal objetivo é centralizar o processo de gestão de propostas comerciais, registros de negociações e acompanhamento do desempenho, proporcionando uma visão clara das oportunidades e decisões estratégicas.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Justificativa da Plataforma</h3>
        <p>A criação deste sistema responde à necessidade de maior controle e padronização das informações comerciais, aumentando a agilidade na comunicação interna, otimizando o atendimento e possibilitando a análise crítica de dados para orientar tomadas de decisão fundamentadas.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Principais Funcionalidades</h3>
        <ul>
            <ul>Cadastro e gerenciamento de escolas e clientes.</li>
            <ul>Registro detalhado de propostas e negociações.</li>
            <ul>Acompanhamento de status das tratativas comerciais.</li>
            <ul>Painéis de visualização de desempenho comercial (Dashboards).</li>
            <ul>Geração de relatórios de apoio à gestão.</li>
            <ul>Histórico centralizado de interações.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="caixa-branca">
        <h3>Impacto Esperado</h3>
        <p>Com o uso do aplicativo, a equipe comercial poderá estabelecer processos mais organizados, mensurar resultados de maneira eficiente, aprimorar o relacionamento com os parceiros e embasar decisões estratégicas na análise de dados reais e consolidados.</p>
        </div>
        """, unsafe_allow_html=True)
