# COMP 4710 Project - Group 11
Group Members:
    
    Yan Wen 7848205
    
    Joshua Smallwood 7826555
    
    Chenru Zhao 7830959
    
    Hao Zheng 7870389
    
## Jobs data:
  - https://www.jobs.ca/
  - https://www.hrjob.ca
  - https://www.jobwings.ca/en/
  - https://www.pmjobs.ca/
  - https://www.legaljobs.ca/
  - https://www.paralegaljobs.ca/
  - https://www.salesrep.ca/en/
  - https://www.itjobs.ca/en/
  - https://www.retail.ca/
  - https://www.callcentrejob.ca/
  - https://www.adminjobs.ca/en/
  - https://www.techjobs.ca/en/
  - https://www.accountingjobs.ca/
  - https://www.bajobs.ca/en/
  - https://www.pharmaceutical.ca/
  - https://www.healthcarejobs.ca/
  - https://www.aerojobs.ca/en/
  - https://www.hospitalityjobs.ca/en/
  - https://ca.indeed.com/jobs?l=canada
  - https://www.jobbank.gc.ca/jobsearch/jobsearch?locationstring=&sort=M
  
## Links to datasets
  - [North American Industry Classification System (NAICS) Canada 2017 Version 3.0.](https://www23.statcan.gc.ca/imdb/p3VD.pl?Function=getVD&TVD=1181553)
  - [Employment by industry, monthly, seasonally adjusted and unadjusted, and trend-cycle, last 5 months (x 1,000)](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410035501&pickMembers%5B0%5D=1.1&pickMembers%5B1%5D=3.1&pickMembers%5B2%5D=4.1&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=2018&cubeTimeFrame.endMonth=11&cubeTimeFrame.endYear=2020&referencePeriods=20180101%2C20201101)
  - [job_count.csv](https://github.com/hypzheng/COMP4710/blob/main/job_count.csv)
  - [jobs_dot_ca_output.csv](https://github.com/hypzheng/COMP4710/blob/main/jobs_dot_ca_output.csv)
  - [jobs_dot_ca_search_output.csv](https://github.com/hypzheng/COMP4710/blob/main/jobs_dot_ca_search_output.csv)
## Compile and Run
  
  ### packages used:
  - pandas
  - numpy
  - requests
  - beautifulsoup
  
  ### first run (If you would like to parse data from websites)
       python jobs_dot_ca_downloader.py
       python jobs_dot_ca_search_downloader.py
       python job_count_avg.py

### second run
      python rem_dup_dataset.py
Try to remove duplicates in the dataset to prepare for applying algorithm

### third run
      python apriori.py
There are two csv files, please uncomment the file that you would like to do frequent pattern mining on. You need to do frequent pattern mining on both of them to get our final result.

The apriori_output.txt is the result of applying apriori algorithm on jobs_dot_ca_output.csv which parsed through jobs_dot_ca_downloader.py.

The apriori_output2.txt is the result of applying apriori algorithmon on jobs_dot_ca_search_output.csv which parsed through jobs_dot_ca_search_downloader.py.
