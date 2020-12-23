import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
import concurrent.futures
import re

keywords = [
    'Accomodation',
    'Food',
    'Publishing',
    'Recording',
    'Broadcasting',
    'Telecommunications',
    'Hosting',
    'Recreation',
    'Construction',
]

def get_jobs_dot_ca_number(keyword: str) -> int:
    url = 'https://www.jobs.ca/search/?keywords={}'.format(keyword)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    

