
import json
from SkillsBucket import SkillsBucket
from sys import stdout


def get_ndjson(obj):
    """
    Given an S3 object that points to a JSON file,
    read it into memory and return an ndjson string
    representation
    """
    json_content = json.loads(obj.get()['Body'].read().decode('utf-8'))
    ndjson = '\n'.join([json.dumps(x) for x in json_content])
    return(ndjson)


stdout.write("Converting salary files to ndjson...\n")
bucket = SkillsBucket()
for obj in bucket.files(prefix="salaries/"):
    this_obj_key = obj.key
    stdout.write("Processing {}\n".format(this_obj_key))
    ndjson = get_ndjson(obj)
    assert isinstance(ndjson, str)
    # PSA THIS IS A HACK
    # I couldn't figure out how to get logstash to do this because
    # $ is a special character
    ndjson = ndjson.replace("$", "")
    # upload that file to S3
    s3_file = obj.key.replace('salaries/', 'salaries_ndjson/')
    bucket.put_bytes(body=ndjson.encode('utf-8'), s3_file=s3_file)
    stdout.write("Done\n")

stdout.write("Done uploading ndjson files Have a great day.\n")
