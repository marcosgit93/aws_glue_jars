import os
import boto3
import concurrent.futures

def download_file(bucket_name, key, local_directory):
    s3 = boto3.client('s3')
    file_name = os.path.join(local_directory, os.path.basename(key))
    s3.download_file(bucket_name, key, file_name)
    print(f'Arquivo baixado: {key}')

def download_files_from_s3(bucket_name, folder_path, local_directory, num_threads=10):
    s3 = boto3.client('s3')
    
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)['Contents']
    keys = [obj['Key'] for obj in objects]
    
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_key = {executor.submit(download_file, bucket_name, key, local_directory): key for key in keys}
        for future in concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            try:
                future.result()
            except Exception as e:
                print(f'Erro ao baixar arquivo {key}: {e}')

# Para baixar os arquivos:
bucket_name = 'seu_bucket'
folder_path = 'caminho/para/seu/diretorio/no/S3'
local_directory = '/caminho/local/para/salvar/os/arquivos'

download_files_from_s3(bucket_name, folder_path, local_directory)
