# https://www.football-data.org/documentation/quickstart
url = 'https://api.api-futebol.com.br/v1/campeonatos/10/fases/317'
import requests
import pandas as pd


url = 'http://api.football-data.org/v4/competitions/'
headers = {'X-Auth-Token': 'eacce4ab67424884b3bf4b79882547da'}


response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    # faça o que precisar com os dados retornados em JSON
else:
    print('Erro ao acessar a API:', response.status_code)


b=data['competitions']

print(b[0])
for i in range(len(b)):
    id=b[i]['id']
    campeonato=b[i]['name']
    rodadas=b[i]['currentSeason']['currentMatchday']
    print(id,campeonato,rodadas)

