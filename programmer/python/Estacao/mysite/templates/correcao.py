import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler


def corrigir(ler):
    dados = ler['dados']
    intervalo = ler['intervalo']
    hora = ler['hora']

    score_Temp2 = 0
    score_Pres2 = 0
    score_Umid2 = 0
    
    

    # generate a model of polynomial features
    for i in range(2, 20):
        poly = PolynomialFeatures(degree=i, include_bias=False)

        # transform the x data for proper fitting (for single variable type it returns,[1,x,x**2])
        X_ = poly.fit_transform(intervalo)
        y_Temp = dados['Temp']
        y_Pres = dados['Pres']
        y_Umid = dados['Umid']

        # criando e treinando o modelo
        model_Temp = LinearRegression()
        model_Pres = LinearRegression()
        model_Umid = LinearRegression()

        model_Temp.fit(X_, y_Temp)
        model_Pres.fit(X_, y_Pres)
        model_Umid.fit(X_, y_Umid)

        pred_Temp = model_Temp.predict(X_)
        pred_Pres = model_Pres.predict(X_)
        pred_Umid = model_Umid.predict(X_)
       
        score_Temp = model_Temp.score(X_, y_Temp)
        score_Pres = model_Pres.score(X_, y_Pres)
        score_Umid = model_Umid.score(X_, y_Umid)

        if score_Temp > score_Temp2:
            score_Temp2 = score_Temp
            pred_Temp2 = pd.DataFrame(pred_Temp).round(1)
            i_Temp = i

        if score_Pres > score_Pres2:
            score_Pres2 = score_Pres
            pred_Pres2 = pd.DataFrame(pred_Pres).round(1)
            i_Pres = i

        if score_Umid > score_Umid2:
            score_Umid2 = score_Umid
            umid=pd.DataFrame(pred_Umid)
            minn=umid.min().values
            maxx=umid.max().values
            if maxx >99:
                maxx=99
            scaler = MinMaxScaler(feature_range=(minn,maxx))
            umid=scaler.fit_transform(umid)
            pred_Umid2 = pd.DataFrame(umid).round(1)
            i_Umid = i

    print(i_Temp, score_Temp2.__round__(4))
    print(i_Pres, score_Pres2.__round__(4))
    print(i_Umid, score_Umid2.__round__(4))
   
    corrigido = pd.DataFrame([hora[1].values, pred_Pres2[0][-24:], pred_Temp2[0]
                              [-24:], pred_Umid2[0][-24:]], index=['hora', 'Pres', 'Temp', 'Umid']).T

    return {'corrigido': corrigido}
