import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go

def graf(corrigido,SVCprev):
    pres_min=corrigido['Pres'].min()

    '''
    plt.plot(corrigido['hora'], corrigido['Temp'])
    plt.xticks(rotation=90)
    plt.show()
    plt.plot(corrigido['hora'], corrigido['Pres'])
    plt.xticks(rotation=90)
    plt.show()
    plt.plot(corrigido['hora'], corrigido['Umid'])
    plt.xticks(rotation=90)
    plt.show()'''

    trace = go.Scatter(x=corrigido['hora'],
                    y=corrigido['Temp'],
                    text=corrigido['Temp'],
                    textposition='top center',
                    mode='lines+markers+text',
                    showlegend=False)

    trace2 = go.Bar(x=corrigido['hora'],
                    y=corrigido['Temp'],
                    marker_color='LightBlue',
                    opacity=0.5,
                    showlegend=False
                    )
    trace3= go.Scatter(x=corrigido['hora'],
                    y=corrigido['Umid']*0.13,
                    text=corrigido['Umid'],
                    textposition='top center',
                    mode='lines+markers+text',
                    showlegend=False)

    trace4= go.Scatter(x=corrigido['hora'],
                    y=corrigido['Pres']-pres_min,
                    text=corrigido['Pres'],
                    textposition='top center',
                    mode='lines+markers+text',
                    showlegend=False)

    trace5 = go.Scatter(x=corrigido['hora'],
                    y=SVCprev['previsao'][1],
                    text=(SVCprev['previsao'][1]*100).round(0),
                    textposition='top center',
                    mode='lines+markers+text',
                    showlegend=True,
                    name='chuva')


    data_temp = [trace, trace2,trace3,trace4,trace5]
    py.plot(data_temp)




# station_df.to_csv('estacao.csv')
# station_df.to_json('estacao.json',orient='records') # ou 'table'
# corrigido.to_json('corrigido.json',orient='records')
