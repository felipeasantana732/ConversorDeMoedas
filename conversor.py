import requests

API_URL = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY = "0m2AlZMuk5mjLSHccB2OnfTxBJUsc6Hr"

def ApiConverte(valor, de, para):
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": API_KEY}
    params = {"to": para , "from": de, "amount": valor}
    resposta = requests.get(url, headers=headers, params=params)

    if resposta.status_code == 200:
        dados = resposta.json()
        return dados["result"]
    else:
        raise Exception("Erro ao buscar taxas de câmbio.", dados)
    

def cotacaoAtual(moeda_base, moeda_alvo):
    try:
        # URL da API de câmbio com chave de API (substitua 'YOUR_API_KEY' por sua chave de API)
        url = f"https://api.exchangerate-api.com/v4/latest/{moeda_base}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            cotacao = data['rates'].get(moeda_alvo)
            if cotacao is not None:
                return cotacao
            else:
                raise ValueError(f"Não foi possível encontrar a cotação para {moeda_alvo}.")
        else:
            raise Exception(f"Erro ao buscar a cotação: {data.get('error', 'Erro desconhecido')}")
    except Exception as e:
        return str(e)
