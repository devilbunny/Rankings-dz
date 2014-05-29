# Pivots the table of trials from clinical trials.gov and then pivots it to
# collect in

import pandas as pd


# Read in the lists of trials

ctg_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTgovDz_'
output_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTgov_pivot_' 

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

for cancer in cancers:
    path = ctg_path + cancer[0] + '.csv'
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

    path = output_path + cancer[0] + '.csv'
    pivot.to_csv(path, sep = ',', index = False)

