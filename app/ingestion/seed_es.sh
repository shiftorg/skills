
# break if it breaks
set -e

# globals
export ES_HOST="localhost:9200"

# Upload mappings
echo "Setting up mappings"
curl -X PUT "${ES_HOST}/job_descriptions" -d @jd_mapping.json
curl -X PUT "${ES_HOST}/salaries" -d @salary_mapping.json
echo "Done configuring mappings"

# ingest data from S3 via logstash
echo "Ingesting raw job descriptions from S3"
logstash -f s3_jd.conf
echo "Done ingesting raw job descriptions"
