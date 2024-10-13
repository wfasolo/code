import tkinter as tk
from tkinter import messagebox
import csv
import src.gerar as gerar
import src.merge as merge

# Função para chamar o script gerar.py e exibir o retorno
def chamar_gerar():
    ano = entrada_ano.get()
    mes = entrada_mes.get()
    local = entrada_local.get()
    try:
        # Chama o script principal e captura o retorno
        gerar.main(ano, mes, local, opcoes_local)
        messagebox.showinfo("Sucesso", f"Escalas gerado com sucesso para o ano {ano} e mês {mes}.")

        
    except Exception as e:
        # Exibe um popup em caso de erro
        messagebox.showerror("Erro", f"Erro ao gerar: {e}")

# Função para chamar o script imprimir.py e gerar o PDF
def chamar_pdf():
    ano = entrada_ano.get()
    mes = entrada_mes.get()
    try:
        # Passa os parâmetros (ano, mês) para o script imprimir.py
        merge.main(ano, mes)
        messagebox.showinfo("Sucesso", f"PDF gerado com sucesso para o ano {ano} e mês {mes}.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

# Função para ler o arquivo CSV e pegar os locais únicos
def carregar_locais_do_csv(arquivo_csv):
    locais = set()  # Utiliza um conjunto para evitar duplicações
    try:
        with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
            leitor_csv = csv.DictReader(csvfile, delimiter=';')  # Lê o arquivo como dicionário
            for linha in leitor_csv:
                locais.add(linha['local'])  # Adiciona o local ao conjunto
        
        locais_ordenados = sorted(locais)  # Ordena os locais
        if '_TODOS' not in locais_ordenados:
            locais_ordenados.insert(0, '_TODOS')  # Garante que '_TODOS' seja o primeiro na lista
        return locais_ordenados  # Retorna a lista de locais ordenada
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo {arquivo_csv} não encontrado.")
        return []

# Configuração da janela principal
janela = tk.Tk()
janela.title("Gerador de Escala")
janela.geometry("400x250")

# Título da janela centralizado
titulo = tk.Label(janela, text="Gerador de Escala", font=("Helvetica", 16))
titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")

# Configuração dos rótulos e caixas de entrada
label_ano = tk.Label(janela, text="Ano", font=("Arial", 10, "bold"))
label_ano.grid(row=1, column=0, padx=10, pady=5, sticky="w", ipadx=10)
entrada_ano = tk.Entry(janela)
entrada_ano.grid(row=1, column=1, padx=10, pady=5, ipadx=10)

label_mes = tk.Label(janela, text="Mês", font=("Arial", 10, "bold"))
label_mes.grid(row=2, column=0, padx=10, pady=5, sticky="w", ipadx=10)
entrada_mes = tk.Entry(janela)
entrada_mes.grid(row=2, column=1, padx=10, pady=5, ipadx=10)

# Configuração do rótulo e menu de seleção para o local
label_local = tk.Label(janela, text="Local:", font=("Arial", 10, "bold"))
label_local.grid(row=3, column=0, padx=10, pady=5, sticky="w", ipadx=10)

# Variável associada ao OptionMenu
entrada_local = tk.StringVar(janela)
entrada_local.set("_TODOS")  # Definir valor padrão como "_TODOS"

# Carrega os locais únicos do arquivo CSV
arquivo_csv = 'dados/funcionarios.csv'
opcoes_local = carregar_locais_do_csv(arquivo_csv)

# Criando o OptionMenu para a seleção do local
local_menu = tk.OptionMenu(janela, entrada_local, *opcoes_local)
local_menu.grid(row=3, column=1, padx=5, pady=5, ipadx=26)

# Botões para Gerar e Imprimir
botao_gerar = tk.Button(janela, text="Gerar PDF", command=chamar_pdf)
botao_gerar.grid(row=4, column=0, padx=10, pady=10, sticky="w")

botao_imprimir = tk.Button(janela, text="Gerar Escalas", command=chamar_gerar)
botao_imprimir.grid(row=4, column=1, padx=10, pady=10, sticky="e")

# Inicia o loop da interface gráfica
janela.mainloop()
