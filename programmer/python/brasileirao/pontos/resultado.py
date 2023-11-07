import pandas as pd

def res():
    df = pd.read_csv('dados/posicao.csv')
    tabela=pd.DataFrame()
    for i in range(0,21):
        cont_pos = df[df['pos'] == i].groupby('equipe').size()

        total_sim = df.groupby('equipe').size()

        porcentagem = (cont_pos / total_sim) * 100

        tab=pd.DataFrame([porcentagem.dropna()])
        tab['pos']=i
            
        tab=tab.reset_index()
        
        tabela=pd.concat([tabela, tab], ignore_index=True)
    tabela=tabela.fillna(0)
    tabela=tabela.T.round(0).astype(int)

    tabela=tabela.reset_index()
    tabela=tabela.drop([0,1])
    tabela=tabela.drop(0,axis=1)
    tabel=tabela.reset_index(drop=True,inplace=True)
    tabela.index=tabela.index+1
    tabela=tabela.sort_values(by=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],ascending=False)

    return tabela
