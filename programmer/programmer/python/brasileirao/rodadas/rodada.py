import pandas as pd
import numpy as np
from scipy.stats import poisson


def rodar(i, df3, df4):
   
    eqA = df3['equipeA'][i]
    eqB = df3['equipeB'][i]
    off_A = df4[df4['equipe'] == eqA]['off'].values[0]
    off_B = df4[df4['equipe'] == eqB]['off'].values[0]
    def_A = df4[df4['equipe'] == eqA]['def'].values[0]
    def_B = df4[df4['equipe'] == eqB]['def'].values[0]
    s_v_A = df4[df4['equipe'] == eqA]['soma_vit'].values[0]
    s_v_B = df4[df4['equipe'] == eqB]['soma_vit'].values[0]
    gol_A = off_A * def_B * 0.05
    gol_B = off_B * def_A * 0.05

    resul_A = np.random.poisson(off_A, 5)
    resul_A = [x for x in resul_A if x <= 4]

    probab_A = np.around(poisson.pmf(
        k=resul_A, mu=gol_A)*100, decimals=1)

    prob_A = pd.DataFrame([resul_A, probab_A]).T
    prob_A = prob_A.groupby(0).sum()

    resul_B = np.random.poisson(off_B, 5)
    resul_B = [x for x in resul_B if x <= 4]

    probab_B = np.around(poisson.pmf(
        k=resul_B, mu=gol_B)*100, decimals=1)
    prob_B = pd.DataFrame([resul_B, probab_B]).T
    prob_B = prob_B.groupby(0).sum()

    ga = prob_A.idxmax()[1]
    gb = prob_B.idxmax()[1]

    df3.loc[i, 'scor_A'] = ga
    df3.loc[i, 'scor_B'] = gb

    return df3
