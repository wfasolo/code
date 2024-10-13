import tkinter as tk
from tkinter import messagebox
import pandas as pd
import src.gerar as gerar
import src.merge as merge

# Funções de lógica de negócio
def chamar_gerar(entrada_ano, entrada_mes, entrada_local, opcoes_local):
    """
    Chama o script 'gerar.py' para gerar escalas, usando os valores de ano, mês e local,
    exibindo uma mensagem de sucesso ou erro.
    """
    ano = entrada_ano.get()
    mes = entrada_mes.get()
    local = entrada_local.get()
    try:
        gerar.main(ano, mes, local, opcoes_local)
        messagebox.showinfo("Sucesso", f"Escalas geradas com sucesso para o ano {ano} e mês {mes}.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar: {e}")

def chamar_pdf(entrada_ano, entrada_mes):
    """
    Chama o script 'merge.py' para gerar um PDF com base nos valores de ano e mês,
    exibindo uma mensagem de sucesso ou erro.
    """
    ano = entrada_ano.get()
    mes = entrada_mes.get()
    try:
        merge.main(ano, mes)
        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso para o ano {ano} e mês {mes}.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

def carregar_locais_do_csv(arquivo_csv):
    """
    Carrega o arquivo CSV, extrai os locais únicos e os retorna como uma lista.
    """
    try:
        df = pd.read_csv(arquivo_csv, delimiter=';', encoding='utf-8')
        locais = sorted(df['local'].drop_duplicates())
        if '_TODOS' not in locais:
            locais.insert(0, '_TODOS')
        return locais
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo {arquivo_csv} não encontrado.")
        return []
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar o CSV: {e}")
        return []

# Funções de UI
def criar_entradas(janela):
    """
    Cria as caixas de entrada para ano, mês e local na janela principal.
    """
    # Entrada de Ano
    label_ano = tk.Label(janela, text="Ano", font=("Arial", 10, "bold"))
    label_ano.grid(row=1, column=0, padx=10, pady=5, sticky="w", ipadx=10)
    entrada_ano = tk.Entry(janela)
    entrada_ano.grid(row=1, column=1, padx=10, pady=5, ipadx=10)

    # Entrada de Mês
    label_mes = tk.Label(janela, text="Mês", font=("Arial", 10, "bold"))
    label_mes.grid(row=2, column=0, padx=10, pady=5, sticky="w", ipadx=10)
    entrada_mes = tk.Entry(janela)
    entrada_mes.grid(row=2, column=1, padx=10, pady=5, ipadx=10)

    return entrada_ano, entrada_mes

def criar_selecao_local(janela, arquivo_csv):
    """
    Cria o menu de seleção para o local, carregando os valores únicos do CSV.
    """
    # Rótulo para o Local
    label_local = tk.Label(janela, text="Local:", font=("Arial", 10, "bold"))
    label_local.grid(row=3, column=0, padx=10, pady=5, sticky="w", ipadx=10)

    # Variável associada ao OptionMenu
    entrada_local = tk.StringVar(janela)
    entrada_local.set("_TODOS")

    # Carregar locais únicos do CSV
    opcoes_local = carregar_locais_do_csv(arquivo_csv)

    # Criando o OptionMenu
    local_menu = tk.OptionMenu(janela, entrada_local, *opcoes_local)
    local_menu.grid(row=3, column=1, padx=5, pady=5, ipadx=26)

    return entrada_local, opcoes_local

def criar_botoes(janela, entrada_ano, entrada_mes, entrada_local, opcoes_local):
    """
    Cria os botões para gerar PDF e escalas, associando suas funções.
    """
    # Botão Gerar PDF
    botao_gerar = tk.Button(janela, text="Gerar PDF", 
                            command=lambda: chamar_pdf(entrada_ano, entrada_mes))
    botao_gerar.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    # Botão Gerar Escalas
    botao_imprimir = tk.Button(janela, text="Gerar Escalas", 
                               command=lambda: chamar_gerar(entrada_ano, entrada_mes, entrada_local, opcoes_local))
    botao_imprimir.grid(row=4, column=1, padx=10, pady=10, sticky="e")

# Função principal para inicialização da interface gráfica
def inicializar_interface():
    """
    Configura e inicializa a interface gráfica do aplicativo.
    """
    janela = tk.Tk()
    janela.title("Gerador de Escala")
    janela.geometry("400x250")

    # Título da janela
    titulo = tk.Label(janela, text="Gerador de Escala", font=("Helvetica", 16))
    titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")

    # Criação de entradas e seleção de local
    entrada_ano, entrada_mes = criar_entradas(janela)
    entrada_local, opcoes_local = criar_selecao_local(janela, 'dados/funcionarios.csv')

    # Criação de botões
    criar_botoes(janela, entrada_ano, entrada_mes, entrada_local, opcoes_local)

    # Iniciar o loop da interface gráfica
    janela.mainloop()

# Executar o programa
if __name__ == "__main__":
    inicializar_interface()
