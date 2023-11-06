

def out2(dados2):
    dados2['pontos'] = dados2.groupby(['equipe'])['result'].cumsum()
    dados2['g_pro'] = dados2.groupby(['equipe'])['feito'].cumsum()
    dados2['g_con'] = dados2.groupby(['equipe'])['sofr'].cumsum()
    
    dados2['g_p_c'] = dados2[dados2['local'] == 1].groupby('equipe')['feito'].cumsum()
    dados2['g_p_f'] = dados2[dados2['local'] == 2].groupby('equipe')['feito'].cumsum()

    dados2['g_c_c'] = dados2[dados2['local'] == 1].groupby('equipe')['sofr'].cumsum()
    dados2['g_c_f'] = dados2[dados2['local'] == 2].groupby('equipe')['sofr'].cumsum()

    dados2['jogos_c'] = dados2[dados2['local'] == 1].groupby('equipe')['local'].cumsum()
    dados2['jogos_f'] = dados2[dados2['local'] == 2].groupby('equipe')['local'].cumsum()/2

    dados2['off'] = round(dados2['g_pro']/(dados2['rod']), 2)
    dados2['def'] = round(dados2['g_con']/(dados2['rod']), 2)
    
    dados2['off_c'] = round(dados2['g_p_c']/(dados2['jogos_c']), 2)
    dados2['def_c'] = round(dados2['g_c_c']/(dados2['jogos_c']), 2)

    dados2['off_f'] = round(dados2['g_p_f']/(dados2['jogos_f']), 2)
    dados2['def_f'] = round(dados2['g_c_f']/(dados2['jogos_f']), 2)
    
    dados2['off_c'] = dados2['off_c'].rolling(window=4).mean()
    dados2['def_c'] = dados2['def_c'].rolling(window=4).mean()
    dados2['off_f'] = dados2['off_f'].rolling(window=4).mean()
    dados2['def_f'] = dados2['def_f'].rolling(window=4).mean()

    dados2 = dados2.fillna(0)

    dados2 = dados2.dropna()

    dados2 = dados2.drop(['feito', 'sofr', 'result'], axis=1)
    dados2 = dados2.sort_values(['rod', 'pontos'], ascending=[True, False])
    
    return dados2
