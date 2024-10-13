from datetime import datetime

# Função para obter o dia da semana em português
def dia_da_semana_em_portugues(dia):
    dias_da_semana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    return dias_da_semana[dia]

# Função para obter o ano e o mês atuais
def obter_data_atual():
    ano_atual = datetime.now().year
    mes_atual = datetime.now().month
    return ano_atual, mes_atual

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
