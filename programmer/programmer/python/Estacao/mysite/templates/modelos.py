import numpy as np
import matplotlib.pyplot as plt
import leitura
import correcao
import prepro
import KNeighbors
import SVC
import Florest
import graficos

leit = leitura.ler()

corrige = correcao.corrigir(leit)

prepara = prepro.dados(corrige, leit['estacao'])

dados_KN = KNeighbors.valor(prepara['X_train'],
                            prepara['X_test'],
                            prepara['y_train'],
                            prepara['y_test'],
                            prepara['prev_trans'])

dados_SVC = SVC.valor(prepara['X_train'],
                      prepara['X_test'],
                      prepara['y_train'],
                      prepara['y_test'],
                      prepara['prev_trans'])

dados_FL = Florest.valor(prepara['X_train'],
                         prepara['X_test'],
                         prepara['y_train'],
                         prepara['y_test'],
                         prepara['prev_trans'])

graficos.graf(corrige['corrigido'])


#print(dados_mu.idxmax(),  dados_mu.max())
#print(dados_mu2.idxmax(), dados_mu2.max())
#print(dados_mu3.idxmax(), dados_mu3.max())
