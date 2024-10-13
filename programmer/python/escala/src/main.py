from src.manipulacao_dados import carregar_mes_anterior, salvar_escala
from src.geracao_escala import gerar_escala

from src.ordenar_dia import ordenar
import pandas as pd
import os



os.system('cls')


def main(ano,mes,local,lista):
    ''' ano, mes = obter_data_atual()
    ano = int(input('Digite o ano ou <enter> pra atual: ') or ano)
    mes = int(input('Digite o número do mês ou <enter> pra atual: ') or mes)
    local = input('Digite o local para o qual deseja gerar a escala: ')
    '''
    mes=int(mes)
    ano=int(ano)
    lista.remove("_TODOS")


    func_df = pd.read_csv('dados/funcionarios.csv', sep=';')
    
    funcionarios_df = ordenar(func_df, mes, ano)

    if local!='_TODOS':
        lista=[local]
        
    
        
    for local in lista:

        ultimos_4_dias = carregar_mes_anterior(mes, ano, local)

        escala = gerar_escala(mes, ano, local, funcionarios_df, ultimos_4_dias)

        if escala:
            salvar_escala(mes, ano, local, escala)



#if __name__ == '__main__':
#    main()
