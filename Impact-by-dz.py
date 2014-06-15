# Runs through a list of cancers and determines the number and impact factor
# of their publications
# Impact factors from: http://www.citefactor.org/impact-factor-list-2012.html

import pandas as pd
from pubmedsearch import pubmedsearch, pmhits
from urllib2 import URLError

# Read in the list of cancers which includes the organizations
cancer_path = 'C:\Users\JAG\USN-dz\cancers_cases_keys_mesh.csv'
cancers = pd.read_csv(cancer_path, index_col=False, header=0)


# Read in the impact-factor list
IF_path = 'C:\Users\JAG\USnewsy\impact_factors.csv'
IF = pd.read_csv(IF_path, index_col=False, header=0)
journals = IF['Pubmed Journal Title']
factors = IF['Impact Factor']
IFdict = dict(zip(journals,factors))


# Which article types to consider
types = ['Clinical Trial', 'Clinical Trial, Phase I', 'Clinical Trial, Phase II', 'Clinical Trial, Phase III',
        'Review', 'All']

types = ['Clinical Trial, Phase I', 'Clinical Trial, Phase II', 'Clinical Trial, Phase III']

# get publications for each organization
def getfactors (articletype, cancer, short_cancer):

    hit_count = 0
    miss_count = 0
    bad_journals = []
    
    if articletype != 'All':
        searchterm = "2008:2013 [DP] " + articletype + "[PT] "
    else:
        searchterm = "2008:2013 [DP] "


    full_searchterm = searchterm + cancer

    print full_searchterm
    try:
        cancer_count = pmhits(full_searchterm)
    except URLError:
        try:
            cancer_count = pmhits(full_searchterm)
        except URLError:
            pass
    
    records = pubmedsearch(full_searchterm, MAX_COUNT = 100000)
    cancer_factor = 0
    
    for record in records: #iterating over the records collected, get the journal for each and impact factor
        TA = record.get('TA', '?')
        TA = TA.upper()
        TA = TA.replace('.', '')
        factor = IFdict.get(TA)
        try:
            factor = float(factor)
            cancer_factor = cancer_factor + factor #add this IF to the total IF for the organization
            hit_count = hit_count + 1
        except TypeError:
            bad_journals.append(TA)
            miss_count = miss_count + 1

    print articletype
    bad_journals = list(set(bad_journals))
    print bad_journals
    return (cancer_count,cancer_factor)


    

for PT in types:
    a = 0
    counts = []
    impacts = []
    
    while a < len(cancers.kw1) :
        # string together all the synonyms to make a single string
        shortkey = cancers['kw1'][a]
        keys = cancers['mesh'][a]
        (count,impact) = getfactors(PT, keys, shortkey)
        counts.append(count)
        impacts.append(impact)
        a = a + 1
    count_title = 'Publications - ' + PT
    cancers[count_title] = counts
    impact_title = 'Impacts - ' + PT
    cancers[impact_title] = impacts
    cancers.to_csv('C:\Users\JAG\USN-dz\Impact_by_dz.csv', sep = ',' , index = False)
    
cancers.to_csv('C:\Users\JAG\USN-dz\Impact_by_dz.csv', sep = ',' , index = False)