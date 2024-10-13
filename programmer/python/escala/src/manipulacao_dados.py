import os
import pandas as pd

# Função para carregar o arquivo do mês anterior e determinar a ordem inicial
def carregar_mes_anterior(mes, ano, local):
    mes_anterior = mes - 1 if mes > 1 else 12
    ano_anterior = ano if mes > 1 else ano - 1

    caminho_arquivo_mes_anterior = f'escalas/{ano_anterior}/{mes_anterior}/escala_{local}_{mes_anterior}_{ano_anterior}.csv'

    if os.path.exists(caminho_arquivo_mes_anterior):
        print(f'Carregando arquivo do mês anterior: {caminho_arquivo_mes_anterior}')
        escala_anterior_df = pd.read_csv(caminho_arquivo_mes_anterior, sep=';')
        
        # Chamada para verificar férias
        ultimos_4_dias = escala_anterior_df.tail(4)['Funcionario'].tolist()
        return [ultimos_4_dias, verificar_funcionarios_ferias(escala_anterior_df)]
    else:
        print(f'Arquivo do mês anterior {caminho_arquivo_mes_anterior} não encontrado. Iniciando a partir da ordem padrão.')
        return None

# Função para verificar férias
def verificar_funcionarios_ferias(escala_anterior_df):
    ferias_apos_dia_9 = escala_anterior_df.iloc[9:]
    contagem_ferias = ferias_apos_dia_9['Ferias'].astype(int).sum()
    if contagem_ferias == 4:
        print('Tem menos de 5 dias de férias após o dia 9.')
        funcionarios_com_ferias = ferias_apos_dia_9[ferias_apos_dia_9['Ferias'] == 1]['Funcionario']
        return funcionarios_com_ferias[-1:].values[0]

# Função para salvar a escala em um arquivo CSV
def salvar_escala(mes, ano, local, escala):
    pasta_destino = f'escalas/{ano}/{mes}'
    os.makedirs(pasta_destino, exist_ok=True)

    arquivo_saida = f'{pasta_destino}/escala_{local}_{mes}_{ano}.csv'
    escala_df = pd.DataFrame(escala)
    escala_df.to_csv(arquivo_saida, sep=';', index=False)
    
    print(f'Escala do mês {mes}/{ano} para o local {local} salva com sucesso em "{arquivo_saida}".')
    
