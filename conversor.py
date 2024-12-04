import requests

API_URL = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY = "SUA_CHAVE_API"

def converte_moeda(valor, de, para):
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": API_KEY}
    params = {"from": de, "to": para, "amount": valor}
    resposta = requests.get(url, headers=headers, params=params)

    if resposta.status_code == 200:
        dados = resposta.json()
        return dados["result"]
    else:
        raise Exception("Erro ao buscar taxas de câmbio.")
