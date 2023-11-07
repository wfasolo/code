import requests
import pandas as pd

def func_equipe(campeonato,ano):
    url = "http://api.football-data.org/v4/competitions/"+str(campeonato)+"/teams?season="+str(ano)
    headers = {"X-Unfold-Goals": "true",
            "X-Auth-Token": "eacce4ab67424884b3bf4b79882547da"}

    response = requests.get(url, headers=headers)
    times = response.json()
    tab = []
    for i in range(len(times['teams'])):
        tab.append([times['competition']['id'], times['teams']
                [i]['id'], times['teams'][i]['shortName']])

    tabela = pd.DataFrame(tab, columns=['competicao', 'id', 'equipe'])
    #print(tabela)
    #tabela.to_csv('equipes.csv')
    return tabela

