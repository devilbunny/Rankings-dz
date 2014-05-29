# Dictmerge
# This will read in a list of grants / trials / papers and, using a dictionary, merge
# Them onto a rank list

import pandas as pd

top_cancers = [['lung', 'bronch', 'small-cell', 'small cell', 'nsclc', 'sclc', 'smoking'],
            ['prostate', 'prostatic'],
            ['breast', 'ductal carcinoma', 'dcis', 'mammogram', 'mammography'],
            ['colon', 'colorectal', 'rectal', 'rectum', 'polyp'],
            ['pancreas', 'pancreatic'],
            ['liver', 'hepatocellular', 'intrahepatic bile', 'cholangio', 'hepatitis', 'nafld'],
            ['ovary', 'ovarian'],
            ['leukemia', 'cml', 'cll', 'hairy cell', 'leukaemia'],
            ['esophagus', 'esophagael', 'esophageal', 'barrett'],
            ['uterus', 'uterine', 'endometrial', 'endometrium', 'leiomyoma'],
            ['bladder', 'urinary', 'transitional', 'uroepithelial'],
            ['non-hodgkin', 'nhl', 'burkitt', 
                'chronic lymphocytic', 'small lymphocytic',
                'diffuse large b-cell', 'follicular lymphoma',
                'immunoblastic large cell lymphoma',
                'precursor b-lymphoblastic', 'mantle cell',
                'mycosis fungoides', 'cutaneous t-cell',
                'anaplastic large cell', 'precursor t-lymphoblastic', 'lymphoma'],
            ['kidney', 'renal', 'clear cell'],
            ['brain', 'glioblastoma', 'astrocytoma', 'glioma', 'cns',
                 'meningioma', 'leoptomeninges', 'spinal cord', 'choroid'],
            ['melanoma'],
            ['oral', 'pharynx', 'mouth', 'tongue', 'smokeless']]


other_cancers = [['skin', 'basal cell', 'actinic keratosis', 'actinic keratoses'],
        ['head and neck', 'head & neck'], ['soft tissue', 'sarcoma'],
        ['multiple myeloma', 'plasma cell', 'myeloma'], 
        ['thyroid'],
        ['cervical', 'cervix'], 
        ['gastric', 'pyloric', 'pylori', 'stomach'], 
        ['unknown primary'], 
        ['mesothelioma'], 
        ['testicular', 'testicle'], 
        ['myeloproliferative', 'myelodysplastic', 'polycythemia', 
        'thrombocytosis', 'thrombocythemia', 'mds', 'myelodysplasia', 'myelofibrosis'],
        ['hiv', 'aids', 'human immunodeficiency virus', 'acquired immunodeficiency syndrome'], 
        ['sinonasal', 'nasopharyngeal', 'nasopharyngael'],
        ['pediatric', 'ewing', 'neuroblastoma', 'rhabdomyosarcoma', 'childhood'],
        ['retinoblastoma'],
        ['neuroendocrine', 'multiple endocrine', 'islet', 'pheochromocytoma', 'medullary thyroid'],
        ['hpv', 'papilloma', 'wart'],
        ['carcinoid'],
        ['gastrointestinal stromal', 'gist'],
        ['hodgkin disease', "hodgkin's disease"],
        ['anus', 'anal', 'anorectum']]

cancers = top_cancers + other_cancers + [['all']]
    
# Read in the rank-list which includes the organizations
RL_path = 'C:\Users\JAG\USnewsy\RL_USN.csv'
RL = pd.read_csv(RL_path, index_col=False, header=0, squeeze=True)


# Read in the dictionary
dict_path = 'C:\Users\JAG\USnewsy\CTgov_dict.csv'
ctgdict = pd.read_csv(dict_path, index_col = False, header = 0, squeeze = True)

array = []


for cancer in cancers:
        
    # Read in the clinical trials
    ctg_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTgov_pivot_' + cancer[0] + '.csv'
    ctg = pd.read_csv(ctg_path, index_col = False, header = 0, squeeze = True)

    m1 = ctgdict.merge(ctg, on = 'Institution')
    m1 = m1.groupby('Org name - Ctgov').sum()
    m1['Org name - Ctgov'] = m1.index
    m2 = RL.merge(m1, on = 'Org name - Ctgov', how = 'left')
    m2 = m2.fillna(0)    
    save_path = 'C:\Users\JAG\USN-dz\RL_USN_Ctg_' + cancer[0] + '.csv'
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
