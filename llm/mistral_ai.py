import time
import requests

from .models import LLM


# Mistral AI API Endpoint
llm = LLM.objects.filter(name='Mistral AI').first()
API_KEY = llm.api_key if llm else ''

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# Function to check visa sponsorship in job description
def has_visa_sponsorship(job_description):

    url = "https://api.mistral.ai/v1/chat/completions"
    
    prompt = f"""
    You are an AI assistant analyzing job descriptions to determine the likelihood of visa sponsorship.  

    Rules:  
    - return **"1"** if it mentions any form of visa sponsorship (including phrases like "visa support", "relocation assistance", "work authorization provided", "sponsorship available", "visa transfer", etc.).  
    - Otherwise, return **"0"**.  

    Respond with only one of these numbers: **1 or 0**.  

    Job Description:  
    {job_description}
    """

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    time.sleep(1)
    response = requests.post(url, json=data, headers=headers)
    result = response.json()["choices"][0]["message"]["content"].strip()

    out_put = False
    if '1' in result:
        out_put = True

    return out_put