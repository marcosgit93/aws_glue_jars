import os
import concurrent.futures
import boto3

# Função para fazer o upload de um arquivo para o S3
def upload_file(bucket_name, file_path, s3_key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, s3_key)

# Função para fazer upload de uma pasta para o S3 de forma multitarefa
def upload_folder_to_s3(bucket_name, folder_path, s3_prefix):
    s3 = boto3.client('s3')
    files_to_upload = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = s3_prefix + file_path[len(folder_path) + 1:]
            files_to_upload.append((file_path, s3_key))

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for file_path, s3_key in files_to_upload:
            futures.append(executor.submit(upload_file, bucket_name, file_path, s3_key))
        
        # Espera até que todas as threads tenham concluído
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Erro ao fazer upload: {e}")

# Defina suas credenciais AWS antes de usar
# boto3.setup_default_session(profile_name='your_profile_name')

# Chame a função para fazer upload da pasta para o S3
bucket_name = 'nome_do_seu_bucket'
folder_path = '/caminho/da/sua/pasta'
s3_prefix = 'prefixo_para_o_seu_s3/'  # O prefixo que você deseja no S3

upload_folder_to_s3(bucket_name, folder_path, s3_prefix)
