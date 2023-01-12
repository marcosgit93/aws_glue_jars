import boto3
import threading
from queue import Queue

s3 = boto3.client('s3')
nome_do_bucket = 'meu-bucket'

def baixar_arquivo(obj):
    s3.download_file(nome_do_bucket, obj['Key'], obj['Key'])

# create a queue for the objects
queue = Queue()

# specify the prefix of the folder
folder_prefix = 'pasta/'

# get the objects of the folder 
objects = s3.list_objects_v2(Bucket=nome_do_bucket, Prefix=folder_prefix)['Contents']

# add the objects to the queue
for obj in objects:
    queue.put(obj)

# function to download files from the queue
def worker():
    while not queue.empty():
        obj = queue.get()
        baixar_arquivo(obj)
        queue.task_done()

# define number of worker threads
num_worker_threads = 8

# start the worker threads
for _ in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()

# wait for the queue to be empty
queue.join()

print("Todos os arquivos baixados!")