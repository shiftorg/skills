How to scrape glassdoor
---------------------
---------------------


## Command

```
python glassdoor-scraper.py 
```

The command will spit out objects into S3 of the form salaries/title/location1/title_location1.json, salaries/title/location1/title_location1.json, etc. The files of the same structure are written out locally too, in case we want to cleanup/reprocess before uploading to S3. The local files avoid re-scraping.

The script expects a file glassdoor-urls.csv to be present. This CSV should have rows with 3 columns - title, location, url. Note that the glassdoor urls are not easy to construct programatically. So, here are the steps to come up with this CSV:
1. Go to glassdoor.com, enter the job title and location and hit enter. 
2. Copy the job title, location and the url that loads up as a row in the CSV.
3. Name that glassdoor-urls.csv and save that in this directory.

## How does this script scrape?
This scripts reuses a lot of code from https://github.com/ajbentley/glassdoor-salary-scraper

That project is old and did not work - so, I made changes on top of that by hacking around the glassdoor login, salary pages, saving to local disk and uploads to s3.

The script first logs into glassdoor.com with the creds you use in the script (commented section for creds). For every row in the csv, it uses selenium to launch a browser with that url and parses out the salary, company, location for every single listing in the first 6 pages (~60 salary+company+location combinations).

Once this information is scraped, the data is first saved to the local disk and then uploaded into s3.

## Next steps
The glassdoor-urls-1.csv and glassdoor-urls-2.csv has the information on the salaries we already scraped. If there are any other locations, jobs for which we want to scrape salaries, we can run the script again.
