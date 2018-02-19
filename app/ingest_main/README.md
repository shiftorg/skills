
# ingest_main

This service is responsible for taking raw job description data stored in S3, converting them to our schema, and writing them to whatever we choose as a persistent store (Elasticsearch, for now).
