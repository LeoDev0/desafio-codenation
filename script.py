import requests
import json
import string
import hashlib

# Fazendo a requisição HTTP via GET dos dados da API e armazenando-os em forma de JSON   
response = requests.get("https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=03f386cb7c6fe496efcb34186179f09b0dd0e081")
json_data = response.json()
# json_data = json.loads(response.content.decode('utf-8'))

# Escrevendo e formatando os dados num arquivo JSON
with open('answer.json', 'w') as outfile:
    json.dump(json_data, outfile, indent=1)

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

# Reescrevendo o arquivo JSON com as respostas preenchida
with open ('answer.json', 'w') as outfile:
    json.dump(data, outfile, indent=1)


# Enviando o arquivo com uma requisição HTTPS do tipo POST
url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=03f386cb7c6fe496efcb34186179f09b0dd0e081'

files = {'file': open('answer.json', 'rb')}

r = requests.post(url, files=files)
print(r.status_code)
print(r.text)