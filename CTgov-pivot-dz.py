# Pivots the table of trials from clinical trials.gov and then pivots it to
# collect in

import pandas as pd


# Read in the lists of trials

ctg_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTgovDz_vp_'
output_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTgov_pivot_vp_' 

cancer_path = 'C:\Users\JAG\USN-dz\cancers_cases_keys.csv'
cancers = pd.read_csv(cancer_path, index_col=False, header=0)

brief_cancers = [deet for deet in cancers['kw1']]
brief_cancers.append('all')



for cancer in brief_cancers:
    path = ctg_path + cancer + '.csv'
    ctg = pd.read_csv(path, index_col = False, header = 0)
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

    Enrollment = []
    for deet in ctg['Enrollment']:
        try:
            deet = int(deet)
            Enrollment.append(deet)
        except ValueError:
            Enrollment.append(0)
    ctg['Enrollment'] = Enrollment
    ctg = ctg[ctg['Enrollment'] < 200000]    
    
    print ctg
    # make the pivot table - count the number of trials in each phase
    try:
        pivot = pd.pivot_table(ctg, values = 'nct_id', rows = 'Institution', cols = 'Phase', aggfunc = 'count')
        pivot['Institution'] = pivot.index
        pivot = pivot.fillna(0)
    except KeyError:
        pass

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
    try:
        pivot['N/A ' + cancer] = pivot['N/A']
        pivot = pivot.drop('N/A', axis = 1)
    except KeyError:
        pass

    try:
        pivot['Phase 1 ' + cancer] = pivot['Phase 1']
        pivot = pivot.drop('Phase 1', axis = 1)
    except KeyError:
        pass
        
    try:
        pivot['Phase 2 ' + cancer] = pivot['Phase 2']
        pivot = pivot.drop('Phase 2', axis = 1)
    except KeyError:
        pass
        
    try:
        pivot['Phase 3 ' + cancer] = pivot['Phase 3']
        pivot = pivot.drop('Phase 3', axis = 1)
    except KeyError:
        pass

    try:
        pivot['All ' + cancer] = pivot['All']
        pivot = pivot.drop('All', axis = 1)
    except KeyError:
        pass

    path = output_path + cancer + '.csv'
    pivot.to_csv(path, sep = ',', index = False)

