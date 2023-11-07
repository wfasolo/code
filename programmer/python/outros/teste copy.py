
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from scipy.stats import poisson

mapa = []
placar = []


df = pd.read_csv('forca.csv')
df = df.dropna().reset_index(drop=True)

# Exibe as primeiras linhas do DataFrame

aa = pd.DataFrame([df['0'], df['1']]).T
bb = pd.DataFrame([df['2'], df['3']]).T
aa=aa/10
bb=bb/10
placar = np.array(aa)
mapa = np.array(bb)

print(mapa)


# Definir os dados de entrada e saída
X = mapa
y = placar

# Dividir o conjunto de dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Cria um modelo de regressão linear
model = LinearRegression()

# Treina o modelo usando os dados de treinamento
model.fit(X_train, y_train)

# Usa o modelo para fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# Calcula o coeficiente de determinação (R2) para avaliar a precisão do modelo
score = r2_score(y_test, y_pred)

print("R2 score:", score)

########

# Definir os dados de entrada e saída
X = mapa
y = placar

# Dividir o conjunto de dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Cria um modelo de regressão de floresta aleatória
model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)

# Treina o modelo usando os dados de treinamento
model.fit(X_train, y_train)

# Usa o modelo para fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# Calcula o coeficiente de determinação (R2) para avaliar a precisão do modelo
score = r2_score(y_test, y_pred)

print("R2 score:", score)

###

# Definir os dados de entrada e saída
X = mapa
y = placar

# Dividir o conjunto de dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Cria um modelo de regressão Ridge
model = Ridge(alpha=1.0)

# Treina o modelo usando os dados de treinamento
model.fit(X_train, y_train)

# Usa o modelo para fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# Calcula o coeficiente de determinação (R2) para avaliar a precisão do modelo
score = r2_score(y_test, y_pred)

print("R2 score:", score)
###


# Definir os dados de entrada e saída
X = mapa
y = placar

# Normalizar os dados
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Dividir o conjunto de dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Cria um modelo de rede neural sequencial
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='selu', input_shape=(2,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(2, activation='linear')
])

# Compila o modelo com a função de perda e otimizador
model.compile(loss='MSE',
              optimizer='Adam',metrics='accuracy')

# Treina o modelo usando os dados de treinamento
history = model.fit(X_train, y_train, epochs=50,
                    batch_size=32, validation_data=(X_test, y_test))

# Usa o modelo para fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# Avalia a precisão do modelo no conjunto de teste
score = model.evaluate(X_test, y_test)

print("Test loss:", score)
print(model.predict([[3,1],[1,1],[1.5,2]])*10)
