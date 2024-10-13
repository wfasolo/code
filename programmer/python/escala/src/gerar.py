import pandas as pd
import os
import platform
from src.manipulacao_dados import carregar_mes_anterior, salvar_escala
from src.geracao_escala import gerar_escala
from src.ordenar_dia import ordenar

# Função para limpar a tela do terminal, independentemente do sistema operacional
def limpar_tela():
    sistema = platform.system()
    if sistema == "Windows":
        os.system('cls')  # Comando para Windows
    else:
        os.system('clear')  # Comando para Linux e macOS

# Função que processa os dados para um local específico
def processar_local(mes, ano, local, funcionarios_df):
    ultimos_4_dias = carregar_mes_anterior(mes, ano, local)
    escala = gerar_escala(mes, ano, local, funcionarios_df, ultimos_4_dias)
    
    if escala:
        salvar_escala(mes, ano, local, escala)

# Função principal que organiza o fluxo geral
def main(ano, mes, local, lista):
    limpar_tela()  # Chama a função para limpar a tela
    mes = int(mes)
    ano = int(ano)
    lista.remove("_TODOS")
    
    # Carrega e ordena o DataFrame de funcionários
    func_df = pd.read_csv('dados/funcionarios.csv', sep=';')
    funcionarios_df = ordenar(func_df, mes, ano)

    # Caso o local não seja '_TODOS', processa apenas um local
    if local != '_TODOS':
        lista = [local]

    # Processa os dados para cada local na lista
    for local in lista:
        processar_local(mes, ano, local, funcionarios_df)
