import streamlit as st
import pandas as pd
import math

def carregar():
    st.title("Calculadora de Custos Eskolare")
    st.image("imagens/calculadora.png", use_container_width=True)
    st.subheader("Cidade Viva Education")

    st.sidebar.header("Informações")
    st.sidebar.info("""
    Esta calculadora determina o preço final ao consumidor 
    considerando todas as taxas da Eskolare e a comissão desejada.

    **Taxas aplicadas:**
    - Taxa da plataforma: 1,5%
    - Taxa fixa por parcela: R$ 0,30
    - Taxa do cartão (varia por parcelas)
    - Valor mínimo por parcela: R$ 30,00
    """)

    def obter_taxa_cartao(num_parcelas):
        if num_parcelas == 1:
            return 2.89
        elif 2 <= num_parcelas <= 6:
            return 2.99
        else:
            return 3.69

    def calcular_preco_final(valor_produto, comissao_percent, num_parcelas):
        valor_liquido = valor_produto * (1 + comissao_percent / 100)
        taxa_plataforma = 1.5
        taxa_cartao = obter_taxa_cartao(num_parcelas)
        taxa_fixa_total = 0.30 * num_parcelas
        denominador = 1 - (taxa_plataforma / 100) - (taxa_cartao / 100)
        preco_final = (valor_liquido + taxa_fixa_total) / denominador
        preco_final = math.ceil(preco_final * 100) / 100
        valor_taxa_plataforma = preco_final * (taxa_plataforma / 100)
        valor_taxa_cartao = preco_final * (taxa_cartao / 100)
        total_taxas = valor_taxa_plataforma + valor_taxa_cartao + taxa_fixa_total
        valor_liquido_real = preco_final - total_taxas
        valor_parcela = preco_final / num_parcelas
        parcela_valida = valor_parcela >= 30.00

        return {
            'valor_produto': valor_produto,
            'comissao_percent': comissao_percent,
            'valor_comissao': valor_liquido - valor_produto,
            'valor_liquido_desejado': valor_liquido,
            'num_parcelas': num_parcelas,
            'taxa_plataforma_percent': taxa_plataforma,
            'taxa_cartao_percent': taxa_cartao,
            'taxa_fixa_total': taxa_fixa_total,
            'preco_final': preco_final,
            'valor_taxa_plataforma': valor_taxa_plataforma,
            'valor_taxa_cartao': valor_taxa_cartao,
            'total_taxas': total_taxas,
            'valor_liquido_real': valor_liquido_real,
            'valor_parcela': valor_parcela,
            'parcela_valida': parcela_valida,
            'diferenca': valor_liquido_real - valor_liquido
        }

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Dados de Entrada")
        valor_produto = st.number_input("💼 Valor do Produto (R$)", min_value=0.01, value=1000.00, step=0.01, format="%.2f")
        comissao_percent = st.number_input("📈 Comissão Desejada (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1, format="%.1f")
        num_parcelas = st.selectbox("💳 Número de Parcelas", options=list(range(1, 13)))

    if valor_produto > 0:
        resultado = calcular_preco_final(valor_produto, comissao_percent, num_parcelas)

        with col2:
            st.header("Resultados")
            if resultado['parcela_valida']:
                st.success(f"**Preço Final: R$ {resultado['preco_final']:.2f}**")
                st.info(f"**{num_parcelas}x de R$ {resultado['valor_parcela']:.2f}**")
            else:
                st.error(f"**Preço Final: R$ {resultado['preco_final']:.2f}** ⚠️ Parcela abaixo do mínimo!")
                st.warning(f"**{num_parcelas}x de R$ {resultado['valor_parcela']:.2f}** (Mínimo: R$ 30,00)")

        st.header("Detalhamento dos Cálculos")
        col3, col4, col5 = st.columns(3)

        with col3:
            st.subheader("Valores Base")
            st.metric("Valor do Produto", f"R$ {resultado['valor_produto']:.2f}")
            st.metric("Comissão ({:.1f}%)".format(resultado['comissao_percent']), f"R$ {resultado['valor_comissao']:.2f}")
            st.metric("Líquido Desejado", f"R$ {resultado['valor_liquido_desejado']:.2f}")

        with col4:
            st.subheader("Taxas Aplicadas")
            st.metric("Taxa Plataforma", f"R$ {resultado['valor_taxa_plataforma']:.2f}")
            st.metric("Taxa Cartão", f"R$ {resultado['valor_taxa_cartao']:.2f}")
            st.metric("Taxa Fixa", f"R$ {resultado['taxa_fixa_total']:.2f}")
            st.metric("Total Taxas", f"R$ {resultado['total_taxas']:.2f}")

        with col5:
            st.subheader("✅ Verificação")
            st.metric("Líquido Real", f"R$ {resultado['valor_liquido_real']:.2f}")
            diferenca = resultado['diferenca']
            if abs(diferenca) < 0.01:
                st.success("✅ Cálculo correto!")
            else:
                st.metric("Diferença", f"R$ {diferenca:.2f}")

        # Comparativo de Parcelas
        st.header("Comparativo por Parcelas")
        dados_comparativo = []
        for p in range(1, 13):
            r = calcular_preco_final(valor_produto, comissao_percent, p)
            dados_comparativo.append({
                'Parcelas': f"{p}x" if p > 1 else "À vista",
                'Taxa Cartão (%)': f"{r['taxa_cartao_percent']:.2f}%",
                'Preço Final': f"R$ {r['preco_final']:.2f}",
                'Valor Parcela': f"R$ {r['valor_parcela']:.2f}",
                'Total Taxas': f"R$ {r['total_taxas']:.2f}",
            })

        st.dataframe(pd.DataFrame(dados_comparativo), use_container_width=True)


