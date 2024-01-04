import json

# Função para processar o JSON lido do arquivo
def processar_json(data):
    for item in data.get("dados", []):
        detalhe_plano = item.get("detalheplanorecord", [])
        for i, detalhe in enumerate(detalhe_plano):
            if detalhe.get("nome-cliente-relacionamento") == "AQUISICAO":
                # Mantém somente o primeiro item se for "AQUISICAO"
                item["detalheplanorecord"] = [detalhe]
                break  # Para no primeiro item encontrado
    return data

# Nome do arquivo JSON
nome_arquivo = "dados.json"

# Leitura do arquivo JSON
with open(nome_arquivo, "r") as arquivo:
    dados_json = json.load(arquivo)

# Processamento do JSON
json_processado = processar_json(dados_json)

# Saída do JSON processado
print(json.dumps(json_processado, indent=4))
