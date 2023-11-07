# https://docs.betting-api.com/1xbet/index.html#api-Football-FootballLiveById
import requests
import json
import pandas as pd
ligas_ativas = 'https://api.betting-api.com/1xbet/football/live/leagues'
todas_as_ligas = 'https://api.betting-api.com/1xbet/football/line/leagues'
jogos_aovivo = 'https://api.betting-api.com/1xbet/football/live/all'
proximos_jogos = 'https://api.betting-api.com/1xbet/football/line/all'
jogo = 'https://api.betting-api.com/1xbet/football/live/436671368'
headers = {
    "Authorization": "Bearer f28d7c2d50964622bc0b3f85069b991020243583017b42658ad86821aa5549dc"}

response = requests.get(jogos_aovivo, headers=headers)

data = response.json()

dados = json.dumps(data, indent=2)
dados2 = pd.DataFrame(data)
dados2=dados2.dropna()
dados2 = dados2.drop(columns=['team2_rus',  'team2_id', 'id', 'team1', 'team2', 'title', 'league',
                              'team1_rus', 'team1_id',  'country', 'hash', 'actual_at', 'href', 'date_start'])
print(dados2.columns)
print(dados2)
