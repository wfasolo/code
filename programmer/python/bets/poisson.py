from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
import pandas as pd
from scipy.stats import poisson
import matplotlib.pyplot as plt
url = 'https://projects.fivethirtyeight.com/soccer-api/club/spi_global_rankings.csv'
df = pd.read_csv(url)
df = df.sort_values(by='name')
ta = input('digite o nome do time A: ')
ta = df.loc[df['name'].str.contains(ta, case=False)]
if len(ta) > 1:
    print(ta)
    ta = input('digite o nome do time A: ')
    ta = df.loc[df['name'].str.contains(ta, case=False)]
tb = input('digite o nome do time B: ')
tb = df.loc[df['name'].str.contains(tb, case=False)]
if len(tb) > 1:
    print(tb)
    tb = input('digite o nome do time B: ')
    tb = df.loc[df['name'].str.contains(tb, case=False)]
foa = ta['off'].values[0]
fda = ta['def'].values[0]
fob = tb['off'].values[0]
fdb = tb['def'].values[0]

ga = (foa*fdb)*1.05
gb = (fob*fda)*0.95


# Definir média de gols para cada time

linha = np.around(poisson.pmf(k=range(6), mu=ga)*100, decimals=1)
coluna = np.around(poisson.pmf(k=range(6), mu=gb)*100, decimals=1)
matriz = np.outer(linha, coluna)/100
vit_a = np.sum(np.tril(matriz, k=-1))
empate = np.sum(np.diag(matriz))
vit_b = np.sum(np.triu(matriz, k=1))
matriz = np.around(matriz, decimals=1)
print('Probabilidade de gols de cada time:')
print(pd.DataFrame([linha, coluna],
      index=[ta.name.values[0], tb.name.values[0]]).T)
print()
print("Chance de Vitoria:")
print(
    f'{ta.name.values[0]}: {round(vit_a,1)} / empate: {round(empate,1)} / {tb.name.values[0]}: {round(vit_b,1)}')
print()
print("Odds:")
print(
    f'{ta.name.values[0]}: {round(100/vit_a,1)} / empate: {round(100/empate,1)} / {tb.name.values[0]}: {round(100/vit_b,2)}')


def fechar_janelas():
    plt.close()
    root.destroy()


# define a escala de cores
vmin = matriz.min()
vmax = matriz.max()

# cria um mapa de calor a partir da matriz com as cores invertidas
fig, ax = plt.subplots(figsize=(8, 8))
im = ax.imshow(matriz, cmap='coolwarm_r', vmin=vmin,
               vmax=vmax, interpolation='nearest')

# adiciona os valores de cada célula do mapa
for i in range(6):
    for j in range(6):
        text = ax.text(j, i, matriz[i, j], ha='center', va='center', color='k')


# adiciona rótulos na parte superior do eixo x
ax.xaxis.set_ticks_position('top')

# adiciona um título ao mapa de calor
plt.title(
    f'{ta.name.values[0]}: {round(vit_a,1)}({round(100/vit_a,1)}) / empate: {round(empate,1)}({round(100/empate,1)}) / {tb.name.values[0]}: {round(vit_b,1)}({round(100/vit_b,2)})', y=1.1)

# cria uma janela do Tkinter
root = tk.Tk()

# cria um widget Frame para o mapa de calor
frame = tk.Frame(root)

# cria uma instância do FigureCanvasTkAgg com a figura do mapa de calor
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()

# adiciona o widget Frame ao layout do Tkinter
frame.pack()

# exibe o mapa de calor na janela do Tkinter
canvas.get_tk_widget().pack()

# conecta a função ao evento de fechamento da janela do Tkinter
root.protocol("WM_DELETE_WINDOW", fechar_janelas)


# inicia o loop principal do Tkinter
root.mainloop()
