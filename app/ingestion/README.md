
# Ingestion

This directory holds files related to ingesting raw data into elasticsearch for analysis.

To get the ES cluster up and running locally and seed it with data from S3, run the following (starting from `app/` directory)

```
docker-compose up -d
cd ingestion

# do this only if you don't already have this information in the environment somewhere
export S3_KEY="your_S3_access_key"
export S3_SECRET="your_s3_secret_key"

bash seed_es.sh
```
