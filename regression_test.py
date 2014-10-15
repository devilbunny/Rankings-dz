# Looks at different predictors to see what is best at getting reputation
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


Data_Path = "C:\Users\JAG\USN-dz\RL_reputation_guess.csv"
output_path = 'C:\Users\JAG\USN-dz\Reputation_guess_'

Data =  pd.read_csv(Data_Path, sep=',' , index_col = False, header =0)
Data['IF_Trial2'] = Data['IF_Ph2'] + Data['Trials_Ph2']
Data['IF_Trial_All'] = Data['IF_all'] + Data['Trials_all']
Data['IFx2_Trialsx2'] = Data['IF_Trial2'] + Data['IF_Trial_All']

line = []
array = []
guesses = []
for col in Data.columns[1:]:
    line = stats.linregress(Data[col], Data['Reputation-USNews'])
    array.append(line) # run the regressions

    reputations = [] # What values do we estimate with our regressions
    for deet in Data[col]:
        guess = line[0] * deet + line[1]
        reputations.append(guess)
    guesses.append(reputations)


        
    '''
    #Let's graph those!
    fig = plt.figure()
    plt.figure(figsize=(9,6), dpi = 300)
    plt.scatter(reputations, Data['Reputation-USNews'], s = 15, c = 'r', marker = 'o', linewidths = 0.2)
    plt.scatter(np.arange(0,80,0.1), np.arange(0,80,0.1), s = 2, c = 'k', marker = '.')
    plt.savefig(output_path + col + '_line.png', dpi = 300, figsize = (9,6))
    plt.close()
    '''


Regressions = pd.DataFrame(array, index = Data.columns[1:], columns = ['Slope', 'Intercept', 'r_value','p_value','std_error'])
reg_path = output_path + 'regressions.csv'
Regressions.to_csv(reg_path, sep = ',')

Guesses = pd.DataFrame(np.transpose(guesses), index = Data['Org name - Ctgov'], columns = Data.columns[1:])
guess_path = output_path + 'guesses.csv'
Guesses.to_csv(guess_path, sep = ',')




# Create plots with pre-defined labels.
plt.close()
plt.scatter(Guesses['Reputation-USNews'], ((Guesses['IF_Ph2']-Guesses['Reputation-USNews'])/Guesses['Reputation-USNews']), color = 'b', label='Phase 2 Impact Factopr')
plt.scatter(Guesses['Reputation-USNews'], ((Guesses['Trials_Ph2']-Guesses['Reputation-USNews'])/Guesses['Reputation-USNews']), color = 'g', label='Phase 2 Trials')
plt.scatter(Guesses['Reputation-USNews'], ((Guesses['IF_Trial2']-Guesses['Reputation-USNews'])/Guesses['Reputation-USNews']), color = 'r', label='Combined')
#plt.scatter(Guesses['Reputation-USNews'], ((Guesses['IF_all']-Guesses['Reputation-USNews'])/Guesses['Reputation-USNews']), color = 'w', edgecolor = 'k', label='All Impact Factors', linewidths = 0.5)
plt.plot(np.arange(0,75,0.1),np.zeros(750), 'k-', label = 'Actual reputation')
legend = plt.legend(loc='upper right')
plt.savefig(output_path + 'Combine-IF-Paper2_adjust.png', dpi = 300, figsize = (9,6))
   

'''
plt.scatter(Data['death'], Data['phase2totalpts'], s = 15, c = 'g', marker = 'd', linewidth = 0.2)
plt.scatter(Data['death'], Data['phase3totalpts'], s = 15, c = 'r', marker = 's', linewidth = 0.2)


plt.xscale('log', basex = 10, subsx = [])
plt.yscale('log', basey = 10, subsy = [])
plt.xlim(1000, 200000)
plt.ylim(1000, 200000)
plt.xticks([750,1000,10000,50000,159260], [750,1000,10000,50000,159260], size = 6)
plt.yticks([300,1000,10000,50000,159260], [300,1000,10000,50000,164971], size = 6)
plt.xlabel('Deaths', size = 6)
plt.ylabel('Clinical Trial Patients', size = 6)

death = Data['death']
ph1 = Data['phase1totalpts']
ph3 = Data['phase3totalpts']
labels = Data['disease']

i=0
while i < len(death):
    plt.annotate(labels[i], xy = (death[i],ph3[i]), xytext = (death[i]*0.99,(175000 - (175000 - ph3[i]*1.5))), size = 4, rotation = 90) 
    i = i + 1
    
#plt.show()
plt.savefig(Figure_path +'lines.png', dpi = 300, figsize = (8,6))
'''

