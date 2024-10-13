import pandas as pd
import tkinter as tk
from tkinter import ttk

# Função para carregar o arquivo CSV e verificar as colunas


def carregar_dataframe(filepath):
    try:
        dataframe = pd.read_csv(filepath)
    except FileNotFoundError:
        print("Erro: O arquivo CSV não foi encontrado.")
        exit(1)

    # Verifica se as colunas necessárias estão presentes
    required_columns = ["Dia", "Dia da Semana", "Funcionário", "Férias"]
    for col in required_columns:
        if col not in dataframe.columns:
            print(f"Erro: A coluna '{col}' não está presente no DataFrame.")
            exit(1)

    return dataframe


# Função para configurar a interface gráfica principal (janela)


def configurar_janela():
    root = tk.Tk()
    root.title("Escala de Funcionários")
    root.geometry("900x800")
    return root


# Função para configurar os frames da interface


def configurar_frames(root):
    frame_tabela = tk.Frame(root)
    frame_tabela.grid(row=0, column=0, sticky="nsew")

    frame_direito = tk.Frame(root, bg="lightgrey")
    frame_direito.grid(row=0, column=1, sticky="nsew")

    root.grid_columnconfigure(0, weight=3)
    root.grid_columnconfigure(1, weight=2)

    return frame_tabela, frame_direito


# Função para criar e configurar a tabela Treeview


def configurar_treeview(frame_tabela):
    tree = ttk.Treeview(
        frame_tabela,
        columns=("Dia", "Dia da Semana", "Funcionário", "Férias"),
        show="headings",
        height=31,
    )

    tree.heading("Dia", text="Dia")
    tree.heading("Dia da Semana", text="Dia da Semana")
    tree.heading("Funcionário", text="Funcionário")
    tree.heading("Férias", text="Férias")

    tree.column("Dia", width=50, anchor="center")
    tree.column("Dia da Semana", width=100, anchor="center")
    tree.column("Funcionário", width=150, anchor="center")
    tree.column("Férias", width=70, anchor="center")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    return tree


# Função para configurar as tags de estilo da Treeview


def configurar_tags(tree):
    tree.tag_configure("evenrow", background="lightgrey")
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("weekend", foreground="red")
    tree.tag_configure("ferias", foreground="green")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))


# Função para aplicar as cores condicionais às linhas da tabela


def aplicar_cor_condicional(linha):
    tags = []
    if linha["Dia da Semana"].lower() in ["sábado", "domingo"]:
        tags.append("weekend")
    if linha["Férias"] != 0:
        tags.append("ferias")
    return tags if tags else None


# Função para atualizar a tabela com os dados do DataFrame


def atualizar_tabela(tree, dataframe):
    for row in tree.get_children():
        tree.delete(row)

    for index, linha in dataframe.iterrows():
        cor_tags = aplicar_cor_condicional(linha)
        row_tag = "evenrow" if index % 2 == 0 else "oddrow"
        tags = (row_tag,) + tuple(cor_tags) if cor_tags else (row_tag,)

        tree.insert(
            "",
            "end",
            values=(
                linha["Dia"],
                linha["Dia da Semana"],
                linha["Funcionário"],
                linha["Férias"],
            ),
            tags=tags,
        )


# Função para atualizar o funcionário no DataFrame e na tabela


def atualizar_funcionario(dataframe, tree, entry_nome, label_dia_atualizado):
    for index, linha in dataframe.iterrows():
        if linha["Férias"] == 1:
            novo_nome = entry_nome.get()
            if novo_nome:
                dataframe.at[index, "Funcionário"] = novo_nome
                dataframe.at[index, "Férias"] = 2
                label_dia_atualizado.config(
                    text=f"Dia atualizado: {linha['Dia']} - {linha['Dia da Semana']}"
                )

            atualizar_tabela(tree, dataframe)
            mostrar_primeiro_dia(dataframe, label_dia_atualizado)
            break


# Função para mostrar o primeiro dia a ser alterado


def mostrar_primeiro_dia(dataframe, label_dia_atualizado):
    for index, linha in dataframe.iterrows():
        if linha["Férias"] == 1:
            label_dia_atualizado.config(
                text=f"Dia a ser alterado: {linha['Dia']} - {linha['Dia da Semana']}"
            )
            break


# Função principal para inicializar e executar a interface gráfica


def iniciar_interface(filepath):
    dataframe = carregar_dataframe(filepath)
    root = configurar_janela()
    frame_tabela, frame_direito = configurar_frames(root)

    titulo = tk.Label(
        frame_tabela, text="Escala do Mês de Outubro", font=("Arial", 12, "bold")
    )
    titulo.pack(pady=10)

    label_dia_atualizado = tk.Label(
        frame_direito, text="Nenhum dia selecionado", bg="lightgrey"
    )
    label_dia_atualizado.pack(pady=5)

    tree = configurar_treeview(frame_tabela)
    configurar_tags(tree)

    atualizar_tabela(tree, dataframe)
    mostrar_primeiro_dia(dataframe, label_dia_atualizado)

    label_nome = tk.Label(frame_direito, text="Novo Nome do Funcionário:")
    label_nome.pack(pady=5)

    entry_nome = tk.Entry(frame_direito)
    entry_nome.pack(pady=5)

    botao_atualizar = tk.Button(
        frame_direito,
        text="Atualizar Funcionário",
        command=lambda: atualizar_funcionario(
            dataframe, tree, entry_nome, label_dia_atualizado
        ),
    )
    botao_atualizar.pack(pady=10)

    root.mainloop()


# Executa a interface passando o caminho do arquivo CSV
iniciar_interface("escala_Bom Jesus_10_2024.csv")
