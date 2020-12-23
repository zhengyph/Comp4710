from jobs_dot_ca_search_downloader import keywords, get_jobs_dot_ca_records

from bs4 import BeautifulSoup
import requests
import datetime
import concurrent.futures
import re
import pandas as pd

def indeed_numbers() -> pd.Series:
    numbers = pd.Series()
    for keyword in keywords:
        url = 'https://ca.indeed.com/jobs?q={}&l=canada'.format(keyword.lower())
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        count = int(soup.find('div', {'id': 'searchCountPages'}).string.strip().split(' ')[3].replace(',', ''))
        numbers[keyword] = count
    return numbers

def job_bank_numbers() -> pd.Series:
    numbers = pd.Series()
    for keyword in keywords:
        url = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={}&locationstring=&sort=M'.format(keyword.lower())
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        count = int(soup.find('span', {'class': 'found'}).string.replace(',', ''))
        numbers[keyword] = count
    return numbers

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        industry_numbers = {
            executor.submit(indeed_numbers): 'glassdoor',
            executor.submit(get_jobs_dot_ca_records): 'jobs.ca',
            executor.submit(job_bank_numbers): 'canada job bank',
        }

        numbers = pd.DataFrame()
        for future in concurrent.futures.as_completed(industry_numbers):
            identifier = industry_numbers[future]
            result = future.result()
            if identifier == 'jobs.ca':
                result = result.groupby('keyword').count()['date'].rename(identifier)
            numbers[identifier] = result
    print('--------------------')
    print(numbers)
    print('Statistics')
    print(numbers.transpose().describe().drop(['count']))
    print('Saving to "job_count.csv"')
    numbers.to_csv('job_count.csv', index=False)
    