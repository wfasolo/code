import pandas as pd


def res():
    df = pd.read_csv("dados/posicao.csv")
    tabela = pd.DataFrame()
    for i in range(0, 21):
        cont_pos = df[df["pos"] == i].groupby("equipe").size()

        total_sim = df.groupby("equipe").size()

        porcentagem = (cont_pos / total_sim) * 100

        tab = pd.DataFrame([porcentagem.dropna()])
        tab["pos"] = i

        tab = tab.reset_index()

        tabela = pd.concat([tabela, tab], ignore_index=True)
    tabela = tabela.fillna(0)
    tabela = tabela.T.round(0).astype(int)

    tabela = tabela.reset_index()
    tabela = tabela.drop([0, 1])
    tabela = tabela.drop(0, axis=1)

    tabela = tabela.sort_values(
        by=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
            12, 13, 14, 15, 16, 17, 18, 19, 20],
        ascending=False,
    )
    tabela = tabela.reset_index(drop=True)
    tabela.index = tabela.index + 1
    return tabela


new_df = res()
# Somando colunas anteriores (C2 a C16)
new_df.iloc[:, 1:16] = new_df.iloc[:, 1:16].cumsum(axis=1)
# Somando colunas subsequentes (C17 a C20)
new_df.iloc[:, 19] = new_df.iloc[:, 19:].sum(axis=1)  # C20
new_df.iloc[:, 18] = new_df.iloc[:, 18:].sum(axis=1)  # C19
new_df.iloc[:, 17] = new_df.iloc[:, 17:].sum(axis=1)  # C18
new_df.iloc[:, 16] = new_df.iloc[:, 16:].sum(axis=1)  # C17

numerical_cols = new_df.select_dtypes(
    include=['number']).columns  # Seleciona colunas numéricas
new_df[numerical_cols] = new_df[numerical_cols].where(
    (new_df[numerical_cols] >= 1) & (new_df[numerical_cols] <= 96), '-')

print(new_df)
