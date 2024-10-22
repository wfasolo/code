import requests
import pandas as pd
from datetime import datetime, timezone

# Definindo as coordenadas de Bom Jesus do Itabapoana
lat = [-21.1255, -20.848084, -21.4123651, -20.733638, -21.7558619]
lon = [-41.6712, -41.11129, -42.1965147, -42.0299412, -41.3326895]

# Sua chave da API do OpenWeatherMap
api_key = "3c935dbe0c33fe08fc9c9215a17e3f9b"

# Lista para armazenar os dados
dados_climaticos = []

for i in range(len(lat)):
    # URL da API de Current Weather Data do OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat[i]}&lon={lon[i]}&appid={api_key}&units=metric"

    # Fazendo a requisição GET
    response = requests.get(url)

    # Verificando se a resposta foi bem-sucedida
    if response.status_code == 200:
        data = response.json()

        # Extraindo os dados relevantes
        local = data['name']
        temperatura = data['main']['temp']
        pressao = data['main']['pressure']
        umidade = data['main']['humidity']
        volume = data['rain']['1h'] if 'rain' in data else 0
        chovendo = 1 if 'rain' in data else 0
        timestamp = data[
            'dt']  # O timestamp é dado no formato UNIX (epoch time)

        # Convertendo timestamp para formato de data legível
        data_hora = datetime.fromtimestamp(
            timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')

        # Armazenando os dados em um dicionário
        dados_climaticos.append({
            'Local': local,
            'Temperatura (°C)': temperatura,
            'Pressão (hPa)': pressao,
            'Umidade (%)': umidade,
            'Preciptação (mm)': volume,
            'Chovendo': chovendo,
            'Data/Hora': data_hora
        })

    else:
        print(f"Erro na requisição: {response.status_code}")

# Criando o DataFrame com os dados
df = pd.DataFrame(dados_climaticos)

# Exibindo o DataFrame
print(df)
