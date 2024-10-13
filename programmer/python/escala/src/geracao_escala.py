import pandas as pd
from datetime import datetime, timedelta
from src.utilidades import dia_da_semana_em_portugues, ajustar_ordem_funcionarios, filtrar_funcionarios_por_local

def gerar_escala(mes, ano, local, funcionarios_df, ultimos_4_dias=None):
    funcionarios_local = filtrar_funcionarios_por_local(funcionarios_df, local)
    if funcionarios_local.empty:
        return None

    funcionarios_local = funcionarios_local.sort_values(by='ordem')
    nome_ferias = ''

    if ultimos_4_dias:
        funcionarios_local = ajustar_ordem_funcionarios(funcionarios_local, ultimos_4_dias[0])
        nome_ferias = ultimos_4_dias[1]

    dias_do_mes = pd.date_range(f'{ano}-{mes}-01', periods=1, freq='ME').day[0]
    data_inicio = datetime(ano, mes, 1)
    escala_local = []
    ordem_inicial = 0
    
    # Dicionário para contar os dias de férias de cada funcionário
    contador_ferias = {nome: 0 for nome in funcionarios_local['nome'].tolist()}

    for dia in range(1, dias_do_mes + 1):
        data_atual = data_inicio + timedelta(days=dia - 1)
        dia_semana = dia_da_semana_em_portugues(data_atual.weekday())
        funcionario_escalado = funcionarios_local.iloc[ordem_inicial % len(funcionarios_local)]

        inicio = funcionario_escalado['inicio']
        dia_inicio = datetime(ano, mes, inicio).weekday()
        if dia_inicio == 0:
            inicio += 1

        # Verificar se o funcionário já atingiu o limite de 5 dias de férias
        if funcionario_escalado['ferias'] == mes and inicio <= dia and contador_ferias[funcionario_escalado['nome']] < 5:
            ferias = '1'
            contador_ferias[funcionario_escalado['nome']] += 1  # Incrementa o contador de férias
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
