import os
import concurrent.futures
import boto3

# Configurações do AWS S3
BUCKET_NAME = 'seu-bucket'
AWS_ACCESS_KEY_ID = 'seu-access-key'
AWS_SECRET_ACCESS_KEY = 'seu-secret-key'
REGION_NAME = 'sua-regiao-do-bucket'

# Função para realizar o upload de uma pasta para o AWS S3
def upload_folder(folder_path, s3_client, bucket_name):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = os.path.relpath(local_path, folder_path)
            s3_client.upload_file(local_path, bucket_name, s3_path)
            print(f'Uploaded {local_path} to S3 bucket')

if __name__ == "__main__":
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=REGION_NAME)

    folder_path = 'C:/windows/teste'  # Caminho da pasta local a ser carregada para o S3

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for root, dirs, files in os.walk(folder_path):
            for dir_name in dirs:
                full_path = os.path.join(root, dir_name)
                futures.append(executor.submit(upload_folder, full_path, s3, BUCKET_NAME))

        # Espera todas as threads terminarem
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Exception: {e}')
