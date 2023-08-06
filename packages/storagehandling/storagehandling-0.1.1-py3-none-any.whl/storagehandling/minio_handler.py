from minio import Minio

class MinioHandler:

    def __init__(self,endpoint,access_key,secret_key):
        self.client=Minio(endpoint,access_key,secret_key,secure=False)
        
    def create_bucket(self,bucket_name):
        return self.client.make_bucket(bucket_name=bucket_name)

    def list_buckets(self):
        list_buckets=[]
        buckets= self.client.list_buckets()
        for bucket in buckets:
            list_buckets.append(bucket.name)
        return list_buckets

    def upload_object(self,bucket_name,obj,filename):
        return self.client.fput_object(bucket_name=bucket_name,object_name=obj,file_path=filename)
    
    def list_objects(self,bucket_name):
        list_obj=[]
        objects = self.client.list_objects(bucket_name=bucket_name,recursive=True)
        for obj in objects:
            list_obj.append(obj.object_name)
        return list_obj  

    def delete_object(self,bucket_name,obj):
        return self.client.remove_object(bucket_name=bucket_name,object_name=obj)   

    def download_object(self,bucket_name,obj,filename):
        return self.client.fget_object(bucket_name=bucket_name,object_name=obj,file_path=filename)


   