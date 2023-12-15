import os
import boto3
import concurrent.futures

# Configuração do cliente S3
s3 = boto3.client('s3',
                  aws_access_key_id='SEU_ACCESS_KEY_ID',
                  aws_secret_access_key='SEU_SECRET_ACCESS_KEY')

# Função para fazer upload de um diretório para o S3
def upload_directory(local_path, bucket_name, s3_path):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_file_path = os.path.join(s3_path, os.path.relpath(local_file_path, local_path))
            print(f'Uploading {local_file_path} to {s3_file_path}')
            s3.upload_file(local_file_path, bucket_name, s3_file_path)

if __name__ == "__main__":
    # Diretório local a ser carregado
    local_directory = "C:/Windows/teste"
    
    # Bucket S3 e caminho no bucket
    bucket_name = "pessoa"
    s3_path = "plano/cadadro/"

    # Listar diretórios no local_directory
    directories = [os.path.join(local_directory, name) for name in os.listdir(local_directory) if os.path.isdir(os.path.join(local_directory, name))]

    # Use ThreadPoolExecutor para executar o upload em múltiplos threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(upload_directory, directories, [bucket_name]*len(directories), [s3_path]*len(directories))
