import pandas as pd
import numpy as np

# Uncomment to apply apriori on different files
#file = 1 # If file is 1, then aplly apriori on jobs_dot_ca_output.csv
file = 2  # If file is 2, then aplly apriori on jobs_dot_ca_search_downloader.csv

# Load data from csv file
def load_data_set():
    if(file == 1):
      data_set = pd.read_csv("jobs_dot_ca_output.csv", usecols=[
                          "job_title", "company", "location", "category"])
    if(file == 2):
      data_set = pd.read_csv("jobs_dot_ca_search_output.csv", usecols=[
                           "job_title", "company", "location", "keyword"])

    return data_set

# Generate frequent candidates of 1-itemset
def generate_C1(data_set):
    C1 = set()
    data_set = data_set.values.tolist()
    for t in data_set:
        for item in t:
            item_set = frozenset([item])
            C1.add(item_set)

    return C1;

# Prune candidates
def prune(Ck_item, LkSub1):
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in LkSub1:
           return True
    return False

# Generate frequent candidates of k-itemset
def generate_Ck(LkSub1, k):
    Ck = set()
    len_LkSub1 = len(LkSub1)
    list_LkSub1 = list(LkSub1)
    for i in range(len_LkSub1):
        for j in range(1, len_LkSub1):
            l1 = list(list_LkSub1[i])
            l2 = list(list_LkSub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
               Ck_item = list_LkSub1[i] | list_LkSub1[j]
               if not prune(Ck_item, LkSub1):
                  Ck.add(Ck_item)
    return Ck

# Generate Lk by Ck
def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    Lk = set()
    item_count = {}
    data_set = np.array(data_set)

    for t in data_set:
        for item in Ck:
            if item.issubset(t):
               if item not in item_count:
                  item_count[item] = 1;
               else:
                  item_count[item] += 1;

    t_num = float(len(data_set))

    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk

# Generate all frequent itemsets
def generate_L(data_set, k, min_support):
    support_data = {}
    C1 = generate_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    LkSub1 = L1.copy()
    L = []
    L.append(LkSub1)
    for i in range(2, k+1):
        Ci = generate_Ck(LkSub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        LkSub1 = Li.copy()
        L.append(LkSub1)
    return L, support_data

# Generate association rules
def generate_assoc_rules(L, support_data, min_conf):
        assoc_rules_list = []
        sub_set_list = []
        for i in range(0, len(L)):
            for freq_set in L[i]:
                for sub_set in sub_set_list:
                    if sub_set.issubset(freq_set):
                        conf = support_data[freq_set] / support_data[freq_set - sub_set]
                        assoc_rule = (freq_set - sub_set, sub_set, conf)
                        if (conf >= min_conf) and (assoc_rule not in assoc_rules_list):
                            assoc_rules_list.append(assoc_rule)
                sub_set_list.append(freq_set)
        return assoc_rules_list

# Main
if __name__ == '__main__':
    data_set = load_data_set()
    ms = 0
    mf = 0
    if(file == 1):
      ms = 0.01
      mf = 0.5
    if(file == 2):
      ms = 0.03
      mf = 0.9
    L, support_data = generate_L(data_set, k=3, min_support=ms)
    assoc_rules_list = generate_assoc_rules(L, support_data, min_conf = mf)

    if len(list(L)) > 0:
        for Lk in L:
            print("=" * 50)
            if len(list(Lk)) > 0:
                print("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
                print("=" * 50)
                for freq_set in Lk:
                    print(freq_set, support_data[freq_set])
            else:
                print("Null") 
        print('\n'+"Association Rules")
        if len(assoc_rules_list) > 0:
            for item in assoc_rules_list:
                print(item[0], "=>", item[1], "conf = ", item[2])
        else:
            print("Null")


