import pandas as pd
import numpy as np
import tensorflow as tf

# Carregar dados
dados = pd.read_csv('ultima.csv')
print(dados)

# Carregar modelo
modelo = tf.keras.models.load_model('modelo_tf')

# Preparar dados de entrada
entradas = []
for i in range(len(dados)):
    entradas.append([dados['forca_c'][i], dados['forca_f'][i]])
    
entradas = np.array(entradas)

# Fazer previsões
previsoes = modelo.predict(entradas)
previsoes_arredondadas = np.round(pd.DataFrame(previsoes), 0)

# Adicionar previsões à tabela
dados['golA'] = previsoes_arredondadas[0].astype(int)
dados['golB'] = previsoes_arredondadas[1].astype(int)

# Exibir resultados
resultados = pd.DataFrame({
    'Equipe A': dados['equipeA'],
    'Gol A': dados['golA'],
    'Gol B': dados['golB'],
    'Equipe B': dados['equipeB']
})
print(resultados)
