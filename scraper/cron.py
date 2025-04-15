import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scraper.models import Linkedin
from job.models import Location, Search


# Set up Chrome
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")        # Run in headless mode
options.add_argument("--force-device-scale-factor=0.25")

driver = webdriver.Chrome(options=options)
driver.get("https://www.linkedin.com")
time.sleep(2)

# Clear existing cookies
driver.delete_all_cookies()

# Inject li_at cookie for selenium
se_cookie = {
    'name': 'li_at',
    'value': Linkedin.objects.first().li_at_cookie,
    'domain': '.linkedin.com',
    'path': '/',
    'secure': True,
    'httpOnly': True
}


driver.add_cookie(se_cookie)


locations = Location.objects.all().values_list(flat=True)
keywords = Search.objects.all().values_list(flat=True)


def search_linkedin_jobs():
    for page in range(40):
        for location in locations:
            for keyword in keywords:
                # Target URL (LinkedIn profile, job listings, etc.)
                # f_TPR=r2592000 => This MONTH Time Filter 
                # f_JT=F%2CC => FULL_TIME and CONTRACT job filter
                # f_E=2%2C3%2C4%2C5%2C6 => ENTRY_LEVEL,MID_SENIOR,ASSOCIATE,Director,Executive experiance level filter
                # f_WT=1%2C3 => ON_SITE and HYBRID job filter
                url = f'https://www.linkedin.com/jobs/search?keywords={keyword}&location={location}&f_TPR=r2592000&f_JT=F%2CC&f_E=2%2C3%2C4%2C5%2C6&f_WT=1%2C3&start={page*25}'        
                # get list of jobs
                driver.get(url)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                # sleep 10 sec until full load
                # time.sleep(10)
                links = [a['href'] for a in soup.find_all('a', href=True)]
                jobs = list(set([link for link in links if link.startswith('/jobs/view/')]))
                job_ids = gathered_jobs()
                # append new jobs to jobs csv
                for job in jobs:
                    if job.split("/")[3] not in job_ids:
                        with open('./data/jobs.csv','a') as fd:
                            fd.write(f'{job.split("/")[3]},https://www.linkedin.com{job}')
                            fd.write("\n")
                # append new jobs to new_jobs csv
                for job in jobs:
                    if job.split("/")[3] not in job_ids:
                        with open('./data/new_jobs.csv','a') as fd:
                            fd.write(f'{job.split("/")[3]},https://www.linkedin.com{job}')
                            fd.write("\n")