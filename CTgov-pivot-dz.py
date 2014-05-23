# Pivots the table of trials from clinical trials.gov and then pivots it to
# collect in

import pandas as pd


# Read in the lists of trials

ctg_path = 'C:\Users\JAG\USnewsy\Clinicaltrials\CTgovDz_'

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

for cancer in cancers:
    path = ctg_path + cancer[0] + '_b.csv'
    ctg = pd.read_csv(path, index_col = False, header = 0, squeeze = True)
    #get start years as numbers and then select on them
    Start_years = []
    for deet in ctg['Start_date']:
        deet = deet[-4:]
        try:
            deet = int(deet)
            Start_years.append(deet)
        except ValueError:
            Start_years.append(0)
    ctg['Start year'] = Start_years
    ctg = ctg[ctg['Start year'] > 2007]
    ctg = ctg[ctg['Start year'] < 2014]
    ctg = ctg.drop('Start year', axis = 1)
    
    # make the pivot table - count the number of trials in each phase
    pivot = ctg.pivot_table('nct_id', rows ='Institution', cols ='Phase', aggfunc = 'count')
    pivot['Institution'] = pivot.index
    pivot = pivot.fillna(0)

   
    #clean up phases
    try:
        pivot['N/A'] = pivot['N/A'] + pivot['Phase 4']
        pivot = pivot.drop('Phase 4', axis = 1)
    except KeyError:
        pass
    try:
        pivot['N/A'] = pivot['N/A'] + pivot['Phase 0']
        pivot = pivot.drop('Phase 0', axis = 1)
    except KeyError:
        pass
    try:
        pivot['Phase 1'] = pivot['Phase 1'] + pivot['Phase 1/Phase 2']
        pivot = pivot.drop('Phase 1/Phase 2', axis = 1)
    except KeyError:
        pass
    try:
        pivot['Phase 2'] = pivot['Phase 2/Phase 3'] + pivot['Phase 2']
        pivot = pivot.drop('Phase 2/Phase 3', axis = 1)
    except KeyError:
        pass
    try:
        pivot['All'] = pivot['N/A'] + pivot['Phase 1'] + pivot['Phase 2'] + pivot['Phase 3']
    except KeyError:
        pass

    #Rename columns so they include the cancer
    pivot['N/A ' + cancer[0]] = pivot['N/A']
    pivot = pivot.drop('N/A', axis = 1)

    pivot['Phase 1 ' + cancer[0]] = pivot['Phase 1']
    pivot = pivot.drop('Phase 1', axis = 1)
    
    pivot['Phase 2 ' + cancer[0]] = pivot['Phase 2']
    pivot = pivot.drop('Phase 2', axis = 1)
    
    try:
        pivot['Phase 3 ' + cancer[0]] = pivot['Phase 3']
        pivot = pivot.drop('Phase 3', axis = 1)
    except KeyError:
        pass

    try:
        pivot['All ' + cancer[0]] = pivot['All']
        pivot = pivot.drop('All', axis = 1)
    except KeyError:
        pass

    path = 'C:\Users\JAG\USnewsy\Clinicaltrials\CTgov_pivot_' + cancer[0] + '_b.csv'
    pivot.to_csv(path, sep = ',', index = False)

