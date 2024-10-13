import os
import pandas as pd
import src.imprimir as imprimir



# Função para substituir o funcionário em caso de férias


def substituir_funcionario(row, lista_funcionarios, indice_substituicao):
    """
    Substitui o funcionário se ele estiver de férias (Ferias = 1).
    Percorre a lista de funcionários disponíveis e atribui um substituto.
    """
    if row["Ferias"] == 1:
        while lista_funcionarios[indice_substituicao] == row["Funcionario"]:
            # Evita atribuir o mesmo funcionário e avança na lista
            indice_substituicao = (
                indice_substituicao + 1) % len(lista_funcionarios)
        substituto = 'Férias: '+lista_funcionarios[indice_substituicao]
        indice_substituicao = (indice_substituicao +
                               1) % len(lista_funcionarios)
        return substituto, indice_substituicao
    else:
        return row["Funcionario"], indice_substituicao

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

# Função para processar apenas os quatro primeiros funcionários de férias


def processar_ferias(df):
    """
    Seleciona os quatro primeiros funcionários e processa suas substituições em caso de férias.
    """
    quatro_primeiros_funcionarios = df["Funcionario"].head(4).tolist()
    df = processar_dataframe(df, quatro_primeiros_funcionarios)
    return df

# Função para agrupar arquivos com base em substring de seus nomes


def agrupar_arquivos_por_substring(diretorio):
    """
    Agrupa os arquivos no diretório com base na substring dos nomes de arquivo (posições 7 a 10).
    Retorna um dicionário com a substring como chave e uma lista de arquivos como valor.
    """
    arquivos_por_substring = {}
    for nome_arquivo in os.listdir(diretorio):
        if len(nome_arquivo) >= 10:
            substring = nome_arquivo[6:10]
            arquivos_por_substring.setdefault(
                substring, []).append(nome_arquivo)
    return arquivos_por_substring

# Função principal para processar arquivos CSV e substituir funcionários de férias


def processar_arquivos_csv(arquivos_csv, diretorio, ano, mes):
    """
    Processa uma lista de arquivos CSV, substitui funcionários de férias, 
    e combina os dados em um DataFrame principal.
    """
    # Ler o primeiro arquivo (base)
    df_base = pd.read_csv(f"{diretorio}/{arquivos_csv[0]}", sep=';')
    df_base = processar_ferias(df_base)

    # Loop através dos arquivos restantes e adiciona dados ao DataFrame base
    for i, arquivo in enumerate(arquivos_csv[1:], start=2):
        df_temp = pd.read_csv(f"{diretorio}/{arquivo}", sep=';')
        df_temp = processar_ferias(df_temp)

        # Verifica se a coluna 'Funcionario' existe no arquivo atual
        if 'Funcionario' in df_temp.columns:
            df_base[f'Funcionario_{i}'] = df_temp['Funcionario']
        else:
            print(
                f"A coluna 'Funcionario' não foi encontrada no arquivo {arquivo}")

    # Salva ou processa o DataFrame final


    colunas_renomear = {}
    if 'Funcionario' in df_base.columns:
        colunas_renomear['Funcionario'] = 'Tratamento'
    if 'Funcionario_2' in df_base.columns:
        colunas_renomear['Funcionario_2'] = 'Captação'
    if 'Funcionario_3' in df_base.columns:
        colunas_renomear['Funcionario_3'] = 'Elevatória'
    df_base = df_base.rename(columns=colunas_renomear)
    
    arq = arquivos_csv[0]
    imprimir.main(df_base, ano, mes, arq[:-4])

# Função para processar todos os arquivos do diretório


def processar_diretorio(diretorio, ano, mes):
    """
    Processa todos os arquivos no diretório, agrupando-os por substring,
    e substitui funcionários em caso de férias.
    """
    arquivos_por_substring = agrupar_arquivos_por_substring(diretorio)

    for substring, arquivos in arquivos_por_substring.items():
        processar_arquivos_csv(arquivos, diretorio, ano, mes)


# Execução principal do script
def main(ano,mes):
        # Parâmetros globais

    diretorio = f'escalas/{ano}/{mes}'
    processar_diretorio(diretorio, ano, mes)

# Executar o programa
#if __name__ == "__main__":
#    main()
