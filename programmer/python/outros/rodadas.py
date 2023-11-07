# https://www.football-data.org/documentation/quickstart
import pandas as pd
import requests
import time

simular=pd.DataFrame()
def func_dados(campeonato, matchday):
    url = f'http://api.football-data.org/v4/competitions/{campeonato}/matches?matchday={matchday}'
    headers = {'X-Auth-Token': 'eacce4ab67424884b3bf4b79882547da'}
    response = requests.get(url, headers=headers)
    data = response.json()
    matches = data['matches']
    return matches


def func_rodadas(jogos):
    global simular
    rodada = []

    for i in range(len(jogos)):
        casa = jogos[i]['homeTeam']['name']
        vist = jogos[i]['awayTeam']['name']
        p_casa = jogos[i]['score']['fullTime']['home']
        p_vist = jogos[i]['score']['fullTime']['away']
        if p_casa != None:
            n_jogo = 1
            if p_casa > p_vist:
                ponto_c = 3
                ponto_v = 0
            elif p_casa < p_vist:
                ponto_c = 0
                ponto_v = 3
            elif p_casa == p_vist:
                ponto_c = 1
                ponto_v = 1
        else:
            ponto_c = 0
            ponto_v = 0
            p_casa = 0
            p_vist = 0
            n_jogo = 0

        rodada.append([casa, vist, p_casa, p_vist, ponto_c, ponto_v, n_jogo])

        ofc = antiga.loc[casa, 'ofe']
        dfc = antiga.loc[casa, 'dfe']
        ofv = antiga.loc[vist, 'ofe']
        dfv = antiga.loc[vist, 'dfe']

        sim=pd.DataFrame([ponto_c,p_vist,round(ofc*dfv,1),round(ofv*dfc,1)]).T

        simular = pd.concat([simular, sim], ignore_index=True)
     
     
    return rodada


def func_tabela_rodada(rodada):
    result = pd.DataFrame(rodada, columns=[
        'casa', 'vist', 'placar_casa', 'placar_vist', 'ponto_casa', 'ponto_vist', 'jogos'])

    result_c = pd.DataFrame([result['casa'].values, result['placar_casa'].values,
                            result['placar_vist'].values, result['ponto_casa'].values, result['jogos'].values]).T
    result_v = pd.DataFrame([result['vist'].values, result['placar_vist'].values,
                            result['placar_casa'].values, result['ponto_vist'].values, result['jogos'].values]).T

    tab = pd.concat([result_c, result_v])
    tab = tab.rename(columns={0: 'Equipe', 1: 'gol_pro', 2: 'gol_con', 3: 'Pontos', 4: 'Jogos'}).sort_values(
        'Equipe').reset_index(drop=True)

    return tab


antiga = pd.read_csv('dados.csv',sep=';')
print(antiga)
antiga['ofe'] = antiga['gol_pro']/antiga['Jogos']
antiga['dfe'] = antiga['gol_con']/antiga['Jogos']
antiga = antiga.set_index('Equipe')
print(f'Rodada: 1')
print(antiga.sort_values('Pontos', ascending=False))

for i in range(1, 34):

    nova = func_tabela_rodada(func_rodadas(func_dados(2021, i)))
    nova = nova.set_index('Equipe')
    antiga = antiga.add(nova)
    antiga['ofe'] = antiga['gol_pro']/antiga['Jogos']
    antiga['dfe'] = antiga['gol_con']/antiga['Jogos']

    time.sleep(7)
    print(f'\nRodada: {i}')
    print(antiga.sort_values('Pontos', ascending=False))
    print(simular)
simular.to_csv('forca.csv')
