import requests

def buscar_cep(cep):
    cep = cep.replace("-", "").strip()
    if len(cep) != 8:
        return None

    url = f"https://brasilapi.com.br/api/cep/v2/{cep}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        return {
            "rua": dados.get("street", ""),
            "bairro": dados.get("neighborhood", ""),
            "cidade": dados.get("city", ""),
            "estado": dados.get("state", "")
        }
    else:
        return None
