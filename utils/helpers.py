import streamlit as st
import base64
from pathlib import Path

def exibir_banner(nome_base):
    extensoes = ['.jpeg', '.jpg', '.png']
    for ext in extensoes:
        caminho = Path(f"{nome_base}{ext}")
        if caminho.exists():
            with open(caminho, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f'<img class="banner-img" src="data:image/{ext[1:]};base64,{encoded}">',
                unsafe_allow_html=True
            )
            return
    st.warning(f"Banner '{nome_base}' não encontrado.")

# utils/helpers.py

def limpar_formulario():
    import streamlit as st
    st.session_state["form_limpar"] = True



def calcular_potencial_financeiro(qtd_infantil, qtd_fund1, qtd_fund2, qtd_medio):
    # Exemplo de cálculo
    return (
        qtd_infantil * 500 +
        qtd_fund1 * 600 +
        qtd_fund2 * 700 +
        qtd_medio * 800
    )

def calcular_probabilidade(interesses, prontidao, abertura, encaminhamentos):
    # Exemplo ajustado considerando múltiplos encaminhamentos
    peso = {
        "Muito Baixo": 1, "Baixo": 2, "Médio": 3, "Alto": 4, "Muito Alto": 5
    }
    peso_prontidao = {
        "Negociação Parada": 1, "Nova Reunião Necessária": 2,
        "Esperando Retorno": 3, "Apresentação em Andamento": 4,
        "Contrato Enviado": 5, "Atualizar Contrato": 6, "Contrato Assinado": 7
    }
    peso_abertura = {"N": 1, "S": 3}
    
    peso_enc = len(encaminhamentos) if encaminhamentos else 1

    return min(100, int(
        (peso.get(interesses, 0) + peso_prontidao.get(prontidao, 0) + peso_abertura.get(abertura, 0)) * peso_enc
    ))

def calcular_classificacao(probabilidade, potencial):
    if probabilidade >= 80 and potencial >= 20000:
        return "Lead Quente"
    elif probabilidade >= 50 and potencial >= 10000:
        return "Lead Morno"
    else:
        return "Lead Frio"
