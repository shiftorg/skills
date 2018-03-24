import boto3


class SkillsBucket:
    """
    Connect to the project S3 bucket. Assumes that you already
    have your creds in the standard format in ~/.aws/credentials
    """
    def __init__(self, bucket_name="tech-salary-project"):
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket(bucket_name)

    def files(self, prefix=""):
        """
        Stream all files matching some pattern.
        This method is an iterator and will yield one file
        at a time.
        """
        return(self.bucket.objects.filter(Prefix=prefix))

    def put_bytes(self, body, s3_file):
        assert isinstance(body, bytes)
        assert isinstance(s3_file, str)
        print("Putting object to S3 path {}".format(s3_file))
        self.bucket.put_object(Key=s3_file, Body=body)
        print("Done")
