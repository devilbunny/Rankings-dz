# Generates plots
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


Data_Path = "C:\Users\JAG\USN-dz\Helpme.csv"
Figure_path = 'C:\Users\JAG\USN-dz\\'

Data =  pd.read_csv(Data_Path, sep=',' , index_col = False, header =0)

fig = plt.figure()
plt.figure(figsize=(12,3), dpi = 300)

plt.scatter(Data['death'], Data['phase1totalpts'], s = 15, c = 'b', marker = 'o', linewidth = 0.2)
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
plt.savefig(Figure_path +'fig1_25.png', dpi = 300, figsize = (8,6))




'''
# This is for the perimatch scatter plots
fig = plt.figure()
plt.scatter((RWG_fix.Prematch + RWG_fix.Perimatch), RWG_fix.TOTAL_COST)
plt.savefig(Figure_path + 'preperimatch_vs_grantmoney_scatter.png')
plt.close()

fig = plt.figure()
plt.scatter((RWG_fix.Prematch), RWG_fix.TOTAL_COST)
plt.savefig(Figure_path + 'prematch_vs_grantmoney_scatter.png')
plt.close()

fig = plt.figure()
plt.scatter((RWG_fix.Perimatch), RWG_fix.TOTAL_COST)
plt.savefig(Figure_path + 'perimatch_vs_grantmoney_scatter.png')
plt.close()

fig = plt.figure()
plt.scatter((RWG_fix.Postmatch), RWG_fix.TOTAL_COST)
plt.savefig(Figure_path + 'postmatch_vs_grantmoney_scatter.png')
plt.close()

fig = plt.figure()
plt.scatter((RWG_fix.Prematch + RWG_fix.Perimatch), RWG_fix.Postmatch)
plt.savefig(Figure_path + 'pre_vs_postmatch_scatter.png')
plt.close()

# This is to make a scatter of preperi vs post overacheivers
RWG_fix['Preperi_wt'] = RWG_fix['Preperi'] / np.average(RWG_fix['Preperi'])
print RWG_fix['Preperi_wt']
RWG_fix['Postmatch_wt'] = RWG_fix['Postmatch'] / np.average(RWG_fix['Postmatch'])
RWG_grant = RWG_fix[RWG_fix['Any_grant'] == True]
RWG_nogrant = RWG_fix[RWG_fix['Any_grant'] == False]


fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.scatter(RWG_grant['Preperi_wt'], RWG_grant['Postmatch_wt'], s=20, c='r', marker="o")
ax2.scatter(RWG_nogrant['Preperi_wt'], RWG_nogrant['Postmatch_wt'], s=20, c='b', marker="o")
plt.show()
plt.savefig(Figure_path + 'Weighted_scatter_b.png')
plt.close()
'''
