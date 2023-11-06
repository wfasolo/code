from datetime import datetime
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
#import plotly.offline as py
import plotly.graph_objs as go


url_weather = 'https://api.weather.com/v1/geocode/-21.129/-41.677/forecast/hourly/48hour.json?units=m&language=pt-BR&apiKey=320c9252a6e642f38c9252a6e682f3c6'


# Dados site weather.com
resp = requests.get(url_weather)
weather_json = resp.json()
weather_pd = pd.DataFrame(weather_json['forecasts'])
weather_df = pd.DataFrame([weather_pd.fcst_valid-10800], index=['dt']).T
weather_df.reset_index(inplace=True, drop=True)
hora = pd.DataFrame()
for i in range(22):

    hora[i] = [datetime.utcfromtimestamp(
        weather_df['dt'][i]).strftime("%d/%m/%Y %H:%M")]

hora = hora.T
print(hora)
df = pd.DataFrame([range(10, 30), np.random.randint(50,size=20)],
                  index=['yr_built', 'price']).T
print(df)

trace = go.Scatter(x=df['yr_built'],
                   y=df['price'],
                   text=df['price'],
                   textposition='top center',
                   mode='lines+markers+text')

data = [trace]
py.plot(data)
