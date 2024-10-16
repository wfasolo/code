

def out2(dados2):
    dados2['pontos'] = dados2.groupby(['equipe'])['result'].cumsum()
    dados2['g_pro'] = dados2.groupby(['equipe'])['feito'].cumsum()
    dados2['g_con'] = dados2.groupby(['equipe'])['sofr'].cumsum()
    mask = (dados2['result'] == 3)
    dados2['soma_vit'] = mask.groupby(dados2['equipe']).cumsum()

    dados2 = dados2.fillna(0)

    dados2['off'] = round(dados2['g_pro']/(dados2['rod']), 2)
    dados2['def'] = round(dados2['g_con']/(dados2['rod']), 2)
    dados2['soma_vit'] = round(dados2['soma_vit']/(dados2['rod']), 2)

    dados2['off'] = dados2['off'].rolling(window=5).mean()
    dados2['def'] = dados2['def'].rolling(window=5).mean()
    dados2 = dados2.dropna()

    dados2 = dados2.drop(['feito', 'sofr', 'result'], axis=1)
    dados2 = dados2.sort_values(['rod', 'pontos'], ascending=[True, False])
    
    return dados2
