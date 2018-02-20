#!/usr/bin/python

import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import requests
import random
import pandas as pd
import boto3
import botocore
import json
import logging

# Locations in Bay Area, CA where there many jobs for each search term (for ex: Software Engineer), so, let use a smaller radius
# than the default of 25miles. With this smaller radius, there is lesser chance of crossing 1000. While paginating through next links,
# indeed.com only allows a max of 1000. 
LOCATIONS_BAY_AREA_CA = {
             "San+Jose%2C+CA":10, 
             "Los+Altos%2C+CA":10,
             "Sunnyvale%2C+CA":10,
             "Mountain+View%2C+CA":10,
             "Palo+Alto%2C+CA":10,
             "Redwood+City%2C+CA":10,
             "San+Mateo%2C+CA":10,
             "San+Francisco%2C+CA":10,
             "Milpitas%2C+CA":10,
             "Fremont%2C+CA":10,
             "Dublin%2C+CA":10, 
             "Foster+City%2C+CA":10
             }
      
# other locations in CA       
LOCATIONS_OTHER_CA = {
                      "Los+Angeles%2C+CA":50,
                      "Sacramento%2C+CA":50
                      }

# other locations in US
LOCATIONS_OTHER_STATES = {
                          "Texas":50,
                          "Washington+State":50,
                          "Florida":50,
                          "North+Carolina":50,
                          "Washington+DC":50,
                          "Oregon":50,
                          "Arizona":50,
                          "New+York+State":50,
                          "New+Jersey":50,
                          "Massachusetts":50,
                          "Utah":50,
                          "Colorado":50,
                          "Nevada":50,
                          "Georgia":50,
                          "Pennsylvania":50
                          }
                          

BUCKET_NAME = 'tech-salary-project'
s3 = boto3.resource('s3')
# this is the set of unique job ids - we ensure that we only scrape jobs once and dont do additional work
unique_job_ids = set()


def main():
    # get search term from the arguments
    search_terms = sys.argv[1:]
    # if there are multiple terms, we need to URL encode
    search_string = '+'.join(search_terms)
    print("Search String: {}".format(search_string))
    # logger
    logging.basicConfig(filename="indeed-scraper-{}.log".format(search_string), level=logging.INFO)
    scrape(search_string)
    
    
def scrape(search_term):
    locations={}
    locations.update(LOCATIONS_BAY_AREA_CA)
    locations.update(LOCATIONS_OTHER_CA)
    locations.update(LOCATIONS_OTHER_STATES)
    #start_url = "https://www.indeed.com/jobs?q=title%3A%28{}%29&l=Texas&radius=50&limit=50&start=50"
    for location in locations:
        try:
            scrape_search_location(search_term, location, locations[location])
        except Exception as e:
            logging.error("Failed to scrape for search_term:{}, location:{}. Exception:{}".format(search_term, location, str(e)))
            continue  # or you could use 'continue'
        
    log("Completed scraping {} jobs for Search:{}".format(len(unique_job_ids), search_term))
 
def scrape_search_location(search_term, location, radius):
    # sleep a random number of seconds
    sleep_non_bot()
    log("Search:{} in Location:{} within Radius:{}".format(search_term, location, str(radius)))
    # URl with the query parameter for location, search term and limit. We do not use "start={}" parameter here. This is the starting point.
    search_start_url = "https://www.indeed.com/jobs?q=title%3A%28{}%29&l={}&radius={}&limit=50".format(search_term, location, str(radius))
    #scrape page 0
    soup = scrape_jobs_page(search_start_url, search_term, location, 0)
 
    #find how many more pages to scrape
    search_counts = None
    try:
        search_counts = soup.find(id = 'searchCount').string.encode('utf-8').split() #this returns the total number of results
    except Exception as e:
        logging.error("Failed to get the number of search counts for search_term:{}, location:{}. Exception:{}".format(search_term, location, str(e)))
        return

    if not search_counts:
        log("Could not get the number of search counts")
        return
    
    num_search_results = int(search_counts[3].replace(',',''))
    log("Nummber of search results:{}".format(str(num_search_results)))
    if num_search_results < 50:
        log("No additional pages for Search:{} in Location:{} within Radius:{}".format(search_term, location, str(radius)))
        return
    
    num_pages = num_search_results//50 + 1
    log("Number of pages:{}".format(str(num_pages)))
    
    for page_number in range(1, num_pages):
        sleep_non_bot()
        start_from = 50 * page_number
        #NOTE: the start={} is required here when we paginate.
        search_url = search_start_url + "&start={}".format(str(start_from))
        try:
            scrape_jobs_page(search_url, search_term, location, page_number)
        except Exception:
            logging.error("Failed to scrape for search_term:{}, location:{}, PagNumber:{}. Exception:{}".format(search_term, location, 
                          str(page_number), str(e)))
            continue
    

def scrape_jobs_page(search_url, search_term, location, page_number):
    log("Scraping URL:{}".format(search_url))
    
    search_page = requests.get(search_url)
    soup = BeautifulSoup(search_page.text, "html.parser")
    job_ids = extract_job_ids_from_page(soup)
    
    log("Number of job ids in the url:{} is {}".format(search_url, str(len(job_ids))))
    
    out_file_name = search_term + "_" + location + "_Page{}_".format(str(page_number)) + str(int(time.time()))    
    log("Scraping jobs in the URL:{} into file:{}".format(search_url, out_file_name))
    # save file locally and also to S3. One file contains all the job information (around 50) in one page
    scrape_jobs(job_ids, out_file_name) 
    data = open(out_file_name, 'rb')
    s3_key = "{}/{}/{}".format(search_term,location,out_file_name)
    
    log("Writing jobs to s3 with key={}".format(s3_key))
    
    s3.Bucket(BUCKET_NAME).put_object(Key=s3_key, Body=data)
    
    return soup     
        
  
def scrape_jobs(job_ids, out_file_name):
    job_jsons = []
    for job_id in job_ids:
        job_json = scrape_job(job_id)
        if (job_json):
            job_jsons.append(job_json)
            
    with open(out_file_name, 'w+') as outfile:
        for job_json in job_jsons:
           outfile.write("{}\n".format(job_json)) 
        
 
        
def scrape_job(job_id):
    # do not scrape a job page if we already did that before (in the current run of the script)
    if (job_id in unique_job_ids):
        log("Job:{} has already been scraped".format(job_id))
        return {}
    unique_job_ids.add(job_id)

    sleep_non_bot()
    # NOTE: the trick here is NOT to load the "classis" indeed page - use the mobile link for a job given the jobId.
    job_link_url = "https://www.indeed.com/m/viewjob?jk={}".format(job_id)
    logging.info("Scraping Job URL:{}".format(job_link_url))
    job_link_page = requests.get(job_link_url)
    job_link_soup = BeautifulSoup(job_link_page.text, "html.parser")
    job_listing_json=extract_job_listing(job_id, job_link_url, job_link_soup)
    return job_listing_json
    
def extract_job_listing(job_id, job_link_url, job_link_soup):
    job_listing = {}
    job_listing["id"] = job_id
    job_listing["url"] = job_link_url
    job_listing["title"] = job_link_soup.body.p.b.text.strip()
    job_listing["companyName"] = job_link_soup.body.p.b.next_sibling.next_sibling.string.strip().split("-")[0].strip()
    job_listing["location"] = job_link_soup.body.p.span.text.strip()
    job_listing["summary"] = job_link_soup.find(name="div", attrs={"id":"desc"}).prettify()
    job_listing["salary"] = "Not_Found"
    job_listing["scrapeTime"] = int(time.time())
    return json.dumps(job_listing)
    
def extract_job_ids_from_page(soup): 
    job_ids = []
    # find all the job ids in a single page
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        job_ids.append(div["data-jk"])
    return(job_ids)

def log(msg):
    print(msg)
    logging.info(msg)
    
def sleep_non_bot():
    sleep_time = random.randint(1100,2300)/1000.0
    #print("Sleeping for time={} seconds".format(str(sleep_time)))
    logging.info("Sleeping for time={} seconds".format(str(sleep_time)))
    time.sleep(sleep_time) #waits for a random time so that the website don't consider you as a bot

# Usage: python indeed-scraper.py <search-term>
if __name__ == "__main__":
    main()