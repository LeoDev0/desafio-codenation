import requests
import json
import string
import hashlib

token = ""
get_url_prefix = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token="
post_url_prefix = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token="
get_url = get_url_prefix + token
post_url = post_url_prefix + token

# Fazendo a requisição HTTP via GET dos dados da API e armazenando-os em forma de JSON   
get_response = requests.get(get_url)
json_data = get_response.json()

# Escrevendo e formatando os dados num arquivo JSON
with open('answer.json', 'w') as file:
    json.dump(json_data, file, indent=1)

# Abrindo o arquivo JSON para pegar a cifra e o número de casas do algoritmo de cesar
with open('answer.json') as json_file:
    data = json.load(json_file)

cifrado = data['cifrado']
numero_casas = data['numero_casas']

# Função para reverter a criptografia de césar
def caesar(plaintext, shift):
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[-shift:] + alphabet[:-shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)

decifrado = caesar(cifrado, numero_casas)
resumo_criptografico = hashlib.sha1(decifrado.encode('utf-8')).hexdigest() # gerando hash da mensagem já descriptografada

data['decifrado'] = decifrado
data['resumo_criptografico'] = resumo_criptografico

# Reescrevendo o arquivo JSON com as respostas preenchidas
with open ('answer.json', 'w') as file:
    json.dump(data, file, indent=1)

# Enviando o arquivo com uma requisição HTTPS do tipo POST
file = {'answer': open('answer.json', 'rb')}
post_response = requests.post(post_url, files=file)
print(post_response.status_code)
print(post_response.text)