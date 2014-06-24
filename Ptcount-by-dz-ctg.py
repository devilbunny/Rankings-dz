# Pivots the table of trials from clinical trials.gov and then pivots it to
# collect the number of patients per trial phase and diagnosis

import pandas as pd
import numpy as np


# Read in the lists of trials
ctg_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\Screening\CTgovDz_vp_all.csv'
ctg = pd.read_csv(ctg_path, index_col = False, header = 0, squeeze = True)

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


   
# make the pivot table - count the number of trials in each phase
pivot = ctg.pivot_table('nct_id', rows = 'Disease', cols = ['Phase', 'Status'], aggfunc = 'count')
pivot['Disease'] = pivot.index
pivot = pivot.fillna(0)

#path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTpt_by_dz_phase.csv'
#pivot.to_csv(path, sep = ',')


pivot = ctg.pivot_table('nct_id', rows = 'Disease', cols = 'Phase', aggfunc = 'count')
pivot['Disease'] = pivot.index
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


path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CT_trials_by_dz_screen.csv'
pivot.to_csv(path, sep = ',')