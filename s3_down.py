import boto3
import os

# Lista de URLs dos arquivos no S3
urls = [
    "s3://pessoa-dev/plano/conversor/year=2023/month=10/day=12/arquivo1.parquet",
    "s3://pessoa-dev/plano/conversor/year=2023/month=10/day=12/arquivo2.parquet",
    # Adicione outras URLs aqui, se necessário
]

# Função para fazer o download do arquivo do S3
def download_from_s3(url):
    # Parse da URL para obter informações do bucket e do objeto
    parsed_url = url.split("/")
    bucket_name = parsed_url[2]
    object_key = "/".join(parsed_url[3:])

    # Criar uma pasta local com base na estrutura da URL
    local_folder = f"month={object_key.split('month=')[1].split('/')[0]}/day={object_key.split('day=')[1].split('/')[0]}"
    os.makedirs(local_folder, exist_ok=True)

    # Configuração do cliente do S3
    s3 = boto3.client('s3')

    # Fazer o download do arquivo do S3 para a pasta local
    local_file_path = os.path.join(local_folder, os.path.basename(object_key))
    s3.download_file(bucket_name, object_key, local_file_path)

# Iterar sobre as URLs e fazer o download dos arquivos
for url in urls:
    download_from_s3(url)
