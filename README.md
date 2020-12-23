# COMP 4710 Project
Author:
    
    Yan Wen
    
    Joshua Smallwood
    
    Chenru Zhao
    
    Hao Zheng
    
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
There are two csv files, please uncomment the file that you would like to do frequent pattern mining on. You need to do frequent pattern mining on both of them to get our result.
