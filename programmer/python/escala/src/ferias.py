# Função para processar apenas os quatro primeiros funcionários de férias
def processar_ferias(df):
    """
    Seleciona os quatro primeiros funcionários e processa suas substituições em caso de férias.
    """
    quatro_primeiros_funcionarios = df["Funcionario"].head(4).tolist()
    df = processar_dataframe(df, quatro_primeiros_funcionarios)
    return df

# Função para processar o DataFrame e substituir funcionários de férias
def processar_dataframe(df, lista_funcionarios):
    """
    Substitui funcionários que estão de férias com base na lista de substitutos.
    """
    indice_substituicao = 0
    for i, row in df.iterrows():
        novo_funcionario, indice_substituicao = substituir_funcionario(
            row, lista_funcionarios, indice_substituicao)
        df.at[i, "Funcionario"] = novo_funcionario
    return df

# Função para substituir o funcionário em caso de férias
def substituir_funcionario(row, lista_funcionarios, indice_substituicao):
    """
    Substitui o funcionário se ele estiver de férias (Ferias = 1).
    Percorre a lista de funcionários disponíveis e atribui um substituto.
    """
    if row["Ferias"] == 1:
        while lista_funcionarios[indice_substituicao] == row["Funcionario"]:
            # Evita atribuir o mesmo funcionário e avança na lista
            indice_substituicao = (indice_substituicao + 1) % len(lista_funcionarios)
        substituto = 'Férias: ' + lista_funcionarios[indice_substituicao]
        indice_substituicao = (indice_substituicao + 1) % len(lista_funcionarios)
        return substituto, indice_substituicao
    else:
        return row["Funcionario"], indice_substituicao
