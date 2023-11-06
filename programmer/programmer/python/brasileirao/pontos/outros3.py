import pandas as pd
import obter
import outros1
import outros2
import rodada
import resultado

obt = obter.obt('BSA', 2023)
tab = obt[0]
df2 = obt[1]

rod = 1
posicao = pd.DataFrame()


for ii in range(1,15):
    print(ii)
    df5 = tab
    while True:

        df = outros2.out2(outros1.out1(df5)).reset_index()

        rod = df['rod'].max()
        df3 = df2[df2['rod'] == rod+1].reset_index(drop=True)
        df4 = df[df['rod'] == rod].reset_index(drop=True)
        if rod == 38:
            break

        for i in range(10):
            df3 = rodada.rodar(i, df3, df4)

        df5 = pd.concat([df5, df3], ignore_index=True)

    final = pd.DataFrame(df['equipe'].tail(20).reset_index())
    final = final.dropna()
    final['pos'] = (final['index']-final['index'].min())+1
    posicao = pd.concat([posicao, final], ignore_index=True)

    if ii % 10 == 0:
        print(resultado.res())

posicao.to_csv('dados/posicao.csv', index=False)
if ii % 10 != 0:
    print(resultado.res())

# exec(open('resultado.py').read())
