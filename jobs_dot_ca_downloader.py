import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import requests
import datetime
import concurrent.futures
import re
import sys
EXTRA_POSTINGS = '--extra' in sys.argv
BASE_URL = 'https://www.jobs.ca/search/' if EXTRA_POSTINGS else 'https://www.itjobs.ca/en/'
SORT_ORDER = 1      # sort by: date

def generate_query_params(sort_order: int, page: int) -> str:
    """
    Generates the query parameters for the url

    :param sort_order: 0 -> relevance, 1 -> date
    :param page: Page number
    :return: String of query parameters
    """
    return f'?{"keywords=Information+Technology&" if EXTRA_POSTINGS else ""}sort_order={sort_order}&page={page}'

def get_page_data(page: int):
    """
    Gets and parses all the information on a page.

    :param page: The page number to parse
    :return: Dataframe with the following columns: date, 
        job title, company, location, and link, populated with
        the data from the page.
    """
    r = requests.get(BASE_URL + generate_query_params(SORT_ORDER, page))
    soup = BeautifulSoup(r.text, 'html.parser')
    page_data = []
    print('Parsing page {}'.format(page))
    # Loop for all results on the page
    for posting in soup.find_all('div', {'class': 'result-item'}):
        posting = posting.find('div', {'class': 'result-info-wrapper'})
        # get date
        date = posting.find('a', {'class': 'date'}).string.strip()
        date = datetime.datetime.strptime(date, "%B %d %Y")
        # get job title
        job_title = posting.find('a', {'class': 'offer-name'})
        job_title = list(job_title.children)[0].strip()
        # get company
        company = posting.find('a', {'class': 'company'}).string
        # get location
        location = posting.find('a', {'class': 'location'}).string.strip()
        location = ' '.join(re.split(r"\s+", location))
        # get link
        link = posting.find('a', {'class': 'offer-name'})['href']
        # combine the row info
        row_info = {
            "date": date,
            "job_title": job_title,
            "company": company,
            "location": location,
            "link": link,
        }
        page_data.append(row_info)
    # Make a dataframe with the row information
    page_data = pd.DataFrame(page_data)
    return page_data

# initial request, get the number of pages
r = requests.get(BASE_URL + generate_query_params(SORT_ORDER, 1))
soup = BeautifulSoup(r.text, 'html.parser')
# find the last page number
num_pages = soup.find('div', {"class": "pager-numbers"}).findAll('a')[-1].string
num_pages = int(num_pages)
print('Total number of pages: {}'.format(num_pages))
# start with an empty data frame
data_frame = pd.DataFrame()

# start the thread pool
with concurrent.futures.ThreadPoolExecutor() as executor:
    # submit all the pages to the queue
    page_data = {executor.submit(get_page_data, page_num): page_num for page_num in range(1, num_pages+1)}
    # Process each request as they are created
    for future in concurrent.futures.as_completed(page_data):
        page_num = page_data[future]
        print('Processing page {}'.format(page_num))
        try:
            data = future.result()
        except Exception as exc:
            print('Page %r generated an exception: %s' % (page_num, exc))
        else:
            # combine the dataframe together
            data_frame = pd.concat([data_frame, data])

# reset the index of the dataframe
data_frame = data_frame.reset_index(drop=True)
print(data_frame)
print('Saving to "jobs_dot_ca_output.csv"')
data_frame.to_csv('jobs_dot_ca_output.csv', index=False)
