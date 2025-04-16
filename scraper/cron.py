import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from scraper.models import Linkedin
from job.models import Location, Search, Job


# Set up Chrome
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless")        # Run in headless mode
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


locations = Location.objects.all().values_list('keyword', flat=True).distinct()
keywords = Search.objects.all().values_list('keyword', flat=True).distinct()
gathered_jobs = list(Job.objects.all().values_list('job_id', flat=True).distinct())


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
                # sleep 10 sec until full load
                time.sleep(10)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                links = [a['href'] for a in soup.find_all('a', href=True)]
                jobs = [link for link in links if link.startswith('/jobs/view/')]
                job_ids = list(set([job.split("/")[3] for job in jobs]))
                # append new jobs to jobs csv
                for job_id in job_ids:
                    if job_id not in gathered_jobs:
                        Job.objects.create(job_id=job_id)
                        gathered_jobs.append(job_id)
                use_tags = driver.find_elements(By.CSS_SELECTOR, 'use[href="#close-small"]')
                if job_ids:
                    for tag in use_tags:
                        try:
                            #click wrapping <button> if needed
                            button = tag.find_element(By.XPATH, "./ancestor::button")
                            button.click()
                            time.sleep(0.5)
                        except Exception as e:
                            print(f"Failed to click use: {e}")