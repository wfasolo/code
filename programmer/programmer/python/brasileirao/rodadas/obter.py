import requests
import pandas as pd


def obt(liga,ano):

    url = "http://api.football-data.org/v4/competitions/" + \
        str(liga)+"/matches?season="+str(ano)
    headers = {
        "X-Unfold-Goals": "true",
        "X-Auth-Token": "eacce4ab67424884b3bf4b79882547da"
    }

    response = requests.get(url, headers=headers)
    matches = response.json()
    matches = matches['matches']

    # seleção dos campos desejados
    tab = [
        [
            match['matchday'],
            match['homeTeam']['shortName'],
            match['awayTeam']['shortName'],
            match['score']['fullTime']['home'],
            match['score']['fullTime']['away']
        ]
        for match in matches
    ]
    df = pd.DataFrame(tab, columns=['rod', 'equipeA',
                                    'equipeB', 'scor_A', 'scor_B']).reset_index(drop=True)

    df2 = df.dropna().reset_index(drop=True)
    df2['scor_A'] = df2['scor_A'].astype(int)
    df2['scor_B'] = df2['scor_B'].astype(int)
    df3 = df[df['rod'] > df2['rod'].max()].reset_index(drop=True)

    return (df2, df3)
