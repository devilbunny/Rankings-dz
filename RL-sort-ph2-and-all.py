import pandas as pd
import numpy as np
from collections import Counter
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


ctg_path = 'C:\Users\JAG\USN-dz\RL_USN_Ctg_sum.csv'
ctg = pd.read_csv(ctg_path, index_col = False, header = 0)

IF_path = 'C:\Users\JAG\USN-dz\RL_dz_pm_impacts_mesh.csv'
IF = pd.read_csv(IF_path, index_col=False, header=0)

cancer_path = 'C:\Users\JAG\USN-dz\cancers_cases_keys_25.csv'
cancers = pd.read_csv(cancer_path, index_col = False, header = 0)
brief_cancers = [deet for deet in cancers['kw1']]
brief_cancers.append('all')

output_path = 'C:\Users\JAG\USN-dz\Sorted\\'

RL = pd.DataFrame({'Institution' : IF['Institution'], 'Rank' : IF['Rank-USNews'],
                    'Reputation' : IF['Reputation-USNews']})



array = [] #This will be the array of regressions
impact_array = [] # Array of impact factor vs paper count to see where I do a bad job
scores_array = []

for cancer in brief_cancers:
    RL_col =  cancer.title() + ' Score'
    ctgph2_col = 'Phase 2 ' + cancer
    ifph2_col =  'Impact factor - ' + cancer + ' Clinical Trial, Phase II'
    countph2_col = 'Paper count - ' + cancer + ' Clinical Trial, Phase II'
    ctgall_col = 'All ' + cancer
    ifall_col =  'Impact factor - ' + cancer + ' Clinical Trial'
    countall_col = 'Paper count - ' + cancer + ' Clinical Trial'
    
            
    # formula for score is  # of clinical trials over maximum number, that over 3
    # and then added to the IF divided by the maximum IF, then all x75 to give a max
    # score of 100
    RL[RL_col] = (ctg[ctgph2_col]/max(ctg[ctgph2_col]) + ctg[ctgall_col]/max(ctg[ctgall_col])
        + IF[ifph2_col]/max(IF[ifph2_col]) + IF[ifall_col]/max(IF[ifall_col]))*25
    
    
    
    specific_list = pd.DataFrame({'Institution' : RL['Institution'], RL_col : RL[RL_col]})
    specific_list[ifall_col] = IF[ifall_col]
    specific_list[ifph2_col] = IF[ifph2_col]
    specific_list[ctgall_col] = ctg[ctgall_col]
    specific_list[ctgph2_col] = ctg[ctgph2_col]
    specific_list = specific_list.sort(columns = RL_col, ascending = False)
    scores_array.append(specific_list[RL_col])
    spec_path = output_path + 'Sorted_' + cancer + '_4factor.csv'
    specific_list.to_csv(spec_path, sep = ',', index = False)
'''
    # This is to do the regressions between clinical trials and impact factor
    line = []
    line = stats.linregress(ctg[ctg_col], IF[if_col])
    array.append(line)
    
    # This does regressions between paper counts and impact factors for different dz
    line = []
    line = stats.linregress(IF[count_col], IF[if_col])
    impact_array.append(line)
'''  

RL_path = output_path + 'RL_scores_4factor.csv'
RL.to_csv(RL_path, sep = ',', index = False)

'''
Regressions = pd.DataFrame(array, index = brief_cancers, columns = ['Slope', 'Intercept', 'r_value','p_value','std_error'])
reg_path = output_path + 'CTG_PM_correlations.csv'
Regressions.to_csv(reg_path, sep = ',')

Regressions = pd.DataFrame(impact_array, index = brief_cancers, columns = ['Slope', 'Intercept', 'r_value','p_value','std_error'])
reg_path = output_path + 'Paper_count_IF_correlations.csv'
Regressions.to_csv(reg_path, sep = ',')
'''

#### Plotting the scores #####

fig = plt.figure()
plt.figure(figsize=(8,6), dpi = 300)
plt.gca().set_color_cycle(['black'])


for scores in scores_array:
    plt.plot(scores)


plt.show()
plt.savefig(output_path +'fig1_25_4factor.png', dpi = 300, figsize = (8,6))
plt.close()