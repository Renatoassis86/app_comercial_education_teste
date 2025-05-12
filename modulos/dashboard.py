import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from utils.banners import exibir_banner
from utils.conexao import conectar
from datetime import datetime

def criar_grafico_barra(dados, titulo, cor, reduzir_nome=False):
    dados_formatado = dados.copy()
    if reduzir_nome:
        dados_formatado.index = [
            str(nome).split()[0] if isinstance(nome, str) and str(nome).strip() else "Desconhecido"
            for nome in dados.index
        ]
    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.bar(dados_formatado.index, dados_formatado.values, color=cor, edgecolor='black')
    ax.set_title(titulo)
    ax.set_ylabel("Total")
    ax.set_xticks(range(len(dados_formatado)))
    ax.set_xticklabels(dados_formatado.index, rotation=30, ha='right')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height * 0.95, f'{int(height)}',
                ha='center', va='top', fontsize=8, color='white')
    plt.tight_layout()
    st.pyplot(fig)

def carregar():
    st.markdown("## 📊 Dashboard Comercial e Relacional")
    exibir_banner("banner_dashboard")

    cores = ['#141A55', '#2486E7', '#F5B301', '#2D001B', '#E6482E', '#3A0CA3']
    conn = conectar()
    query = """
        SELECT r.*, e.nome_escola, e.estado, e.qtd_infantil, e.qtd_fund1, e.qtd_fund2, e.qtd_medio
        FROM registros r
        LEFT JOIN escolas e ON r.id_escola = e.id
    """
    df = pd.read_sql(query, conn)
    conn.close()

    df['data_contato'] = pd.to_datetime(df['data_contato'], errors='coerce')
    df['data_registro'] = pd.to_datetime(df['data_registro'], errors='coerce')
    df['mes_ano'] = df['data_contato'].dt.to_period('M').astype(str)

    with st.expander("🎯 Filtros", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        escola = col1.selectbox("Escola", ["Todas"] + sorted(df['nome_escola'].dropna().unique().tolist()))
        responsavel = col2.selectbox("Responsável", ["Todos"] + sorted(df['responsavel'].dropna().unique().tolist()))
        estado = col3.selectbox("Estado", ["Todos"] + sorted(df['estado'].dropna().unique().tolist()))
        porte = col4.selectbox("Porte", ["Todos", "Pequena", "Média", "Grande"])
        periodo = col5.selectbox("Período", ["Todos", "Últimos 7 dias", "Último mês", "Último ano"])

    df_filtro = df.copy()
    if escola != "Todas":
        df_filtro = df_filtro[df_filtro['nome_escola'] == escola]
    if responsavel != "Todos":
        df_filtro = df_filtro[df_filtro['responsavel'] == responsavel]
    if estado != "Todos":
        df_filtro = df_filtro[df_filtro['estado'] == estado]
    if porte != "Todos":
        total = df_filtro[['qtd_infantil', 'qtd_fund1', 'qtd_fund2', 'qtd_medio']].sum(axis=1)
        if porte == "Pequena":
            df_filtro = df_filtro[total < 200]
        elif porte == "Média":
            df_filtro = df_filtro[(total >= 200) & (total <= 500)]
        else:
            df_filtro = df_filtro[total > 500]
    if periodo != "Todos":
        hoje = pd.to_datetime("today")
        dias = {"Últimos 7 dias": 7, "Último mês": 30, "Último ano": 365}[periodo]
        df_filtro = df_filtro[df_filtro['data_contato'] > hoje - pd.Timedelta(days=dias)]

    if df_filtro.empty:
        st.warning("⚠️ Nenhum dado disponível após aplicar os filtros.")
        return

    # === KPIs principais ===
    st.markdown("### 📌 Visão Geral")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Escolas", df['nome_escola'].nunique())
    col2.metric("Interações", len(df))
    col3.metric("Ticket Médio", f"R$ {df_filtro['potencial_financeiro'].mean():,.2f}" if not df_filtro.empty else "R$ 0,00")
    col4.metric("Potencial Total", f"R$ {df_filtro['potencial_financeiro'].sum():,.2f}")

    contratos = df_filtro[df_filtro['encaminhamento'].str.contains("Contrato", na=False, case=False)]
    tempo_medio = (
        (contratos['data_contato'].max() - contratos['data_contato'].min()).days / len(contratos)
        if len(contratos) > 0 else 0
    )
    st.markdown("### 📈 Indicadores Comerciais")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Contratos", len(contratos))
    col2.metric("Taxa Fechamento", f"{(len(contratos)/len(df_filtro)*100):.1f}%" if len(df_filtro) else "0%")
    col3.metric("⏱ Tempo Médio", f"{tempo_medio:.0f} dias")
    escola_top = df_filtro['nome_escola'].value_counts().idxmax() if not df_filtro.empty else "-"
    col4.metric("Escola + ativa", escola_top)

    # === Gráfico de Pizza e Barra Empilhada ===
    st.markdown("### 📊 Classificação de Leads por Estágio")
    col1, col2 = st.columns(2)

    with col1:
        classificacao = df_filtro['classificacao_lead'].value_counts()
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(classificacao, labels=classificacao.index, autopct='%1.1f%%', colors=cores[:len(classificacao)])
        ax1.set_title("Distribuição de Leads (Pizza)")
        st.pyplot(fig1)

    with col2:
        escolas_por_estado = df_filtro[['estado', 'nome_escola']].dropna().drop_duplicates()
        contagem_estados = escolas_por_estado['estado'].value_counts().sort_values(ascending=False)

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        bars = ax2.bar(contagem_estados.index, contagem_estados.values, color=cores[3], edgecolor='black')
        ax2.set_title("Número de Escolas por Estado")
        ax2.set_ylabel("Total")
        ax2.set_xticks(range(len(contagem_estados)))
        ax2.set_xticklabels(contagem_estados.index, rotation=30, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2, height * 0.95, f'{int(height)}',
                     ha='center', va='top', fontsize=8, color='white')

        plt.tight_layout()
        st.pyplot(fig2)

    # === Potencial financeiro e últimos contatos ===
    st.markdown("### 💰 Potencial e Últimos Contatos")
    col1, col2 = st.columns(2)

    with col1:
        df_pot = df_filtro[df_filtro['potencial_financeiro'] > 0]
        pot = df_pot.groupby("nome_escola")["potencial_financeiro"].mean().sort_values(ascending=False).head(10)
        criar_grafico_barra(pot, "Top Escolas por Potencial", cores[3])

    with col2:
        dias_por_escola = df_filtro.groupby("nome_escola")['data_contato'].max()
        dias_hoje = (pd.to_datetime("today") - dias_por_escola).dt.days
        dias_hoje = dias_hoje[dias_hoje.notna()].sort_values(ascending=False).head(10)
        criar_grafico_barra(dias_hoje, "Dias desde Último Contato", cores[4])

    # === Comunicação e interação ===
    st.markdown("### 📍 Comunicação e Interação")
    col1, col2 = st.columns(2)

    with col1:
        criar_grafico_barra(df_filtro['responsavel'].value_counts(), "Responsáveis", cores[2], reduzir_nome=True)

    with col2:
        criar_grafico_barra(df_filtro['meio_contato'].value_counts(), "Meio de Contato", cores[1])

    # === Temporalidade ===
    st.markdown("### 📅 Temporalidade")
    col1, col2 = st.columns(2)

    with col1:
        criar_grafico_barra(df_filtro['mes_ano'].value_counts().sort_index(), "Contatos por Mês", cores[0])

    with col2:
        top5 = df_filtro['nome_escola'].value_counts().head(5)
        criar_grafico_barra(top5, "Top 5 Escolas por Nº de Interações", cores[5])
    # === 🔁 Funil Comercial ===
    st.markdown("### 🔁 Funil de Conversão")
    col1, col2 = st.columns(2)

    frio = df_filtro[df_filtro['classificacao_lead'].str.contains("Frio", case=False, na=False)]
    morno = df_filtro[df_filtro['classificacao_lead'].str.contains("Morno", case=False, na=False)]
    quente = df_filtro[df_filtro['classificacao_lead'].str.contains("Quente", case=False, na=False)]

    with col1:
        st.metric("Frio ➤ Morno", f"{(len(morno)/len(frio)*100):.1f}%" if len(frio) > 0 else "0%")
        st.metric("Morno ➤ Quente", f"{(len(quente)/len(morno)*100):.1f}%" if len(morno) > 0 else "0%")
        st.metric("Quente ➤ Contrato", f"{(len(contratos)/len(quente)*100):.1f}%" if len(quente) > 0 else "0%")

    with col2:
        if not contratos.empty:
            tempo_medio_fechamento = (
                contratos['data_contato'].max() - contratos['data_contato'].min()
            ).days / len(contratos)
        else:
            tempo_medio_fechamento = 0
        st.metric("⏱ Tempo Médio até Contrato", f"{tempo_medio_fechamento:.0f} dias")
        st.metric("📄 Contratos Assinados", len(contratos))


    # === ☁️ Análise de Texto – WordCloud ===
    st.markdown("### ☁️ Palavras mais citadas nos resumos de interação")

    textos = " ".join(df_filtro['resumo'].dropna().tolist())
    if textos.strip():
        wordcloud = WordCloud(
            width=1000,
            height=400,
            background_color='white',
            stopwords=set(STOPWORDS)
        ).generate(textos)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("Nenhum texto disponível para gerar a nuvem de palavras.")
