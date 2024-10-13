import pandas as pd
from datetime import datetime, timedelta
import os
import datetime as dt

# Função para obter o dia da semana em português
def dia_da_semana_em_portugues(dia):
    dias_da_semana = ['domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado']
    return dias_da_semana[dia]

# Função para obter o ano e o mês atuais
def obter_data_atual():
    ano_atual = dt.datetime.now().year
    mes_atual = dt.datetime.now().month
    return ano_atual, mes_atual

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
        return [ultimos_4_dias, verificar_funcionarios_férias(escala_anterior_df)]
    else:
        print(f'Arquivo do mês anterior {caminho_arquivo_mes_anterior} não encontrado. Iniciando a partir da ordem padrão.')
        return None

# Nova função para verificar férias
def verificar_funcionarios_férias(escala_anterior_df):
    ferias_apos_dia_9 = escala_anterior_df.iloc[9:]
    contagem_ferias = ferias_apos_dia_9['Ferias'].astype(int).sum()
    if contagem_ferias == 4:
        print('Tem menos de 5 dias de férias após o dia 9.')
        funcionarios_com_ferias = ferias_apos_dia_9[ferias_apos_dia_9['Ferias'] == 1]['Funcionario']
        return funcionarios_com_ferias[-1:].values[0]

# Função para filtrar funcionários pelo local
def filtrar_funcionarios_por_local(funcionarios_df, local):
    funcionarios_local = funcionarios_df[funcionarios_df['local'] == local]
    if funcionarios_local.empty:
        print(f'Não há funcionários disponíveis para o local {local}.')
    return funcionarios_local

# Função para ajustar a ordem de funcionários
def ajustar_ordem_funcionarios(funcionarios_local, ultimos_4_dias):
    funcionarios_ordenados = list(funcionarios_local['nome'])
    for funcionario in ultimos_4_dias:
        if funcionario in funcionarios_ordenados:
            funcionarios_ordenados.remove(funcionario)
            funcionarios_ordenados.append(funcionario)
    return funcionarios_local.set_index('nome').loc[funcionarios_ordenados].reset_index()

# Função para gerar a escala mensal
def gerar_escala(mes, ano, local, funcionarios_df, ultimos_4_dias=None):
    funcionarios_local = filtrar_funcionarios_por_local(funcionarios_df, local)
    if funcionarios_local.empty:
        return None

    funcionarios_local = funcionarios_local.sort_values(by='ordem')
    nome_ferias = ''

    if ultimos_4_dias:
        funcionarios_local = ajustar_ordem_funcionarios(funcionarios_local, ultimos_4_dias[0])
        nome_ferias = ultimos_4_dias[1]

    dias_do_mes = pd.date_range(f'{ano}-{mes}-01', periods=1, freq='M').day[0]
    data_inicio = datetime(ano, mes, 1)
    escala_local = []
    ordem_inicial = 0

    for dia in range(1, dias_do_mes + 1):
        data_atual = data_inicio + timedelta(days=dia - 1)
        dia_semana = dia_da_semana_em_portugues(data_atual.weekday())
        funcionario_escalado = funcionarios_local.iloc[ordem_inicial % len(funcionarios_local)]

        inicio = funcionario_escalado['inicio']
        dia_inicio = dt.date(ano, mes, inicio).weekday()
        if dia_inicio == 0:
            inicio += 1

        if funcionario_escalado['ferias'] == mes and inicio <= dia:
            ferias = '1'
        else:
            ferias = '0'

        escala_local.append({
            'Dia': dia,
            'Dia da Semana': dia_semana,
            'Funcionario': funcionario_escalado['nome'],
            'Ferias': ferias
        })

        ordem_inicial += 1

    if nome_ferias:
        for i, funcionario in enumerate(escala_local):
            if funcionario['Funcionario'] == nome_ferias:
                escala_local[i]['Ferias'] = '1'
                break

    return escala_local

# Função para salvar a escala em um arquivo CSV (organizado por ano/mês)
def salvar_escala(mes, ano, local, escala):
    # Criar o caminho dos diretórios por ano/mês
    pasta_destino = f'escalas/{ano}/{mes}'
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Definir o caminho completo para o arquivo
    arquivo_saida = f'{pasta_destino}/escala_{local}_{mes}_{ano}.csv'
    
    # Salvar o arquivo CSV com separador ";"
    escala_df = pd.DataFrame(escala)
    escala_df.to_csv(arquivo_saida, sep=';', index=False)
    
    print(f'Escala do mês {mes}/{ano} para o local {local} salva com sucesso em "{arquivo_saida}".')
    print(escala_df)

# Função principal do programa
def main():
    funcionarios_df = pd.read_csv('dados/funcionarios.csv', sep=';')  # Carregar CSV dos funcionários com separador ';'
    ano, mes = obter_data_atual()
    ano = int(input('Digite o ano para gerar a escala (ex: 2024): ') or ano)
    mes = int(input('Digite o número do mês para gerar a escala (1-12): ') or mes)
    local = input('Digite o local para o qual deseja gerar a escala: ')

    ultimos_4_dias = carregar_mes_anterior(mes, ano, local)

    escala = gerar_escala(mes, ano, local, funcionarios_df, ultimos_4_dias)

    if escala:
        salvar_escala(mes, ano, local, escala)

# Executa o programa
if __name__ == '__main__':
    main()
