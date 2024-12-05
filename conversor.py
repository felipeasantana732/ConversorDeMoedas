#Importando a biblioteca que faz requisições Web em Python
import requests

#Definindo a chave da API e a URL
API_URL = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY = "0m2AlZMuk5mjLSHccB2OnfTxBJUsc6Hr"

#Função que realiza o GET da api, passando os parametros necessários
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
    
#Função que realiza o GET da api, passando os parametros necessários
def cotacaoAtual(moeda_base, moeda_alvo):
    try:
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


#Função que retorna as moedas que estarão disponiveis no menu suspenso
def Moedas ():
    return [
    "USD - Dólar Americano",
    "EUR - Euro",
    "BRL - Real Brasileiro",
    "JPY - Iene Japonês",
    "GBP - Libra Esterlina",
    "AUD - Dólar Australiano",
    "CAD - Dólar Canadense",
    "CHF - Franco Suíço",
    "CNY - Yuan Chinês",
    "INR - Rúpia Indiana",
    "BTC - Bitcoin"
]