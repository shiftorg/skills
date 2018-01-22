# Scraping Job Descriptions: Methodology
_Skill Recommendation and Salary Projection_

## Scraping Process
1. For each company, create  list of open jobs.
  - Find the "/company.com/careers" page
  - (If necessary: find each individual team's page. Software, operations, etc.)
  - Examine each link. Actual job description (JD) pages tend to follow a pattern. Compile the job description links into a list.
2.  Loop through each JD page. Use `BeautifulSoup` and `requests` to pull all of the *visible* text off of job description page. (`selenium` or other headless browser technology hasn't been necessary so far. Companies don't seem to care about people scraping their jobs.)
3. Clean the data. Remove all nonsense text (various CTAs on the page, lines like _"Here at Uber, we believe that..."_, etc).

**Result**: clean, lowercase chunks of 'meat' from the each job description, labelled by the JD's title and company.

## Relevant files in this directory
- `extract_meat.ipynb`
  - After extracting the full visible text for each JD, clean up the text so that only the useful lines remain.
  - (Some of the references to files are broken after re-organizing)
- `./analysis/jd_meat_analysis.ipynb`
  - Use TD-IDF to extract the most useful/important terms from JDs
  - Just for fun, try to use the text in a JD (minus company names) to predict a company. (96% accuracy on held-out test data.)
  - Cluster jobs based on TF-IDF values.
  - Conduct PCA and plot the clusters in two and three dimensions
- _I removed the directories related to scraping JDs -- it's pretty straightforward._
