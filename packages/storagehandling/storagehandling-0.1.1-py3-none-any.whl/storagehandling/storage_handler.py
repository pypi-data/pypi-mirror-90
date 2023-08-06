from storagehandling.minio_handler import MinioHandler
from storagehandling.s3_handler import S3Handler

def open(file_storage,endpoint,access_key,secret_key):
    if file_storage=='Minio':
        storageHandler=MinioHandler(endpoint,access_key,secret_key)
        return storageHandler
        
    elif file_storage=='S3':
        storageHandler=S3Handler(endpoint,access_key,secret_key)
        return storageHandler