import requests
import pandas as pd
import numpy as np
import equipes as eq
import time

ano = [2023, 2022, 2021, 2020]
ligas = [2013, 2016, 2021, 2001, 2018, 2015,
         2002, 2019, 2003, 2017, 2152, 2014]
final = pd.DataFrame()

for iii in range(len(ano)):
    for ii in range(len(ligas)):
        try:
            print(ano[iii])
            equipes = eq.func_equipe(ligas[ii], ano[iii])
            print(equipes)

            url = "http://api.football-data.org/v4/competitions/" + \
                str(ligas[ii])+"/matches?season="+str(ano[iii])
            headers = {
                "X-Unfold-Goals": "true",
                "X-Auth-Token": "eacce4ab67424884b3bf4b79882547da"
            }

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
                tab, columns=['competicao', 'rodada', 'casa', 'fora', 'gol_casa', 'gol_fora', 'equipeA', 'equipeB'])

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

            for i in list(equipes['id']):
                pro_casa = df[df['casa'] == i]['gol_casa'].sum()
                pro_fora = df[df['fora'] == i]['gol_fora'].sum()
                contra_casa = df[df['casa'] == i]['gol_fora'].sum()
                contra_fora = df[df['fora'] == i]['gol_casa'].sum()
                equipe = equipes[equipes['id'] == i]['equipe']
                tab2.append([equipe.values[0], int(pro_casa), int(pro_fora), int(contra_casa), int(
                    contra_fora), int(pro_casa+pro_fora), int(contra_casa+contra_fora)])

            df2 = pd.DataFrame(tab2, columns=['equipe', 'pro_casa', 'pro_fora',
                                              'contra_casa', 'contra_fora', 'gols_pro', 'gols_contra'])

            for index, row in df5.iterrows():
                mask = (df['rodada'] == row['rodada']) & (
                    df['casa'] == row['id'])
                df.loc[mask, 'offc'] = row['off']
                df.loc[mask, 'defc'] = row['def']
                mask = (df['rodada'] == row['rodada']) & (
                    df['fora'] == row['id'])
                df.loc[mask, 'offf'] = row['off']
                df.loc[mask, 'deff'] = row['def']

            df['forca_c'] = round(df['offc']*df['deff'], 2)
            df['forca_f'] = round(df['offf']*df['defc'], 2)

            # Use numpy.select para criar a nova coluna 'resultado'
            conditions = [df['gol_casa'] > df['gol_fora'],
                          df['gol_casa'] < df['gol_fora']]

            choices = [0, 1]
            df['resultado'] = np.select(conditions, choices, default=2)

            df['gol_casa'] = df['gol_casa'].astype(int)
            df['gol_fora'] = df['gol_fora'].astype(int)
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df = df.dropna()
            df = df.loc[df['rodada'] >= 10]
            final = pd.concat([final, df])
            print(df)
            time.sleep(61)
        except:
            print(f"Erro")
            time.sleep(61)
            continue


final.to_csv('forca.csv')

print(final.tail(20))
