How to scrape indeed
---------------------
---------------------


## Command
python indeed.com <search-string>
The command will spit out objects into S3 of the form <search-string>/location1/<search-string>_page<N>_location1_timestamp, <search-string>/location2/<search_string>_location2_page<N>_timestamp, etc. The files of the same structure are written out locally too, in case we want to cleanup/reprocess before uploading to S3. The local files avoid re-scraping.

Example: python indeed-scraper.py Product Manager
```
Product+Manager/Pennsylvania/Product+Manager_Pennsylvania__Page6_1519075181
Product+Manager/Redwood+City%2C+CA/Product+Manager_Redwood+City%2C+CA__Page0_1519090456
Product+Manager/Redwood+City%2C+CA/Product+Manager_Redwood+City%2C+CA__Page1_1519090458
```

## How does this script scrape?
indeed.com has 2 types of urls - "classic" and "mobile" (which have a "/m/" in the url). You start with a search for a job type and location and it loads the first page with a next link to the next page. The basic scraping includes:
1. Start with a job type. We need to come up with different job types we want to scrape. By default, it matches the search terms in the complete title+description. For example, if you search for "Product Manager" - you may end up with a lot of unrelated results. So, the first thing is to use a syntax like "title:(Product+Manager)" for the search query which ensures that the query matches only the jobs which have both those words in the title.
2. Ideally, we do not want to include location in the search query. But, if we do not include location, we will get a LOT of results. Using selenium or not, we cannot scrape more than 1000 jobs for a given search. So, we need to narrow down the results to less than 1000. Hence we will include some known locations in the query.
3. The location by default seems to use 25miles as the radius. In locations like BayArea cities where there are many tech jobs and cities are close by, there will be a lot of jobs (> 1000) returned for each search which are repeated across cities. So, the idea is to tweak the radius in the query param to only 10miles for high-density-job cities and use states for locations where there are not many tech jobs.
4. For a given search-string + location, first load the landing page, set the page limit to 50 (the max possible, so that we dont scrape many pages). Get the job ids in that page. Get the mobile "/m/viewjob?jk=job_id" link given a job_id and load that page for job description. Note that the mobile link gives us a better way to parse the data and seems like can avoid issues with changing html. Also, find out the number of total results for that search query. Figure out the number of pages we need to go through. Use another neat trick here to avoid using selenium - indeed.com seems to allow loading any page without needing a "next link" by constructing the URl of this form "....&start=1200&limit=5-..."
5. Once we have loaded the jobs in a single page, write to a file, with one JSON per line per job id. The JSON structure would be of this form:
```
{
"id": "unique-id-fromindeed",
"url": "indeed-url-so-that-we-can-load-and-check-if-any-issues",
"title": "parsed-out-job-title",
"scrape_time": "timestamp-when-we-scraped-this",
"company_name": "scraped-out-name-of-company",
"location": "city, state",
"summary": "job-responsibilities-free-form text with the html structure retained",
"salary":"parsed-out-salary-if-any"
}
```
6. Upload the file to S3 with this directory structure: <search-string>/location1/<search-string>_page<N>_location1_timestamp so that we can use prefixes to filter out the data that we need.


## Next steps
The job titles we scraped so far are:
Data Scientist
Data Analyst
UX Engineer
Product Manager
Software Manager
Software Engineer
Database Administrator
UX Designer	
Software Test Engineer
Devops
Sales Engineer
Mobile Engineer
Software Developer
Software Architect
QA Engineer
Quality Assurance Engineer
App Developer
Technical Sales
Frontend Engineer
Data Engineer
Hardware Engineer
Technical Program Manager
Software Consultant
Professional Services

If we need to scrape latest jobs for any of these titles OR any other job titles, we can run the script again.
