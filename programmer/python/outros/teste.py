import requests
from bs4 import BeautifulSoup

# faça a requisição HTTP para a página web
url = 'https://news.google.com/home?hl=pt-BR&gl=BR&ceid=BR:pt-419'
response = requests.get(url)

# analise o conteúdo HTML da página usando BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# encontre todos os elementos HTML que contêm as manchetes das notícias
headlines = soup.find_all('div', class_='TRHLAc')

print(headlines)
