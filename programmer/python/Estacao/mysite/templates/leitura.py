import pandas as pd
import numpy as np
import requests
from datetime import datetime


def ler():

    url_station = 'https://api.thinger.io/v1/users/wfasolo/buckets/dados_estacao1/data?items=0&authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJidWNrZXQiLCJ1c3IiOiJ3ZmFzb2xvIn0.CrjRqDEFx4KDVCnkOTJtVjnZlkHehO0M_TGE3KEPZ10'

    # Dados site weather.com
    url_weather = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/hourly"

    querystring = {"lat": "-21.5", "lon": "-41.5", "hours": "48"}

    headers = {
        'x-rapidapi-key': "5e0f2f65d6msh15f253d0b277bb6p1aaa80jsnc1bde5aef933",
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com"
    }
    resp = requests.request(
        "GET", url_weather, headers=headers, params=querystring)
    weather_json = resp.json()
    weather_pd = pd.DataFrame(weather_json['data'])
    weather_df = pd.DataFrame([(weather_pd.ts-10800), weather_pd.slp, weather_pd.temp,
                               weather_pd.rh], index=['dt', 'Pres', 'Temp', 'Umid']).T
    weather_df.reset_index(inplace=True, drop=True)
    weather_df.dropna()

    # Dados estação
    resp = requests.get(url_station)
    station_json = resp.json()
    station_pd = pd.DataFrame(station_json)
    station = station_pd['val'].values
    station_df = pd.json_normalize(station)
    station_df['data_hora'] = pd.to_datetime(
        (station_pd['ts']-(3*3600000))*1e6).dt.round('min')
    station_df = pd.DataFrame(station_df)
    station_df = station_df.dropna()

    # Dados Inea
    df = pd.read_excel(
        "http://alertadecheias.inea.rj.gov.br/alertadecheias/2141095.xlsx")
    df = pd.DataFrame(df)
    df['data_hora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'])
    df['timestamp_epoch'] = (
        df['data_hora'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    # Unir Chuva
    df_unido = pd.merge(station_df, df, on='data_hora')
    df_unido = df_unido[['Pres', 'Temp', 'Umid', 'Chuva Último dado']]
    df_unido = df_unido.rename(columns={'Chuva Último dado': 'Chuv'})
    station_df = df_unido[df_unido['Chuv'] != 'Dado Nulo']
    station_df['Chuv'] = station_df['Chuv'].astype(float)
    station_df.loc[station_df['Chuv'] > 0, 'Chuv'] = 1
    station_df['Chuv'] = station_df['Chuv'].astype(int)

    # hora
    hora = pd.DataFrame()
    for i in range(24):
        hora[i] = [datetime.utcfromtimestamp(weather_df['dt'][i]).strftime(
            "%d/%m/%Y"), datetime.utcfromtimestamp(weather_df['dt'][i]).strftime("%H h")]
    hora = hora.T

    # Concatenar
    station = station_df.drop(['Chuv'], axis=1)
    station = station.round(2)
    inv_station = station[::-1]
    weather_df = weather_df.drop(['dt'], axis=1)
    dados = pd.concat([inv_station[-20:], weather_df[:24]], ignore_index=True)
    intervalo = pd.concat([pd.DataFrame(np.arange(1, 11, 0.5)), pd.DataFrame(
        np.arange(11, 35, 1))], ignore_index=True)

    return {'dados': dados, 'intervalo': intervalo, 'hora': hora, 'estacao': station_df}
