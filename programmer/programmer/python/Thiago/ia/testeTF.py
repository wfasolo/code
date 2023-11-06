

from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import tensorflow as tf

dados = pd.read_csv('forca.csv')
forca = []
placar = []

for i in range(len(dados)):
    placar.append([dados['gol_casa'][i], dados['gol_fora'][i]])
    forca.append([dados['forca_c'][i], dados['forca_f'][i]])

forca = np.array(placar)
placar = np.array(forca)

# Definir os dados de entrada e saída
X = forca
y = placar

# Dividir o conjunto de dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42)


# Cria um modelo de Tensorflow

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(16, input_shape=(
        2,), kernel_initializer='random_uniform', activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='selu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(2,activation='linear')
])


# Ajuste a taxa de aprendizado conforme necessário

model.compile(loss='MSE', optimizer='Adamax',
              metrics=['accuracy'])


# Adicionar EarlyStopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='loss', patience=10, restore_best_weights=True)

# Treinar o modelo
history = model.fit(X_train, y_train, epochs=100,
                    batch_size=32, verbose=1,  validation_split=0.2,callbacks=[early_stopping])

# Avaliar o modelo
score = model.evaluate(X_test, y_test,verbose=1)
print("Test loss:", score)
predictions = model.predict(X_test)
mae = np.mean(np.abs(predictions - y_test))
print("Mean Absolute Error:", mae)


model.save('modelo_tf')
