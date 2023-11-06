import pandas as pd
import requests
token = 'eacce4ab67424884b3bf4b79882547da'

lig=['BL1','PL','FL1','PD','SA','BSA']

tab2=pd.DataFrame()
for ii in range(len(lig)):
    camp=lig[ii]
    dados=[]
    uri = 'https://api.football-data.org/v4/competitions/'+camp+'/standings'
    headers = {'X-Auth-Token': 'eacce4ab67424884b3bf4b79882547da'}

    response = requests.get(uri, headers=headers)

    liga = response.json()
    liga = liga['standings'][0]['table']
    tabela = pd.DataFrame(liga)
    
    for i in range(len(tabela)):
        dados.append([tabela['team'][i]['shortName'], tabela['team'][i]['tla']])

    tab=pd.DataFrame(dados,columns=['nome','sigla'])
    tab['off']=round(tabela['goalsFor']/tabela['playedGames'],3)
    tab['def']=round(tabela['goalsAgainst']/tabela['playedGames'],3)
    tab['forca']=round(2-(tabela['goalsFor']/(3*tabela['playedGames'])/(tabela['points']/tabela['goalsAgainst'])),3)
    
    tab2=pd.concat([tab2,tab]).reset_index(drop=True)
tab2.to_csv('c:/bets/tab.csv')

