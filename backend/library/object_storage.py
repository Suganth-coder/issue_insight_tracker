import os

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from library import Library

MINIO_ENDPOINT_URL = os.getenv("MINIO_ENDPOINT_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")


class S3Storage:
    def __init__(self):
        self.s3_client = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT_URL,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4")
        )
 
        try:
            self.s3_client.head_bucket(Bucket=MINIO_BUCKET_NAME)
        except ClientError:
            print("Bucket does not exist, creating a new bucket...")
            self.s3_client.create_bucket(Bucket=MINIO_BUCKET_NAME)

    def upload_attachment(self, data):
        """
        upload_attachment is used to upload an attachment to the S3 bucket.

        reporter/admin --> upload an attachment
        """

        if data['role'] == "maintainer":
            return 403
        
        attachment = data.get("attachment")
        file_content = data.get("file_content")
        user_id = data.get("user_id")

        filename = Library.get_unique_hashed_data(attachment.filename) + "_" + attachment.filename

        self.s3_client.put_object(
            Bucket=MINIO_BUCKET_NAME,
            Key=filename,
            Body=file_content,
            ContentType=attachment.content_type,
            Metadata = {
                "created_by": user_id
            }
        )
        
        return {"status": 200, "filename": filename}
    
    def get_attachment(self, data):

        filename = data.get("filename")
        try:
            self.s3_client.head_object(Bucket=MINIO_BUCKET_NAME, Key=filename)
        except ClientError as e:
            return 404

        file_data = self.s3_client.get_object(Bucket=MINIO_BUCKET_NAME,Key=filename)
        return file_data

    def delete_attachment(self, data):
        """
        delete_attachment is used to delete an attachment from the S3 bucket.

        Only admin can delete an attachment.
        """
        if data['role'] != "admin":
            return 403
        
        try:
            self.s3_client.delete_object(Bucket=MINIO_BUCKET_NAME, Key=data['filename'])
            return 200
        
        except ClientError as e:
            return 404