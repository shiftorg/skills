
# ingest_raw

This service is responsible for taking raw job description data and storing it in an object store. For now, this is a public S3 bucket. This service is responsible for knowing the details of where we store data in its rawest form.

All ETL code that hits data services (e.g. API calls, selenium scraping, other schemes) will send data to this thing.
