import json

# Carregar o arquivo JSON
with open('seuarquivo.json', 'r') as arquivo:
    dados = json.load(arquivo)

# Filtrar os itens que têm 'nome-cliente-relacionamento' como 'AQUISICAO'
dados_filtrados = [item for item in dados['detalheplanorecord'] if item.get('nome-cliente-relacionamento') == 'AQUISICAO']

# Sobrescrever o arquivo JSON apenas com os dados filtrados, se houver itens correspondentes
if dados_filtrados:
    dados['detalheplanorecord'] = dados_filtrados
    with open('seuarquivo.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=2)
        print("Dados removidos com sucesso.")
else:
    print("Nenhum item correspondente encontrado.")
