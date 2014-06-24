# Runs through a list of cancers and determines the number and impact factor
# of their publications
# Impact factors from: http://www.citefactor.org/impact-factor-list-2012.html

import pandas as pd
from pubmedsearch import pubmedsearch, pmhits
from urllib2 import URLError

# Read in the list of cancers which includes the organizations
cancer_path = 'C:\Users\JAG\USN-dz\cancers_cases_keys_mesh.csv'
cancers = pd.read_csv(cancer_path, index_col=False, header=0)

# Get the rank list with list of organizations and synonyms
RL_path = 'C:\Users\JAG\USN-dz\RL_dz_pm_impacts_mesh.csv'
RL = pd.read_csv(RL_path, index_col=False, header=0)

# Read in the impact-factor list
IF_path = 'C:\Users\JAG\USnewsy\impact_factors.csv'
IF = pd.read_csv(IF_path, index_col=False, header=0)
journals = IF['Pubmed Journal Title']
factors = IF['Impact Factor']
IFdict = dict(zip(journals,factors))


# Which article types to consider
types = ['Clinical Trial', 'Clinical Trial, Phase I', 'Clinical Trial, Phase II', 'Clinical Trial, Phase III',
        'Review', 'All']

types = ['Clinical Trial, Phase I']

# get publications for each organization
def getfactors (RL, articletype, cancer, short_cancer):
    
    article_count = []
    article_factors = []
    hit_count = 0
    miss_count = 0
    bad_journals = []
    columntitlecount = 'Paper count - ' + short_cancer + ' ' + articletype
    columntitleIF = 'Impact factor - ' + short_cancer + ' ' + articletype
    
    if articletype != 'All':
        searchterm = "2008:2013 [DP] " + articletype + "[PT] "
    else:
        searchterm = "2008:2013 [DP] "

    b = 0
    while b < len(RL.Search_Term):
        org = '(' + RL.iloc[b][1] + ') '
        full_searchterm = org + searchterm + cancer
        #print full_searchterm
        try:
            cancer_count = pmhits(full_searchterm)
        except URLError:
            try:
                cancer_count = pmhits(full_searchterm)
            except URLError:
                pass
        article_count.append(cancer_count)
        #print cancer_count
        cancer_factor = 0
        
        if cancer_count > 0:
            records = pubmedsearch(full_searchterm)
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
        else:
            pass
        #print cancer_factor
        article_factors.append(cancer_factor)
        b = b + 1
    
    print sorted(list(set(bad_journals)))
    print short_cancer
    RL[columntitleIF] = article_factors
    RL[columntitlecount] = article_count
    RL.to_csv('C:\Users\JAG\USN-dz\RL_dz_pm_impacts_meshb.csv', sep = ',' , index = False)
    return RL

a = 0
while a < len(cancers.kw1) :
    # string together all the synonyms to make a single string

    shortkey = cancers['kw1'][a]
    keys = cancers['mesh'][a]

    for PT in types:
        RL = getfactors(RL, PT, keys, shortkey)
        
    a = a + 1

RL.to_csv('C:\Users\JAG\USN-dz\RL_dz_pm_impacts_meshc.csv', sep = ',' , index = False)