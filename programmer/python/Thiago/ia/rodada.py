import requests
import pandas as pd
import numpy as np

equipes = pd.read_csv('equipes.csv')
url = "http://api.football-data.org/v4/competitions/BSA/matches"
headers = {"X-Unfold-Goals": "true",
           "X-Auth-Token": "eacce4ab67424884b3bf4b79882547da"}

response = requests.get(url, headers=headers)
matches = response.json()
matches = matches['matches']

############
tab = []
for i in range(len(matches)):
    tab.append([matches[i]['competition']['id'], matches[i]['matchday'], matches[i]['homeTeam']['id'], matches[i]
               ['awayTeam']['id'], matches[i]['score']['fullTime']['home'], matches[i]['score']['fullTime']['away'], matches[i]
               ['homeTeam']['shortName'], matches[i]['awayTeam']['shortName']])

df = pd.DataFrame(
    tab, columns=['comp', 'rodada', 'casa', 'fora', 'gol_casa', 'gol_fora', 'equipeA', 'equipeB'])
ult=df
df = df.dropna()

############
tab2 = []
df5 = pd.DataFrame()

for i in list(equipes['id']):
    df2 = pd.DataFrame()
    df2['id'] = df[df['casa'] == i]['casa']
    df2['rodada'] = df[df['casa'] == i]['rodada']
    df2['pro'] = df[df['casa'] == i]['gol_casa']
    df2['contra'] = df[df['casa'] == i]['gol_fora']

    df3 = pd.DataFrame()
    df3['id'] = df[df['fora'] == i]['fora']
    df3['rodada'] = df[df['fora'] == i]['rodada']
    df3['pro'] = df[df['fora'] == i]['gol_fora']
    df3['contra'] = df[df['fora'] == i]['gol_casa']

    df4 = pd.concat([df2, df3]).sort_values(by=['rodada', 'id'])
    df4['pro'] = df4['pro'].cumsum()
    df4['contra'] = df4['contra'].cumsum()
    df4['off'] = round(df4['pro']/df4['rodada'], 2)
    df4['def'] = round(df4['contra']/df4['rodada'], 2)
    df4['rodada'] = df4['rodada']+1
    df5 = pd.concat([df5, df4])

df5 = df5.reset_index(drop=True)

ultima = ult.loc[ult['rodada'] == df5['rodada'].max()]
ultima = ultima.drop(['gol_casa', 'gol_fora'], axis=1)


for index, row in df5.iterrows():
    mask = (ultima['rodada'] == row['rodada']) & (ultima['casa'] == row['id'])
    ultima.loc[mask, 'offc'] = row['off']
    ultima.loc[mask, 'defc'] = row['def']

    mask = (ultima['rodada'] == row['rodada']) & (ultima['fora'] == row['id'])
    ultima.loc[mask, 'offf'] = row['off']
    ultima.loc[mask, 'deff'] = row['def']

ultima['forca_c'] = round(ultima['offc']*ultima['deff'], 2)
ultima['forca_f'] = round(ultima['offf']*ultima['defc'], 2)
print(ultima)
ultima.to_csv('ultima.csv')
