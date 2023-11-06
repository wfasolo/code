# https://docs.betting-api.com/1xbet/index.html#api-Football-FootballLiveById
import requests
import json
import pandas as pd
jogos_aovivo = 'https://api.betting-api.com/1xbet/football/live/all'

headers = {
    "Authorization": "Bearer f28d7c2d50964622bc0b3f85069b991020243583017b42658ad86821aa5549dc"}

response = requests.get(jogos_aovivo, headers=headers)

data = response.json()

dados = json.dumps(data, indent=2)

dados2 = pd.DataFrame(data)
dados2=dados2.dropna()
dadosdrop = dados2.drop(columns=['team2_rus',  'team2_id', 'id', 'team1', 'team2', 'title', 'league',
                              'team1_rus', 'team1_id',  'country', 'hash', 'actual_at', 'href', 'date_start'])
#print(dados2.columns)
dados3=pd.DataFrame(dados2.stats.values)
dados4=dados3[0][0]

dados4['id']=dados2.id[0]
dados4['league']=dados2.league[0]
dados4['team1']=dados2.team1[0]
dados4['score1']=dados2.score1[0]
dados4['team2']=dados2.team2[0]
dados4['score2']=dados2.score2[0]
dados4['minute']=dados2.minute[0]
dados4['seconds']=dados2.seconds[0]
print(pd.DataFrame(list(dados4.items())))
print(dados2.id)