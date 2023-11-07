import requests
import pandas as pd
import numpy as np
import equipes as eq
import time

url = "http://api.football-data.org/v4/competitions/" 
headers = {
    "X-Unfold-Goals": "true",
    "X-Auth-Token": "eacce4ab67424884b3bf4b79882547da"
}

response = requests.get(url, headers=headers)
matches = response.json()
a=[]
for i in range(12):
    a.append([matches['competitions'][i]['id'].values])
print(a)
