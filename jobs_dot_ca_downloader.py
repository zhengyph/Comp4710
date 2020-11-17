import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import requests
import datetime
import concurrent.futures
import re
urls = {
    'Human Resources': 'https://www.hrjob.ca',
    'Finance': 'https://www.jobwings.ca/en/',
    'Project Management': 'https://www.pmjobs.ca/',
    'Legal': 'https://www.legaljobs.ca/',
    'Paralegal': 'https://www.paralegaljobs.ca/',
    'Sales': 'https://www.salesrep.ca/en/',
    'Information Technology': 'https://www.itjobs.ca/en/',
    'Retail': 'https://www.retail.ca/',
    'Call Centre': 'https://www.callcentrejob.ca/',
    'Administative': 'https://www.adminjobs.ca/en/',
    'Engineering': 'https://www.techjobs.ca/en/',
    'Accounting': 'https://www.accountingjobs.ca/',
    'Business Analyst': 'https://www.bajobs.ca/en/',
    'Pharmaceutical': 'https://www.pharmaceutical.ca/',
    'Healthcare': 'https://www.healthcarejobs.ca/',
    'Aeronautical': 'https://www.aerojobs.ca/en/',
    'Hospitality': 'https://www.hospitalityjobs.ca/en/',
}
SORT_ORDER = 1      # sort by: date

def generate_query_params(sort_order: int, page: int) -> str:
    """
    Generates the query parameters for the url

    :param sort_order: 0 -> relevance, 1 -> date
    :param page: Page number
    :return: String of query parameters
    """
    return f'?sort_order={sort_order}&page={page}'

def get_page_data(category: str, page: int):
    """
    Gets and parses all the information on a page.

    :param page: The page number to parse
    :return: Dataframe with the following columns: date, 
        job title, company, location, and link, populated with
        the data from the page.
    """
    r = requests.get(urls[category] + generate_query_params(SORT_ORDER, page))
    soup = BeautifulSoup(r.text, 'html.parser')
    page_data = []
    print('Loading {} page {}'.format(category, page))
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
            "category": category,
            "link": link,
        }
        page_data.append(row_info)
    # Make a dataframe with the row information
    page_data = pd.DataFrame(page_data)
    return page_data

def get_num_pages(category: str):
    print(f"Getting number of pages for {category}")
    # initial request, get the number of pages
    r = requests.get(urls[category] + generate_query_params(SORT_ORDER, 1))
    soup = BeautifulSoup(r.text, 'html.parser')
    # find the last page number
    num = soup.find('div', {"class": "pager-numbers"}).findAll('a')[-1].string
    return int(num)

# start with an empty data frame
data_frame = pd.DataFrame()
# start the thread pool
with concurrent.futures.ThreadPoolExecutor() as executor:
    category_numbers = {executor.submit(get_num_pages, category): category for category in urls.keys()}

    page_data = dict()
    for future in concurrent.futures.as_completed(category_numbers):
        category = category_numbers[future]
        num_pages = future.result()
        print(f'Number of pages for {category}: {num_pages}')
        for num in range(1, num_pages+1):
            page_data[executor.submit(get_page_data, category, num)] = f"{category} page {num}"

    # Process each request as they are created
    for future in concurrent.futures.as_completed(page_data):
        page_identifier = page_data[future]
        print('Processing {}'.format(page_identifier))
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (page_identifier, exc))
        else:
            # combine the dataframe together
            data_frame = pd.concat([data_frame, data])

# reset the index of the dataframe
data_frame = data_frame.reset_index(drop=True)
print(data_frame)
print('Saving to "jobs_dot_ca_output.csv"')
data_frame.to_csv('jobs_dot_ca_output.csv', index=False)
