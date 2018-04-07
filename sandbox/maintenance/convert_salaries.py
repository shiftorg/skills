
import json
from SkillsBucket import SkillsBucket
from sys import stdout


def get_ndjson(obj, jobType):
    """
    Given an S3 object that points to a JSON file,
    read it into memory and return an ndjson string
    representation
    """
    json_content = json.loads(obj.get()['Body'].read().decode('utf-8'))
    output_records =[]
    for record in json_content:
	output_record = {}
	company = record['company']
	jobTitle = record['jobTitle']
	actualTitle = jobTitle
	salary = record['meanPay']
	salaryType = "annual"
	if "hourly" in actualTitle.lower():
		actualTitle = jobTitle.split("-")[0]
		salaryType = "hourly"

	output_record["rawTitle"] = jobTitle
	output_record["title"] = actualTitle.strip().title()
	output_record["salaryType"] = salaryType.strip().title()
	output_record["salary"] = salary
 	output_record["company"] = company.strip().title()
	output_record["jobType"] = jobType.strip().title()
	
	output_records.append(output_record)	
    ndjson = '\n'.join([json.dumps(output_record) for output_record in output_records])
    return(ndjson)


stdout.write("Converting salary files to ndjson...\n")
bucket = SkillsBucket()
job_types = {
	"app+developer": "App Developer", 
	"business+intelligence": "Business Intelligence", 
	"customer+success": "Customer Success", 
	"data+analyst": "Data Analyst",
	"senior+data+analyst": "Data Analyst",
	"senior+data+scientist": "Data Scientist",
	"senior+software+engineer": "Software Engineer",
	"principal+software+engineer": "Software Engineer",
	"data+scientist": "Data Scientist", 
	"database+administrator": "DBA", 
	"senior+database+administrator": "DBA",
	"senior+software+engineering+manager" : "Software Engineering Manager",
	"staff+software+engineer": "Software Engineer",
	"senior+test+engineer": "Test Engineer",
	"devops": "DevOps", 
	"software+engineer": "Software Engineer",
	"product+manager": "Product Manager", 
	"senior+product+manager": "Product Manager",
	"product+marketing": "Product Marketing", 
	"program+manager": "Program Manager", 
	"test+engineer": "Test Engineer", 
	"release+engineer": "Release Engineer", 
	"sales+engineer": "Sales Engineer", 
	"software+architect": "Software Architect", 
	"software+consultant": "Software Consultant", 
	"software+engineering+manager": "Software Engineering Manager", 
	"data+engineer": "Data Engineer", 
	"frontend+engineer": "FrontEnd Engineer", 
	"mobile+engineer": "Mobile Engineer", 
	"quality+engineer": "Quality Engineer"
	}
for obj in bucket.files(prefix="salaries/"):
    this_obj_key = obj.key
    jobTypeTerm = this_obj_key.split("/")[1]
    jobType = job_types[jobTypeTerm]
    stdout.write("Processing {}\n".format(this_obj_key))
    ndjson = get_ndjson(obj, jobType)
    #print ndjson
    assert isinstance(ndjson, str)
    # PSA THIS IS A HACK
    # I couldn't figure out how to get logstash to do this because
    # $ is a special character
    ndjson = ndjson.replace("$", "")
    # upload that file to S3
    s3_file = obj.key.replace('salaries/', 'salaries-3/')
    #print type(s3_file)
    #print s3_file
    bucket.put_bytes(body=ndjson.encode('utf-8'), s3_file=s3_file)
    stdout.write("Done\n")

stdout.write("Done uploading ndjson files Have a great day.\n")
