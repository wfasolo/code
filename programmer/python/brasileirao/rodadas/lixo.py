import requests
import pandas as pd
from datetime import datetime
# Dados site weather.com
url_weather = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/hourly"

querystring = {"lat": "-21.1291757", "lon": "-41.6769274", "hours": "48"}

headers = {
    'x-rapidapi-key': "5e0f2f65d6msh15f253d0b277bb6p1aaa80jsnc1bde5aef933",
    'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com"
}
resp = requests.request(
    "GET", url_weather, headers=headers, params=querystring)
weather_json = resp.json()
weather_pd = pd.DataFrame(weather_json['data'])
weather_df = pd.DataFrame([(weather_pd.ts-10800), weather_pd.slp*0.98067, (weather_pd.temp+1),
                           weather_pd.rh], index=['dt', 'Pres', 'Temp', 'Umid']).T
weather_df.reset_index(inplace=True, drop=True)
weather_df.dropna()
print(weather_df)
hora = pd.DataFrame()
for i in range(24):
    hora[i] = [datetime.utcfromtimestamp(weather_df['dt'][i]).strftime(
        "%d/%m/%Y"), datetime.utcfromtimestamp(weather_df['dt'][i]).strftime("%H h")]
hora = hora.T
print(hora)
