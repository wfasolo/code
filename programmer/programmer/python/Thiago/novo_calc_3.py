import numpy as np
import pandas as pd
from scipy.stats import poisson
import matplotlib.pyplot as plt
import os

# Leitura dos dados de ranking dos times a partir da URL fornecida
url = 'c:/bets/tab2.csv'
df = pd.read_csv(url)

# Ordena o dataframe por nome de time
df = df.sort_values(by='nome')

# Função para solicitar entrada do usuário com tratamento de exceções

def get_team(df, prompt):
    while True:
        try:
            name = input(prompt)
            team = df.loc[df['nome'].str.contains(name, case=False)]

            if len(team) == 1:
                return team
            elif len(team) > 1:
                print('Mais de um time encontrado. Selecione o time correto:')
                print(team['nome'])
                indice = int(input("digite o número do indice:"))
                if indice in team.index:
                    row = df.loc[indice]
                    team = pd.DataFrame(row).T
                    return team
                else:
                    print('Índice inválido. Tente novamente.')
            else:
                print('Time não encontrado. Tente novamente.')
        except KeyboardInterrupt:
            print('Operação cancelada pelo usuário.')
            return None

# Função Calculos


def calcular():
    # Solicita o nome do time da casa e procura no dataframe
    time_A = get_team(df, 'Digite o nome do time da casa: ')
    if time_A is None:
        exit()

    # Solicita o nome do time visitante e procura no dataframe
    time_B = get_team(df, 'Digite o nome do time visitante: ')
    if time_B is None:
        exit()

    # Obtém as forças ofensivas e defensivas dos times da casa e visitante a partir do dataframe
    foa = time_A['xG'].values[0]
    fda = time_A['xGA'].values[0]
    fob = time_B['xG'].values[0]
    fdb = time_B['xGA'].values[0]
    print(f'\nfoa: {foa}   fda: {fda}   fob: {fob}   fdb: {fdb}')

    # Calcula a média de gols esperada para cada time
    gol_A = (foa*fdb)*1.05
    gol_B = (fob*fda)

    # Cria matrizes de probabilidades de gols para cada time, usando distribuição de Poisson
    linha = np.around(poisson.pmf(k=range(6), mu=gol_A)*100, decimals=1)
    coluna = np.around(poisson.pmf(k=range(6), mu=gol_B)*100, decimals=1)
    matriz = np.outer(linha, coluna)/100
    g0 = matriz[0][0]
    g1 = g0+matriz[1][0]+matriz[0][1]
    g2 = g1+matriz[2][0]+matriz[1][1]+matriz[0][2]
    g3 = g2+matriz[3][0]+matriz[2][1]+matriz[1][2]+matriz[0][3]
    g4 = g3+matriz[4][0]+matriz[3][1]+matriz[2][0]+matriz[1][3]+matriz[0][4]
    g5 = g4+matriz[5][0]+matriz[4][1]+matriz[4][2] + \
        matriz[3][3]+matriz[2][4]+matriz[5][0]
    under = np.around([g0, g1, g2, g3, g4, g5], 1)
    over = np.around([100-g0, 100-g1, 100-g2, 100-g3, 100-g4, 100-g5], 1)
    # Calcula a probabilidade de vitória, empate e derrota para cada time
    vit_a = np.around(np.sum(np.tril(matriz, k=-1)), 1)
    empate = np.around(np.sum(np.diag(matriz)), 1)
    vit_b = np.around(np.sum(np.triu(matriz, k=1)), 1)

    # Cria um dataframe com as probabilidades de cada placar possível
    placar = pd.DataFrame(np.around(matriz, decimals=1))

    # Cria um dataframe com as probabilidades de cada número de gols para cada time
    gols = pd.DataFrame([linha, coluna, under, over],
                        index=[time_A.nome.values[0], time_B.nome.values[0], 'under', 'over']).T
    return (vit_a, empate, vit_b, gols, placar)

# funcao fraficos


def grafico(dado3, dado4):
    # Mapa de Calor
    calor = np.array(dado4)
    # define a escala de cores
    vmin = calor.min()
    vmax = calor.max()

    # cria um mapa de calor a partir da matriz com as cores invertidas
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10, 6))
    im = ax.imshow(calor, cmap='coolwarm_r', vmin=vmin,
                   vmax=vmax, interpolation='nearest')

    # adiciona os valores de cada célula do mapa
    for i in range(6):
        for j in range(6):
            text = ax.text(j, i, calor[i, j],
                           ha='center', va='center', color='k')

    barra = pd.DataFrame(dado3.values, columns=['a', 'b', 'c', 'd'])

    # adiciona rótulos na parte superior do eixo x
    ax.xaxis.set_ticks_position('top')

    pos = list(range(len(barra)))
    plt.bar(pos, barra['a'], width=0.4, label='Casa')
    plt.bar([p + 0.4 for p in pos], barra['b'], width=0.4, label='Visitante')
    plt.legend(['Casa', 'Visitante'])
    plt.xticks(pos, barra.index)
    plt.show()

# funcao limpar a tela


def limpar_tela():
    os.system('clear' if os.name == 'posix' else 'cls')


# funcao principal
limpar_tela()
while True:
    dados = calcular()

    print("\nProbabilidade de vitoria:")
    print(f'Casa: {dados[0]}   Empate: {dados[1]}   Visitante: {dados[2]}')
    print("\nProbabilidade das Odds:")
    print(
        f'Casa: {round(100/dados[0],2)}   Empate: {round(100/dados[1],2)}   Visitante: {round(100/dados[2],2)}')
    print("\nProbabilidade de gols:")
    print(dados[3])
    print()

    grafico(dados[3], dados[4])
    limpar_tela()
