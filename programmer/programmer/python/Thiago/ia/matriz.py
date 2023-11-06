import pandas as pd
import numpy as np
from scipy.stats import poisson

tabela = pd.read_csv('forca.csv')  
gol_A=tabela['forca_c']
gol_B=tabela['forca_f']

dados=[]
for i in range(len(tabela)):
    # Cria matrizes de probabilidades de gols para cada time, usando distribuição de Poisson
    linha = np.around(poisson.pmf(k=range(6), mu=gol_A[i])*100, decimals=1)
    coluna = np.around(poisson.pmf(k=range(6), mu=gol_B[i])*100, decimals=1)
    matriz = np.outer(linha, coluna)/100
    dados.append(matriz)
   
array_d=np.array(dados)
print(array_d[0][0])
np.save('matriz.npy',array_d)
