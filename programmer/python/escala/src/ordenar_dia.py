from datetime import datetime, timedelta

# Função para verificar se a data de verificação está dentro do período de trabalho
def verifica_trabalho(data_inicio_str, data_verificacao_str):
    formato_data = "%d/%m/%Y"
    
    # Converte as datas de string para datetime
    data_inicio = datetime.strptime(data_inicio_str, formato_data)
    data_verificacao = datetime.strptime(data_verificacao_str, formato_data)

    # Ciclo de trabalho e folga (24h de trabalho + 72h de folga)
    ciclo_total = timedelta(hours=96)  # 4 dias no total
    horas_trabalho = timedelta(hours=24)  # 1 dia de trabalho

    # Calcula a diferença entre as datas e a posição no ciclo
    diferenca = data_verificacao - data_inicio
    posicao_no_ciclo = diferenca % ciclo_total

    # Verifica se a posição está dentro do período de trabalho (primeiras 24h)
    return posicao_no_ciclo < horas_trabalho

# Leitura dos dados de funcionários


# Itera sobre as linhas do dataframe
def ordenar(df,mes,ano):
    for idx, row in df.iterrows():
        data_inicio = row['data_base']  # Data de referência do funcionário
        
        # Verifica os dias 1 a 4 de outubro de 2024
        for dia in range(1, 5):
            data_verificacao = f'{dia}/{mes}/{ano}'  # Formata a data para cada dia de verificação

            # Se estiver no período de trabalho, atualiza a coluna 'ordem'
            if verifica_trabalho(data_inicio, data_verificacao):
                df.at[idx, 'ordem'] = dia
                break  # Interrompe o loop assim que encontrar o primeiro dia de trabalho
    return df


