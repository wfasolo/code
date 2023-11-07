import pandas as pd
import numpy as np


def out1(dados):

    conditions = [dados['scor_A'] < dados['scor_B'],
                  dados['scor_A'] > dados['scor_B']]
    choices1 = [0, 3]
    choices2 = [3, 0]
    dados['resultA'] = np.select(conditions, choices1, default=1)
    dados['resultB'] = np.select(conditions, choices2, default=1)

    c = dados.drop(['equipeB', 'resultB'], axis=1)
    d = dados.drop(['equipeA', 'resultA'], axis=1)

    c = c.rename(
        columns={'equipeA': 'equipe', 'scor_A': 'feito', 'scor_B': 'sofr', 'resultA': 'result'})
    d = d.rename(
        columns={'equipeB': 'equipe', 'scor_B': 'feito', 'scor_A': 'sofr', 'resultB': 'result'})

    dados = pd.concat([c, d], ignore_index=True)
    dados = dados.sort_values(by='rod')
    #dados=dados[dados['rod']>=5]
    dados = dados.dropna()
   
    return dados
