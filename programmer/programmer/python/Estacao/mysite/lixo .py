import requests
import pandas as pd

url = "https://encurtador.com.br/gmxGR"
# Faz a requisição para obter o conteúdo do arquivo
response = requests.post(url)

# Verifica se a requisição foi bem-sucedida (código 200)
if response.status_code == 200:
    # Salva o conteúdo do arquivo em um arquivo local
    with open("dados_cheias.xlsx", "wb") as file:
        file.write(response.content)
else:
    print("Erro ao fazer a requisição. Código de status:", response.status_code)
    exit()

# Lê o arquivo .xlsx com o Pandas
dados = pd.read_excel("dados_cheias.xlsx")

# Agora você pode trabalhar com os dados usando o Pandas
print(dados.head())  # Para exibir as primeiras linhas dos dados

payload = {
    'grant_type': 'authorization_code', 
    'code': request.args['code'],
    'state': request.args['state'],
    'redirect_uri': 'http://xxx.xyz.com/request_listener',
}

url = 'https://serviceprovider.xxx.com/auth/j_oauth_resolve_access_code'

response = requests.post(url, data=payload, verify=False)