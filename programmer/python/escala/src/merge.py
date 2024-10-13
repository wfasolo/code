import os
import pandas as pd
import src.criar_pdf as criar_pdf
from src.ferias import processar_ferias

# Função para processar todos os arquivos do diretório
def processar_diretorio(diretorio, ano, mes):
    """
    Processa todos os arquivos no diretório, agrupando-os por substring,
    e substitui funcionários em caso de férias.
    """
    arquivos_por_substring = agrupar_arquivos_por_substring(diretorio)

    for substring, arquivos in arquivos_por_substring.items():
        processar_arquivos_csv(arquivos, diretorio, ano, mes)

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
            arquivos_por_substring.setdefault(substring, []).append(nome_arquivo)
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
            print(f"A coluna 'Funcionario' não foi encontrada no arquivo {arquivo}")

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
    criar_pdf.main(df_base, ano, mes, arq[:-4])

# Execução principal do script
def main(ano, mes):
    # Parâmetros globais
    diretorio = f'escalas/{ano}/{mes}'
    processar_diretorio(diretorio, ano, mes)

# Se precisar executar diretamente:
#if __name__ == "__main__":
#    main(2023, 10)
