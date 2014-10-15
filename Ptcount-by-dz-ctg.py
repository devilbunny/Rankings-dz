# Pivots the table of trials from clinical trials.gov and then pivots it to
# collect the number of patients per trial phase and diagnosis

import pandas as pd
import numpy as np


# Read in the lists of trials
ctg_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\Revised\CTgovDz_vp_all.csv'
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

Phase = []
for deet in ctg['Phase']:
    if (deet == 'Phase 1' or deet == 'Phase 2' or deet == 'Phase 3'):
        pass
    elif deet == 'Phase 1/Phase 2':
        deet = 'Phase 1'
    elif deet == 'Phase 2/Phase 3':
        deet = 'Phase 2'
    else:
        deet = 'N/A'
    
    Phase.append(deet)


ctg['Phase'] = Phase


   
# make the pivot table - count the number of trials in each phase
pivot = ctg.pivot_table('Enrollment', rows = 'Disease', cols = ['Phase', 'Status'], aggfunc = 'sum')
pivot['Disease'] = pivot.index
pivot = pivot.fillna(0)

#path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTpt_by_dz_phase.csv'
#pivot.to_csv(path, sep = ',')


pivot = ctg.pivot_table('Enrollment', rows = 'Disease', cols = 'Phase', aggfunc = 'median')
pivot['Disease'] = pivot.index
pivot = pivot.fillna(0)

ctg['All'] = 'All'
pivot2 = ctg.pivot_table('Enrollment', rows = 'Disease', cols = 'All', aggfunc = 'median')
pivot2['Disease'] = pivot2.index
pivot2 = pivot2.fillna(0)

pivot = pivot.merge(pivot2)



path = 'C:\Users\JAG\USN-dz\Clinicaltrials\Revised\CT_median_pt_by_dz.csv'
pivot.to_csv(path, sep = ',')