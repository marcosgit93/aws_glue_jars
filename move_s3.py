import boto3

def mover_arquivos_s3(bucket_name, origem_prefix, destino_prefix):
    # Configuração do cliente S3
    s3 = boto3.client('s3')

    # Listar objetos na pasta de origem
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=origem_prefix)

    # Mover cada objeto para a pasta de destino
    for obj in response.get('Contents', []):
        origem_key = obj['Key']
        destino_key = origem_key.replace(origem_prefix, destino_prefix, 1)  # Substituir o prefixo de origem pelo de destino

        # Copiar o objeto para o novo local
        s3.copy_object(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': origem_key},
            Key=destino_key
        )

        # Excluir o objeto da pasta de origem após a cópia
        s3.delete_object(Bucket=bucket_name, Key=origem_key)

# Definir o nome do bucket e os prefixos de origem e destino
bucket_name = 'seu-bucket-s3'
origem = 'caminho/da/pasta/origem/'
destino = 'novo/caminho/da/pasta/destino/'

# Chamar a função para mover os arquivos
mover_arquivos_s3(bucket_name, origem, destino)
