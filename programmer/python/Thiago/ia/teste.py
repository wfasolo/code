
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import pandas as pd
import numpy as np
import tensorflow as tf

tabela = pd.read_csv('forca.csv')
mapa = []
placar = []

for i in range(len(tabela)):
    placar.append([tabela['gol_casa'][i], tabela['gol_fora'][i]])
    mapa.append([tabela['forca_c'][i], tabela['forca_f'][i]])

mapa = np.array(placar)
placar = np.array(mapa)

# Definir os dados de entrada e saída
X = mapa
y = placar

# Dividir o conjunto de dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


# 1 Cria um modelo de MLPRegressor

mlp_regressor = MLPRegressor(hidden_layer_sizes=(
    100, 50), max_iter=10, random_state=42)
mlp_regressor.fit(X_train, y_train)
predictions = mlp_regressor.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("1 Mean Squared Error:", mse)
score = r2_score(y_test, predictions)
print("R2 score:", score)

# 2 Cria um modelo de regressão linear

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)
print("2 R2 score:", score)

# 3 Cria um modelo de RandomForestRegressor

model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)
print("3 R2 score:", score)

# 4 Cria um modelo de Ridge

model = Ridge(alpha=1.0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)
print("4 R2 score:", score)

# 5 Cria um modelo de Tensorflow

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(2, activation='selu', input_shape=(2,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(2, activation='elu')
])

model.compile(loss=tf.keras.losses.MeanSquaredError(),
              optimizer="Adamax",metrics='accuracy')
history = model.fit(X_train, y_train, epochs=50, batch_size=16,
                    verbose=1)
y_pred = model.predict(X_test)
score = model.evaluate(X_test, y_test)
print("5 Test loss:", score)
