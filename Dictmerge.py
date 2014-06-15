# Dictmerge
# This will read in a list of grants / trials / papers and, using a dictionary, merge
# Them onto a rank list

import pandas as pd

# Read in the list of cancer key-words
cancer_path = 'C:\Users\JAG\USN-dz\cancers_cases_keys.csv'
cancers = pd.read_csv(cancer_path, index_col=False, header=0)
    
# Read in the rank-list which includes the organizations
RL_path = 'C:\Users\JAG\USN-dz\RL_USN.csv'
RL = pd.read_csv(RL_path, index_col=False, header=0, squeeze=True)


# Read in the dictionary
dict_path = 'C:\Users\JAG\USN-dz\CTgov_dict.csv'
ctgdict = pd.read_csv(dict_path, index_col = False, header = 0, squeeze = True)

array = []

brief_cancers = [deet for deet in cancers['kw1']]
brief_cancers.append('all')


for cancer in brief_cancers:
        
    # Read in the clinical trials
    ctg_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTgov_pivot_vp_' + cancer + '.csv'
    ctg = pd.read_csv(ctg_path, index_col = False, header = 0)

    m1 = ctgdict.merge(ctg, on = 'Institution')
    m1 = m1.groupby('Org name - Ctgov').sum()
    m1['Org name - Ctgov'] = m1.index
    m2 = RL.merge(m1, on = 'Org name - Ctgov', how = 'left')
    m2 = m2.fillna(0)    
    save_path = 'C:\Users\JAG\USN-dz\RL_USN_Ctg_' + cancer + '.csv'
    m2.to_csv(save_path, sep = ',' , index = False, encoding = 'utf-8')
    
    # stripping off extra columns for generating the concatenated array
    m3 = m2.drop(['Institution', 'Search_Term',	'ORG_NAME1', 'ORG_NAME2',
        'ORG_NAME3', 'Locale', 'Rank-USNews', 'Score-USNews', 'Reputation-USNews',
        'Survival-USNews', 'Safety-USNews', 'Volume-USNews', 'Nurse-Staffing-USNews',
        'Magnet-USNews'], axis = 1)
    array.append(m3)
    

ctg_sum = pd.concat(array, axis = 1)
save_path = 'C:\Users\JAG\USN-dz\RL_USN_Ctg_sum.csv'
ctg_sum.to_csv(save_path, sep = ',', index = False, encoding = 'utf-8')
