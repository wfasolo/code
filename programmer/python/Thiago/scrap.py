import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página com a tabela de xG
url = 'https://footystats.org/brazil/serie-a/xg'
agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.'}

# Fazer a requisição HTTP
response = requests.get(url, headers=agent)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    tabela = soup.find(
        "table", {"class": "full-league-table table-sort xg-all mobify-table"})

    # Extrair os dados da tabela
    dados = []
    linhas = tabela.find_all("tr")

    for linha in linhas:
        colunas = linha.find_all("td")
        dados_linha = [col.text.strip() for col in colunas]
        if len(dados_linha) == 50:
            dados.append([dados_linha[2][:25], dados_linha[44],
                         dados_linha[45], dados_linha[47], dados_linha[48]])

df = pd.DataFrame(dados, columns=['nome', 'xG', 'xGA', 'off', 'def'])


print(df)
df.to_csv('c:/bets/tab2.csv')
