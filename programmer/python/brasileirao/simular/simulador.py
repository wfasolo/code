from scipy.stats import poisson
import numpy as np
import requests
import pandas as pd


def Obter_dados(liga, ano):
    url = f"http://api.football-data.org/v4/competitions/{liga}/matches?season={ano}"

    headers = {
        "X-Unfold-Goals": "true",
        "X-Auth-Token": "eacce4ab67424884b3bf4b79882547da"
    }

    # Requisição HTTP
    response = requests.get(url, headers=headers)

    # Verificando se a requisição foi bem-sucedida
    if response.status_code != 200:
        raise Exception(
            f"Erro na requisição: {response.status_code}, {response.text}")

    # Processando o JSON retornado
    matches = response.json().get('matches', [])

    # Verificação se o campo 'matches' existe no JSON
    if not matches:
        raise Exception("Nenhuma partida encontrada ou resposta inválida.")

    # Construindo a tabela a partir dos dados recebidos
    tab = []
    for match in matches:
        matchday = match.get('matchday')
        home_team = match.get('homeTeam', {}).get('shortName', 'N/A')
        away_team = match.get('awayTeam', {}).get('shortName', 'N/A')
        full_time_score = match.get('score', {}).get('fullTime', {})
        score_home = full_time_score.get('home')
        score_away = full_time_score.get('away')

        # Adicionando à tabela, mesmo se os scores forem None
        tab.append([matchday, home_team, away_team, score_home, score_away])

    df = pd.DataFrame(
        tab, columns=['rod', 'equipeA', 'equipeB', 'scor_A', 'scor_B'])

    # Remover linhas com valores nulos em colunas de pontuação
    df2 = df.dropna(subset=['scor_A', 'scor_B']).reset_index(drop=True)

    # Convertendo pontuações para inteiros
    df2['scor_A'] = df2['scor_A'].astype(int)
    df2['scor_B'] = df2['scor_B'].astype(int)

    # Garantindo que a coluna 'rod' seja numérica para comparações
    df2['rod'] = pd.to_numeric(df2['rod'], errors='coerce')
    df['rod'] = pd.to_numeric(df['rod'], errors='coerce')

    # Filtrando rodadas futuras
    max_rod = df2['rod'].max()
    df3 = df[df['rod'] > max_rod].reset_index(drop=True)

    return df2, df3


def Criar_tabela(df_partidas):
    # Condições para determinar os resultados das partidas
    conditions = [
        df_partidas['scor_A'] < df_partidas['scor_B'],  # Time A perdeu
        df_partidas['scor_A'] > df_partidas['scor_B'],  # Time A ganhou
        df_partidas['scor_A'] == df_partidas['scor_B']  # Empate
    ]

    # Pontuações para os times A e B
    choicesA = [0, 3, 1]  # Time A: derrota = 0, vitória = 3, empate = 1
    choicesB = [3, 0, 1]  # Time B: vitória = 3, derrota = 0, empate = 1

    # Atribuindo os resultados baseados nas condições
    df_partidas['resultA'] = np.select(conditions, choicesA, default=1)
    df_partidas['resultB'] = np.select(conditions, choicesB, default=1)

    # Separação dos dados para equipes A e B
    c = df_partidas.drop(['equipeB', 'resultB'], axis=1)
    d = df_partidas.drop(['equipeA', 'resultA'], axis=1)

    # Renomeando as colunas para manter coerência
    c = c.rename(columns={
        'equipeA': 'equipe',
        'scor_A': 'feito',
        'scor_B': 'sofr',
        'resultA': 'result'
    })

    d = d.rename(columns={
        'equipeB': 'equipe',
        'scor_B': 'feito',
        'scor_A': 'sofr',
        'resultB': 'result'
    })

    # Concatenando as duas tabelas (para equipes A e B) em uma só
    df_concat = pd.concat([c, d], ignore_index=True)

    # Ordenando os dados pela coluna 'rod'
    df_concat = df_concat.sort_values(by='rod')

    # Filtrando as rodadas maiores ou iguais a 3
    df_filtrados = df_concat[df_concat['rod'] >= 3]

    # Eliminando valores nulos somente nas colunas essenciais
    df_filtrados = df_filtrados.dropna(
        subset=['equipe', 'feito', 'sofr', 'rod', 'result'])

    return df_filtrados


def Calcular_forças(df_forca):
    # Cálculo dos pontos, gols a favor e gols contra cumulativos por equipe
    df_forca['pontos'] = df_forca.groupby('equipe')['result'].cumsum()
    df_forca['g_pro'] = df_forca.groupby('equipe')['feito'].cumsum()
    df_forca['g_con'] = df_forca.groupby('equipe')['sofr'].cumsum()

    # Cálculo cumulativo das vitórias (quando o resultado é 3)
    df_forca['soma_vit'] = df_forca[df_forca['result'] == 3].groupby(
        'equipe')['result'].cumsum().fillna(0)

    # Tratamento de valores nulos
    df_forca = df_forca.fillna(0)

    # Cálculo das médias ofensiva e defensiva por rodada
    df_forca['off'] = round(df_forca['g_pro'] / df_forca['rod'], 2)
    df_forca['def'] = round(df_forca['g_con'] / df_forca['rod'], 2)
    df_forca['soma_vit'] = round(df_forca['soma_vit'] / df_forca['rod'], 2)

    # Aplicação de médias móveis com janela de 2 rodadas para desempenho ofensivo e defensivo
    df_forca['off'] = df_forca.groupby('equipe')['off'].transform(
        lambda x: x.rolling(window=2).mean())
    df_forca['def'] = df_forca.groupby('equipe')['def'].transform(
        lambda x: x.rolling(window=2).mean())

    # Remoção de linhas que ficaram com valores nulos após o cálculo de médias móveis
    df_forca = df_forca.dropna()

    # Removendo colunas não mais necessárias
    df_forca = df_forca.drop(['feito', 'sofr', 'result'], axis=1)

    # Ordenando por rodada e pontos, com mais pontos em destaque
    df_forca = df_forca.sort_values(['rod', 'pontos'], ascending=[True, False])

    return df_forca


def Simular_partidas(i, df3, df4):
    # Obtenção das equipes para o jogo atual
    eqA = df3['equipeA'][i]
    eqB = df3['equipeB'][i]

    # Extração das métricas das equipes do DataFrame df4
    off_A = df4[df4['equipe'] == eqA]['off'].values[0]
    off_B = df4[df4['equipe'] == eqB]['off'].values[0]
    def_A = df4[df4['equipe'] == eqA]['def'].values[0]
    def_B = df4[df4['equipe'] == eqB]['def'].values[0]
    # s_v_A = df4[df4['equipe'] == eqA]['soma_vit'].values[0]
    # s_v_B = df4[df4['equipe'] == eqB]['soma_vit'].values[0]

    # Cálculo dos gols esperados para cada time
    gol_A = off_A * def_B * 1.05
    gol_B = off_B * def_A * 0.95

   # Definindo o limite de gols como 4 e gerando a distribuição de Poisson
    resul_A = np.random.poisson(off_A, 5)
    resul_A = [x for x in resul_A if x <= 4]

    resul_B = np.random.poisson(off_B, 5)
    resul_B = [x for x in resul_B if x <= 4]

    # Calculando a probabilidade para os gols de A e B
    probab_A = np.around(poisson.pmf(k=resul_A,
                                     mu=gol_A) * 100, decimals=1)
    probab_B = np.around(poisson.pmf(k=resul_B,
                                     mu=gol_B) * 100, decimals=1)

  # Criando DataFrames para probabilidades e agrupando para somar probabilidades repetidas
    prob_A = pd.DataFrame({'gols': resul_A, 'probabilidade': probab_A})
    prob_B = pd.DataFrame({'gols': resul_B, 'probabilidade': probab_B})

    # Pegando o número de gols com a maior probabilidade para cada equipe
    ga = prob_A.loc[prob_A['probabilidade'].idxmax(), 'gols']
    gb = prob_B.loc[prob_B['probabilidade'].idxmax(), 'gols']

    # Atualizando os resultados de placar no DataFrame df3
    df3.loc[i, 'scor_A'] = ga
    df3.loc[i, 'scor_B'] = gb

    return df3


def Calcular_percentual_posicoes():
    # Lendo o arquivo CSV
    df = pd.read_csv('posicao.csv')

    # DataFrame vazio para armazenar os resultados
    tabela = pd.DataFrame()

    # Determinando o valor máximo de 'pos' no dataset
    max_pos = df['pos'].max()

    # Iterando sobre todas as possíveis posições (de 0 ao valor máximo em 'pos')
    for i in range(0, max_pos + 1):
        # Contagem de equipes que ficaram em determinada posição 'i'
        cont_pos = df[df['pos'] == i].groupby('equipe').size()

        # Contagem total de simulações para cada equipe
        total_sim = df.groupby('equipe').size()

        # Cálculo da porcentagem de vezes que a equipe ficou na posição 'i'
        porcentagem = (cont_pos / total_sim) * 100

        # Criando um DataFrame temporário para armazenar os dados
        tab = pd.DataFrame({'equipe': porcentagem.index,
                           'porcentagem': porcentagem.values})
        tab['pos'] = i

        # Concatenando os resultados ao DataFrame final
        tabela = pd.concat([tabela, tab], ignore_index=True)

    # Preenchendo valores nulos com 0
    tabela = tabela.fillna(0)

    # Ajustando o formato para exibir as porcentagens por equipe e posição
    tabela_pivot = tabela.pivot(
        index='equipe', columns='pos', values='porcentagem')

    # Preenchendo novamente os valores ausentes com 0 (se alguma equipe não ocupou certa posição)
    tabela_pivot = tabela_pivot.fillna(0)

    # Arredondando os valores para inteiros
    tabela_pivot = tabela_pivot.round(0).astype(int)

    # Resetando o índice para adequar ao formato final
    tabela_pivot = tabela_pivot.reset_index()

    # Ordenando as equipes pela primeira posição, depois segunda, etc.
    tabela_pivot = tabela_pivot.sort_values(
        by=list(range(1, max_pos + 1)), ascending=False)

    # Reiniciando o índice, começando em 1
    tabela_pivot.index = tabela_pivot.index + 1

    return tabela_pivot


def main():
    # Obtendo os dados iniciais
    dados_iniciais = Obter_dados('BSA', 2024)
    tabela_principal = dados_iniciais[0]  # Tabela principal de dados
    dados_futuros = dados_iniciais[1]  # Dados das rodadas futuras

    # Variáveis de controle
    rodada_atual = 1
    tabela_posicoes = pd.DataFrame()

    # Simulações
    for simulacao in range(1, 150):
        # Evitar modificar diretamente o DataFrame original
        dados_simulados = tabela_principal.copy()
        while True:
            # Atualiza os dados
            dados_calculados = Calcular_forças(
                Criar_tabela(dados_simulados)).reset_index(drop=True)

            rodada_atual = dados_calculados['rod'].max()  # Última rodada
            dados_proxima_rodada = dados_futuros[dados_futuros['rod'] ==
                                                 rodada_atual + 1].reset_index(drop=True)  # Próxima rodada
            dados_rodada_atual = dados_calculados[dados_calculados['rod'] == rodada_atual].reset_index(
                drop=True)  # Rodada atual

            # Finaliza se atingir a rodada 38
            if rodada_atual == 38:
                break

            # Simulação para cada partida da rodada
            for partida in range(10):
                dados_proxima_rodada = Simular_partidas(
                    partida, dados_proxima_rodada, dados_rodada_atual)

            # Atualiza o DataFrame dados_simulados com as novas partidas
            dados_simulados = pd.concat(
                [dados_simulados, dados_proxima_rodada], ignore_index=True)

        # Ajuste das posições finais ao final da simulação
        posicoes_finais = pd.DataFrame(
            dados_calculados['equipe'].tail(20).reset_index())
        posicoes_finais = posicoes_finais.dropna()
        posicoes_finais['pos'] = (
            posicoes_finais['index'] - posicoes_finais['index'].min()) + 1
        tabela_posicoes = pd.concat(
            [tabela_posicoes, posicoes_finais], ignore_index=True)

        # Exibir resultados a cada 5 simulações e gravar os dados no CSV
        if simulacao % 5 == 0:
            tabela_posicoes.to_csv('posicao.csv', index=False)
            print(Calcular_percentual_posicoes())
            print()

    # Garantir que os resultados finais sejam gravados e exibidos
    if simulacao % 5 != 0:
        tabela_posicoes.to_csv('posicao.csv', index=False)
        print(Calcular_percentual_posicoes())


main()
