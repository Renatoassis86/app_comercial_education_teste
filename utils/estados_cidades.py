import requests

def carregar_estados():
    """
    Retorna uma lista de tuplas com a sigla e o nome dos estados brasileiros,
    ordenados por nome. Usa a API oficial do IBGE.
    """
    try:
        resposta = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
        if resposta.status_code == 200:
            dados = resposta.json()
            return sorted([(estado["sigla"], estado["nome"]) for estado in dados], key=lambda x: x[1])
        else:
            return []
    except Exception:
        return []

def carregar_cidades(sigla_estado):
    """
    Retorna uma lista de nomes de cidades para o estado especificado pela sigla.
    Usa a API oficial do IBGE.
    """
    try:
        resposta = requests.get(f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla_estado}/municipios")
        if resposta.status_code == 200:
            dados = resposta.json()
            return sorted([cidade["nome"] for cidade in dados])
        else:
            return []
    except Exception:
        return []
