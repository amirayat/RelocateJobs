import os
import sys
import time
import django
from langdetect import detect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Get the path to the project root (one level up from 'scraper')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
# Set the settings module 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# Setup Django
django.setup()


from scraper.models import Linkedin
from job.models import Job
from relocate.models import Relocate
from llm.mistral_ai import has_visa_sponsorship


# Set up Chrome
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless")        # Run in headless mode
options.add_argument("--disable-gpu")     # Optional: avoid some rendering issues
options.add_argument("--no-sandbox")      # Good for Linux
options.add_argument("--disable-dev-shm-usage")  # Good for Linux

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


def check_linkedin_jobs():
    """
    check gathered linkedin jobs
    for relocation, visa sponsorship 
    """
    while True:
        jobs_to_check = Job.objects.filter(checked=False)
        # term conditions in the job details
        relocation_words = ['visa', 'relocat', 'immigra', 'sponsor', 'permit', 'authoriz',
                            'employment pass', 'blue card', 'move', 'moving', 'transfer', 'mobil'
                            'housing', 'accommodation', 'mobility', 'international', 'worldwide']
    
        # if there is no new unchecked Job, wait for 5 min
        if not jobs_to_check.exists():
            time.sleep(5*60)
        
        for job in jobs_to_check:
            job_id = job.job_id
            job_url = f'https://www.linkedin.com/jobs/view/{job_id}/'
            driver.get(job_url)
            try:
                # Wait until a specific element is present
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "main")))
                # locate and click the "See more" button
                see_more = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Click to see more description']"))
                )
                see_more.click()
                # Find the <main> element and get its visible text
                main_text = driver.find_element(By.TAG_NAME, "main").text
                # job offers relocation
                if detect(main_text) == 'en' and any(word in main_text for word in relocation_words) and has_visa_sponsorship(main_text):
                    job.relocation = True
                    # add job to relocate
                    Relocate.objects.create(job_url=job_url, text=main_text)
                # save the job
                job.checked = True
                job.save()
            except Exception as e:
                print(f"Failed to find element: {e}")


if __name__ == "__main__":
    check_linkedin_jobs()