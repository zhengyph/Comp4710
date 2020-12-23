import pandas as pd
    
def rem_dup(file):
    df = pd.read_csv(file)
    datalist = df.drop_duplicates()
    datalist.to_csv(file)

if __name__=='__main__':
   rem_dup("jobs_dot_ca_output.csv")
   rem_dup("jobs_dot_ca_search_output.csv")

