import os
import boto3
import concurrent.futures

def download_file(bucket_name, key, local_directory, s3_resource):
    # Verificar se o arquivo está no Glacier Deep Archive
    obj = s3_resource.Object(bucket_name, key)
    storage_class = obj.storage_class
    if storage_class == 'DEEP_ARCHIVE':
        print(f"O arquivo {key} está armazenado no Glacier Deep Archive. Não será baixado.")
        return

    local_filename = os.path.join(local_directory, key)
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)

    try:
        s3_resource.meta.client.download_file(bucket_name, key, local_filename)
        print(f"Arquivo {key} baixado com sucesso para {local_filename}")
    except Exception as e:
        print(f"Erro ao baixar o arquivo {key}: {str(e)}")

def download_files_from_s3(bucket_name, folder_path, local_directory, num_threads=10):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    # Listar objetos no caminho especificado no S3
    objects_to_download = [obj.key for obj in bucket.objects.filter(Prefix=folder_path)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for key in objects_to_download:
            futures.append(executor.submit(download_file, bucket_name, key, local_directory, s3))

        for future in concurrent.futures.as_completed(futures):
            future.result()

# Exemplo de uso:
bucket_name = 'seu-bucket'
folder_path = 'caminho/para/os/arquivos'
local_directory = '/caminho/local/para/salvar/os/arquivos'

download_files_from_s3(bucket_name, folder_path, local_directory)
