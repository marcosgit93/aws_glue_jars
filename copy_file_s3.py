import boto3

def copy_files_within_s3_bucket(source_folder, destination_folder, bucket_name, aws_access_key_id, aws_secret_access_key, region_name='us-east-1'):
    # Inicializa o cliente S3
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    # Lista os objetos na pasta de origem
    objects = s3.list_objects(Bucket=bucket_name, Prefix=source_folder)

    # Garante que a pasta de destino termine com '/'
    if not destination_folder.endswith('/'):
        destination_folder += '/'

    # Itera sobre cada objeto na pasta de origem
    for obj in objects.get('Contents', []):
        # Obtém a chave do objeto (caminho no bucket)
        source_key = obj['Key']

        # Calcula a chave de destino com base na pasta de destino
        destination_key = destination_folder + source_key[len(source_folder):]

        # Copia o objeto para a pasta de destino no mesmo bucket
        s3.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': source_key}, Key=destination_key)

        print(f"Arquivo {source_key} copiado para {destination_key}")

# Exemplo de uso
aws_access_key_id = 'SEU_ACCESS_KEY_ID'
aws_secret_access_key = 'SEU_SECRET_ACCESS_KEY'
region_name = 'sua-regiao'  # ex: 'us-east-1'
bucket_name = 'seu-bucket'
source_folder = 'caminho/para/pasta/origem'
destination_folder = 'caminho/para/pasta/destino'

copy_files_within_s3_bucket(source_folder, destination_folder, bucket_name, aws_access_key_id, aws_secret_access_key, region_name)
