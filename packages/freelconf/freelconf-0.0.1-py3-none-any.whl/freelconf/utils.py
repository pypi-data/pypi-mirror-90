import os
import boto3

class FileManager():


    @classmethod
    def read(cls, path, boto_client=None):
        if cls.s3_path(path):
            s3 = boto_client if boto_client else boto3.client('s3')
            return cls.read_s3_file(s3, path).read()
        elif cls.gs_path(path):
            raise NotImplementedError("FileManer.read.gs_path")
        if not cls.local_path(path):
            raise FileNotFoundError(f"{path} not found. Aborting")
        return cls.read_local_file(path)
        

    @classmethod
    def s3_path(cls, path):
        """Check if file is stored on S3"""
        return path.startswith("s3://")

    @classmethod
    def gs_path(cls, path):
        """Check if file is stored on GS"""
        return path.startswith("gs://")

    @classmethod
    def local_path(cls, path):
        """Check if file exists on local host"""
        return os.path.exists(path) and os.path.isfile(path)

    @classmethod
    def read_local_file(cls, path):
        return open(path)

    @classmethod
    def read_s3_file(cls, client, path):
        bucket = path.split("/")[2]
        key = "/".join(path.split("/")[3:])
        try:
            obj = client.get_object(Bucket=bucket, Key=key)
            return obj['Body']
        except Exception:
            raise FileNotFoundError(f"{path} not found.")