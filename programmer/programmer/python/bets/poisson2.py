import numpy as np

# Médias de gols para cada time
ataque_A = 2.2
defesa_A = 1.24
ataque_B = 2.88
defesa_B = 1.08

# Função para calcular as probabilidades de gols
def prob_gols(media):
    # Distribuição de Poisson
    prob = [np.exp(-media)]
    for i in range(1, 15):
        prob.append((media**i) / np.math.factorial(i) * np.exp(-media))
    return prob

# Probabilidades de gols para cada time
gols_A = prob_gols(ataque_A * defesa_B)
gols_B = prob_gols(ataque_B * defesa_A)

# Função para calcular as probabilidades de resultados
def prob_resultados(gols_time_1, gols_time_2):
    resultado = np.zeros((len(gols_time_1), len(gols_time_2)))
    for i in range(len(gols_time_1)):
        for j in range(len(gols_time_2)):
            resultado[i,j] = gols_time_1[i] * gols_time_2[j]
    return resultado / np.sum(resultado)

# Probabilidades de resultados
probabilidades = prob_resultados(gols_A, gols_B)

# Simulação Monte Carlo de 10.000 jogos
vitorias_A = 0
vitorias_B = 0
empates = 0
jogos = 10000

for i in range(jogos):
    resultado_jogo = np.random.choice(np.ravel(probabilidades), p=np.ravel(probabilidades))
    resultado_ij = np.argwhere(probabilidades == resultado_jogo)
    gols_A = resultado_ij[0][0]
    gols_B = resultado_ij[0][1]
    if gols_A > gols_B:
        vitorias_A += 1
    elif gols_B > gols_A:
        vitorias_B += 1
    else:
        empates += 1

# Chances de vitória e empate
chance_vitoria_A = vitorias_A / jogos
chance_vitoria_B = vitorias_B / jogos
chance_empate = empates / jogos

print("Chances de vitória do time A: {:.2%}".format(chance_vitoria_A))
print("Chances de vitória do time B: {:.2%}".format(chance_vitoria_B))
print("Chances de empate: {:.2%}".format(chance_empate))



import numpy as np

# Médias de gols para cada time
ataque_A = 2.2
defesa_A = 1.24
ataque_B = 2.88
defesa_B = 1.08

# Função para calcular as probabilidades de gols
def prob_gols(media):
    # Distribuição de Poisson
    prob = [np.exp(-media)]
    for i in range(1, 15):
        prob.append((media**i) / np.math.factorial(i) * np.exp(-media))
    return prob

# Probabilidades de gols para cada time
gols_A = prob_gols(ataque_A * defesa_B)
gols_B = prob_gols(ataque_B * defesa_A)

# Função para calcular as probabilidades de resultados
def prob_resultados(gols_time_1, gols_time_2):
    resultado = np.zeros((len(gols_time_1), len(gols_time_2)))
    for i in range(len(gols_time_1)):
        for j in range(len(gols_time_2)):
            resultado[i,j] = gols_time_1[i] * gols_time_2[j]
    return resultado / np.sum(resultado)

# Probabilidades de resultados
probabilidades = prob_resultados(gols_A, gols_B)

# Calcula a chance de sair de 0 a 5 gols
chance_0_gols = probabilidades[0, 0] * 100
chance_1_gol = (probabilidades[1, 0] + probabilidades[0, 1]) * 100
chance_2_gols = (probabilidades[2, 0] + probabilidades[1, 1] + probabilidades[0, 2]) * 100
chance_3_gols = (probabilidades[3, 0] + probabilidades[2, 1] + probabilidades[1, 2] + probabilidades[0, 3]) * 100
chance_4_gols = (probabilidades[4, 0] + probabilidades[3, 1] + probabilidades[2, 2] + probabilidades[1, 3] + probabilidades[0, 4]) * 100
chance_5_gols = (probabilidades[5, 0] + probabilidades[4, 1] + probabilidades[3, 2] + probabilidades[2, 3] + probabilidades[1, 4] + probabilidades[0, 5]) * 100

# Imprime as chances
print("Chances de sair 0 gols: {:.2f}%".format(chance_0_gols))
print("Chances de sair 1 gol: {:.2f}%".format(chance_1_gol))
print("Chances de sair 2 gols: {:.2f}%".format(chance_2_gols))
print("Chances de sair 3 gols: {:.2f}%".format(chance_3_gols))
print("Chances de sair 4 gols: {:.2f}%".format(chance_4_gols))
print("Chances de sair 5 gols: {:.2f}%".format(chance_5_gols))
