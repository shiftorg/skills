import boto3
import os
from sys import stdout

# Connect to S3
bucket_name = "tech-salary-project"
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)

MODEL_VERSION = 2
LOCAL_MODEL_DIR = 'models/'
S3_MODEL_DIR = "models/final/"

# Download those files
for obj in bucket.objects.filter(Prefix=S3_MODEL_DIR):
    s3_file = obj.key
    local_file = os.path.join(LOCAL_MODEL_DIR, os.path.basename(s3_file))
    stdout.write("Downloading {} and writing to {}\n".format(s3_file, local_file))
    try:
        bucket.download_file(s3_file, local_file)
        stdout.write("Done\n")
    except IsADirectoryError:
        stdout.write("Skipping. This is a directory\n")
