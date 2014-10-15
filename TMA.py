import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


pten1_path = 'C:\Users\JAG\MAGI_TMA\PTEN_TMA1.csv'
pten1 = pd.read_csv(pten1_path, index_col = False, header = 0)
pten2_path = 'C:\Users\JAG\MAGI_TMA\PTEN_TMA2.csv'
pten2 = pd.read_csv(pten2_path, index_col = False, header = 0)
pten3_path = 'C:\Users\JAG\MAGI_TMA\PTEN_TMA3.csv'
pten3 = pd.read_csv(pten3_path, index_col = False, header = 0)



cols = ['SP#', 'Lesion', 'ANALYZED_AREA', 'Area_Color1', 'Area_Color2', 
'Mean_Intensity_Color1', 'Mean_Intensity_Color2']

array = []
for col in cols:
    newcol = pten1[col].append(pten2[col]).append(pten3[col])
    array.append(newcol)

pten = pd.DataFrame({cols[0] : array[0], cols[1] : array[1], cols[2] : array[2], 
    cols[3] : array[3], cols[4] : array[4], cols[5] : array[5], cols[6] : array[6]})

lez = []
for lesion in pten['Lesion']:
    lesion = lesion.strip()
    lesion = lesion.replace('  ', ' ')
    lesion = lesion.upper()
    lesion = lesion.replace('GLEASON ', 'G')
    lesion = lesion.replace('TREATMENT', 'TX')
    lez.append(lesion)
pten['Lesion'] = lez

sps = []
for sp in pten['SP#']:
    sp = sp.upper()
    if sp[0] == 'U':
        pass
    elif sp[0] != 'S':
        sp = 'S'+sp
    else:
        pass
    sps.append(sp)
pten['SP#'] = sps
    
    

pten['Stain_Area1'] = pten['Area_Color1'] / pten['ANALYZED_AREA'] * 100
pten['Stain_Area2'] = pten['Area_Color2'] / pten['ANALYZED_AREA'] * 100
pten['Total_Area'] = pten['Stain_Area1'] + pten['Stain_Area2']

pten['Intensity_Area1'] = pten['Stain_Area1'] * pten['Mean_Intensity_Color1']
pten['Intensity_Area2'] = pten['Stain_Area2'] * pten['Mean_Intensity_Color2']
pten['Total_Stain'] = pten['Intensity_Area1'] + pten['Intensity_Area2']

pten_area = pd.pivot_table(pten, values = 'Total_Area', rows = 'SP#', cols = 'Lesion', aggfunc = 'mean')
path = 'C:\Users\JAG\MAGI_TMA\PTEN_area.csv'
pten_area.to_csv(path, sep = ',')

pten_stain = pd.pivot_table(pten, values = 'Total_Stain', rows = 'SP#', cols = 'Lesion', aggfunc = 'mean')
path = 'C:\Users\JAG\MAGI_TMA\PTEN_stain.csv'
pten_stain.to_csv(path, sep = ',')



#
# Dealing with MAGI
#
#
magi1_path = 'C:\Users\JAG\MAGI_TMA\MAGI_TMA1.csv'
magi1 = pd.read_csv(magi1_path, index_col = False, header = 0)
magi2_path = 'C:\Users\JAG\MAGI_TMA\MAGI_TMA2.csv'
magi2 = pd.read_csv(magi2_path, index_col = False, header = 0)
magi3_path = 'C:\Users\JAG\MAGI_TMA\MAGI_TMA3.csv'
magi3 = pd.read_csv(magi3_path, index_col = False, header = 0)



cols = ['SP#', 'Lesion', 'ANALYZED_AREA', 'Area_Color1', 'Area_Color2', 
'Mean_Intensity_Color1', 'Mean_Intensity_Color2']

array = []
for col in cols:
    newcol = magi1[col].append(magi2[col]).append(magi3[col])
    array.append(newcol)

magi = pd.DataFrame({cols[0] : array[0], cols[1] : array[1], cols[2] : array[2], 
    cols[3] : array[3], cols[4] : array[4], cols[5] : array[5], cols[6] : array[6]})

lez = []
for lesion in magi['Lesion']:
    lesion = lesion.strip()
    lesion = lesion.replace('  ', ' ')
    lesion = lesion.upper()
    lesion = lesion.replace('GLEASON ', 'G')
    lesion = lesion.replace('TREATMENT', 'TX')
    lez.append(lesion)
magi['Lesion'] = lez

sps = []
for sp in magi['SP#']:
    sp = sp.upper()
    if sp[0] == 'U':
        pass
    elif sp[0] != 'S':
        sp = 'S'+sp
    else:
        pass
    sps.append(sp)
magi['SP#'] = sps
    

magi['Stain_Area1'] = magi['Area_Color1'] / magi['ANALYZED_AREA'] * 100
magi['Stain_Area2'] = magi['Area_Color2'] / magi['ANALYZED_AREA'] * 100
magi['Total_Area'] = magi['Stain_Area1'] + magi['Stain_Area2']

magi['Intensity_Area1'] = magi['Stain_Area1'] * magi['Mean_Intensity_Color1']
magi['Intensity_Area2'] =magi['Stain_Area2'] * magi['Mean_Intensity_Color2']
magi['Total_Stain'] = magi['Intensity_Area1'] + magi['Intensity_Area2']

magi_area = pd.pivot_table(magi, values = 'Total_Area', rows = 'SP#', cols = 'Lesion', aggfunc = 'mean')
path = 'C:\Users\JAG\MAGI_TMA\MAGI_area.csv'
magi_area.to_csv(path, sep = ',')

magi_stain = pd.pivot_table(magi, values = 'Total_Stain', rows = 'SP#', cols = 'Lesion', aggfunc = 'mean')
path = 'C:\Users\JAG\MAGI_TMA\MAGI_stain.csv'
magi_stain.to_csv(path, sep = ',')

merge_area = pten_area.join(magi_area, how = 'outer', lsuffix = '_PTEN', rsuffix = '_MAGI')
path = 'C:\Users\JAG\MAGI_TMA\merge_area.csv'
merge_area.to_csv(path, sep = ',')

merge_stain = pten_stain.join(magi_stain, how = 'outer', lsuffix = '_PTEN', rsuffix = '_MAGI')
path = 'C:\Users\JAG\MAGI_TMA\merge_stain.csv'
merge_stain.to_csv(path, sep = ',')

Array = ['NL','BPH','HGPIN','G3','G4','G5']
data = []
means = []
stdev = []
stderr = []
for column in Array:
    plt.close()
    plt.scatter(pten_stain[column],magi_stain[column])
    plt.xlabel('PTEN total stain, ODS * %')
    plt.ylabel('MAGI2 total stain, ODS * %')
    plt.savefig('C:\Users\JAG\MAGI_TMA\correlate' + column + '_stain.png')
    means.append(np.mean(magi_area[column]))
    deet = magi_area[column]
    deet = deet.dropna()
    stdev.append(np.std(deet))
    stderr.append(stats.sem(deet))
    data.append(deet)
    #print stats.skewtest(deet)
    #print stats.kurtosistest(deet)




plt.close()
N = 6
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, means, width, color='k', yerr=stderr)


plt.ylabel('Magi area, % total (+/- Standard deviation)')
plt.title('Total Magi area')
plt.xticks(ind+width/2, ('Normal', 'BPH', 'HGPIN', 'Gleason 3', 'Gleason 4', 'Gleason 5') )
plt.yticks(np.arange(0,31,5))
plt.ylim(0,30) 

plt.show()
plt.savefig('C:\Users\JAG\MAGI_TMA\Magi_area_sem.png')


# fixed the boxplot
plt.close()
p1 = plt.boxplot(data)
plt.savefig('C:\Users\JAG\MAGI_TMA\\boxplot.png')
plt.close()


#lets do some sensitivity / specificity calcs
def sensitivity(cancers, threshold):
   #cancers array of numbers, # threshold - suggested threhold
    hits = cancers[cancers > threshold]
    sens = float(len(hits)) / float(len(cancers))
    return sens

def specificity(normals, threshold):
    true_negatives = normals[normals < threshold]
    spec = float(len(true_negatives))/ float(len(normals))
    return spec

threshold = np.arange(0,7000,35)
normals = magi_stain['NL'].append(magi_stain['BPH'])
normals = normals.dropna()
cancer = magi_stain['G3'].append(magi_stain['G4'])
cancer = cancer.append(magi_stain['G5'])
cancer = cancer.dropna()

sensitivities = []
specificities = []
minus_spec = []
for level in threshold:
    sens = sensitivity(cancer, level)
    spec = specificity(normals, level)
    sensitivities.append(sens)
    specificities.append(spec)
    minus_spec.append(1-spec)

plt.close()
plt.scatter(minus_spec, sensitivities)
plt.xlabel('1 minus specificity')
plt.ylabel('Specificity')
plt.savefig('C:\Users\JAG\MAGI_TMA\ROC_stain.png')

# Lets sum up the AUC
a = 0
auc = 0
while a < 198:
    newarea = sensitivities[a] * (minus_spec[a] - minus_spec[a+1])
    auc = auc + newarea
    a = a + 1
print 'AUC: ' + str(auc)


from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats.mstats import kruskalwallis, friedmanchisquare

Array = ['NL','BPH','HGPIN','G3','G4','G5']
multiarea = magi_area['NL'].append(magi_area['BPH'])
multiarea = multiarea.append(magi_area['HGPIN'])
multiarea = multiarea.append(magi_area['G3'])
multiarea = multiarea.append(magi_area['G4'])
multiarea = multiarea.append(magi_area['G5'])
multiarea = multiarea.dropna()
multilesion = list()
a = 0
while a < 6:
    column = Array[a]
    coldata = magi_area[column]
    coldata = coldata.dropna()
    for deet in coldata:
        multilesion.append(a)
    a = a + 1

print pairwise_tukeyhsd(multiarea, multilesion) 
print kruskalwallis(magi_area['NL'].dropna(), magi_area['BPH'].dropna(), magi_area['HGPIN'].dropna(),
    magi_area['G3'].dropna(), magi_area['G4'].dropna(), magi_area['G5'].dropna())

print kruskalwallis(magi_stain['NL'].dropna(), magi_stain['BPH'].dropna(), magi_stain['HGPIN'].dropna(),
    magi_stain['G3'].dropna(), magi_stain['G4'].dropna(), magi_stain['G5'].dropna())

