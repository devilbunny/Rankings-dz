# Dictmerge
# This will read in a list of grants / trials / papers and, using a dictionary, merge
# Them onto a rank list

import pandas as pd

cancers = [['colon', 'colorectal', 'rectal'], ['ovary', 'ovarian', 'endometrioid'], 
        ['breast', 'ductal carcinoma', 'DCIS'], ['lung', 'pulmonary', 'small cell'],
        ['lymphoma', 'leukemia', 'leukaemia'], ['brain', 'glioblastoma', 'astrocytoma', 'glioma'],
        ['pancreas', 'pancreatic'], ['melanoma'], ['basal cell', 'squamous cell', 'actinic keratosis', 'skin'],
        ['pediatric', 'ewing', 'neuroblastoma', 'rhabdomyosarcoma'], ['head and neck'],
        ['prostate', 'prostatic'], ['soft tissue', 'sarcoma'], ['esophagus', 'esophagael', 'esophageal', 'barrett'],
        ['kidney', 'renal', 'clear cell'], ['multiple myeloma', 'myeloma'], 
        ['bladder', 'transitional', 'uroepithelial'], ['liver', 'hepatic', 'hepatocellular'], ['thyroid'],
        ['cervical', 'cervix'], ['metastatic'], ['uterus', 'uterine', 'endometrial'],
        ['gastric', 'pyloric', 'pylori', 'stomach'], ['unknown primary'], ['pheochromocytoma'],
        ['mesothelioma'], ['testicular', 'testicle'], 
        ['myeloproliferative', 'myelodysplastic', 'polycythemia', 'thrombocytosis', 'thrombocythemia', 'mds', 'myelodysplasia'],
        ['hiv'], ['sinonasal', 'nasopharyngeal', 'nasopharyngael'], ['meningioma', 'leoptomeninges'], ['all']]
    
# Read in the rank-list which includes the organizations
RL_path = 'C:\Users\JAG\USnewsy\RL_USN.csv'
RL = pd.read_csv(RL_path, index_col=False, header=0, squeeze=True)


# Read in the dictionary
dict_path = 'C:\Users\JAG\USnewsy\CTgov_dict.csv'
ctgdict = pd.read_csv(dict_path, index_col = False, header = 0, squeeze = True)

array = []


for cancer in cancers:
        
    # Read in the clinical trials
    ctg_path = 'C:\Users\JAG\USnewsy\Clinicaltrials\CTgov_pivot_' + cancer[0] + '_b.csv'
    ctg = pd.read_csv(ctg_path, index_col = False, header = 0, squeeze = True)

    m1 = ctgdict.merge(ctg, on = 'Institution')
    m1 = m1.groupby('Org name - Ctgov').sum()
    m1['Org name - Ctgov'] = m1.index
    m2 = RL.merge(m1, on = 'Org name - Ctgov', how = 'left')
    m2 = m2.fillna(0)    
    save_path = 'C:\Users\JAG\USnewsy\USNdz\RL_USN_Ctg_' + cancer[0] + '_b.csv'
    m2.to_csv(save_path, sep = ',' , index = False, encoding = 'utf-8')
    
    # stripping off extra columns for generating the concatenated array
    m3 = m2.drop(['Institution', 'Search_Term',	'ORG_NAME1', 'ORG_NAME2',
        'ORG_NAME3', 'Locale', 'Rank-USNews', 'Score-USNews', 'Reputation-USNews',
        'Survival-USNews', 'Safety-USNews', 'Volume-USNews', 'Nurse-Staffing-USNews',
        'Magnet-USNews'], axis = 1)
    array.append(m3)
    

ctg_sum = pd.concat(array, axis = 1)
save_path = 'C:\Users\JAG\USnewsy\USNdz\RL_USN_Ctg_sum_b.csv'
ctg_sum.to_csv(save_path, sep = ',', index = False, encoding = 'utf-8')
