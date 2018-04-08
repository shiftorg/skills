import time
import json
import Salary
import csv
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from GlassdoorCsvRow import GlassdoorCsvRow
import boto3

username = "###" # your email here
password = "###" # your password here


# Manual options for the city, num pages to scrape, and URL
pages = 6
#cityName = "new-york-city"
#cityURL = "https://www.glassdoor.com/Salaries/new-york-city-data-scientist-salary-SRCH_IL.0,13_IM615_KO14,28.htm"
BUCKET_NAME = 'tech-salary-project'
s3 = boto3.resource('s3')

def obj_dict(obj):
    return obj.__dict__
#enddef

def json_export(data, location, title):
        file_name = title + "_" + location + "_" + str(int(time.time())) + ".json"
        s3_key = "{}/{}/{}/{}".format("salaries", title, location, file_name)
	jsonFile = open(file_name, "w")
	jsonFile.write(json.dumps(data, indent=4, separators=(',', ': '), default=obj_dict))
	jsonFile.close()
        s3.Bucket(BUCKET_NAME).put_object(Key=s3_key, Body=open(file_name, 'rb'))
#enddef

def init_driver():
    #driver = webdriver.Chrome(executable_path = "./chromedriver")
    driver = webdriver.Chrome('/Users/Raghu/Downloads/chromedriver')
    driver.wait = WebDriverWait(driver, 10)
    return driver
#enddef

def login(driver, username, password):
    driver.get("http://www.glassdoor.com/profile/login_input.htm")
    try:
        user_field = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "username")))
        pw_field = driver.find_element_by_css_selector("input[type='password']")
        #pw_field = driver.findElement(By.cssSelector("input[type='password']"));
	#pw_field = driver.find_element_by_class_name("signin-password")
        login_button = driver.find_element_by_xpath("//button[@type='submit']")
        #login_button = driver.find_element_by_id("signInBtn")
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        time.sleep(random.randint(1100,2300)/1000.0)
        pw_field.send_keys(password)
        time.sleep(random.randint(1100,2300)/1000.0)
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")
#enddef

def parse_salaries_HTML(salaries, data):
	for salary in salaries:
		jobTitle = "-"
		company = "-"
		meanPay = "-"
		jobTitle = salary.find("div", { "class" : "JobInfoStyle__jobTitle"}).find("a").getText().strip()
		company = salary.find("div", { "class" : "JobInfoStyle__employerName"}).getText().strip()
		try:
			meanPay = salary.find("div", { "class" : "JobInfoStyle__meanBasePay"}).find("span", {"class": "strong"}).getText().strip()
		except Exception as e:
                        print(str(e))
			meanPay = 'xxx'
		r = Salary.Salary(jobTitle, company, meanPay)
		data.append(r)
	#endfor
	return data
#enddef

def get_data(driver, URL, startPage, endPage, data, refresh):
	if (startPage > endPage):
		return data
	#endif
	print "\nPage " + str(startPage) + " of " + str(endPage)
	currentURL = URL + "_IP" + str(startPage) + ".htm"
	time.sleep(random.randint(2100,2400)/1000.0)
	#endif
	if (refresh):
		driver.get(currentURL)
		print "Getting " + currentURL
	#endif
	time.sleep(random.randint(2100,2300)/1000.0)
	HTML = driver.page_source
	soup = BeautifulSoup(HTML, "html.parser")
	salaries = soup.find("div", { "class" : ["salaryList"] }).find_all("div", { "class" : ["SalaryRowStyle__row"] })
	if (salaries):
		data = parse_salaries_HTML(salaries, data)
		print "Page " + str(startPage) + " scraped."
		if (startPage % 10 == 0):
			print "\nTaking a breather for a few seconds ..."
			time.sleep(10)
		#endif
		get_data(driver, URL, startPage + 1, endPage, data, True)
	else:
		print "Page could not be loaded..ignoring the page"
		time.sleep(3)
		#get_data(driver, URL, startPage, endPage, data, False)
	#endif
	return data
#enddef

if __name__ == "__main__":
	driver = init_driver()
	time.sleep(3)
	print "Logging into Glassdoor account ..."
	login(driver, username, password)
	time.sleep(10)
        print 'logged in..'
	print 'parsing the glassdoor-urls.csv file..'
    	csvRows = []
    	with open('glassdoor-urls.csv') as csvFile:
        	reader = csv.DictReader(csvFile, delimiter=',', quotechar='"')
        	for row in reader:
            		csvRows.append(GlassdoorCsvRow(row['title'], row['location'], row['url']))
     
    	print "\nStarting data scraping ..."       
    	for csvRow in csvRows:
                location = csvRow.location
		title = csvRow.title
		url = csvRow.url
                print 'location:{}'.format(location)
		print 'title:{}'.format(title)
		print 'url:{}'.format(url)
		data = get_data(driver, url[:-4], 1, pages, [], True)
            	print "\nExporting data to " + title + "_" + location + ".json"
            	json_export(data, location, title)
                
	driver.quit()
