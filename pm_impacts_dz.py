''' Deprecated - use pm_counts - even for impact factors '''






# Runs through a list of cancers and determines the number and impact factor
# of their publications
# Impact factors from: http://www.citefactor.org/impact-factor-list-2012.html

import pandas as pd
from pubmedsearch import pubmedsearch, pmhits

# Read in the list of cancers which includes the organizations
cancer_path = 'C:\Users\JAG\USN-dz\cancers_cases_keys.csv'
cancers = pd.read_csv(cancer_path, index_col=False, header=0)

# Get the rank list with list of organizations and synonyms
RL_path = 'C:\Users\JAG\USN-dz\RL_USN.csv'
RL = pd.read_csv(RL_path, index_col=False, header=0)

# Read in the impact-factor list
IF_path = 'C:\Users\JAG\USnewsy\impact_factors.csv'
IF = pd.read_csv(IF_path, index_col=False, header=0)
journals = IF['Pubmed Journal Title']
factors = IF['Impact Factor']
IFdict = dict(zip(journals,factors))

print 'a'

# Which article types to consider
types = ['Clinical Trial', 'Clinical Trial, Phase I', 'Clinical Trial, Phase II', 'Clinical Trial, Phase III',
        'Review', 'All']

types = ['Clinical Trial, Phase I', 'Clinical Trial, Phase II', 'Clinical Trial, Phase III']

print types

# get publications for each organization
def getfactors (cancers, articletype, org = None, orgshort = None):
    IFs = []
    article_count = []
    bad_journals = []
    hit_count = 0
    miss_count = 0
    columntitleIF = 'Impact factor - ' + articletype + orgshort
    columntitlecount = 'Paper count - ' + articletype + orgshort
    
    if articletype != 'All':
        searchterm = "2008:2013 [DP] " + articletype + "[PT] "

    else:
        searchterm = "2008:2013 [DP] "

    a = 0
    while a < len(cancers.kw1) :
        cancer_factor = 0
        cancer_count = 0
        
        # string together all the synonyms to make a single string
        keywords = cancers.iloc[a][2:9]
        keys = ""
        for keyword in keywords:

            if str(keyword) == 'nan':
                pass
            else:
                keys = keys + keyword + '[TIAB] OR '
                if keyword[-6:] == 'cancer':
                    keys = keys + keyword[:-6] + 'carcinoma[TIAB] OR '
                
        keys = keys[:-3]
        full_searchterm = org + searchterm + keys
        print full_searchterm

        records = pubmedsearch(full_searchterm)
        for record in records: #iterating over the records collected, get the journal for each and impact factor
            cancer_count = cancer_count + 1
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
        IFs.append(cancer_factor)
        article_count.append(cancer_count)
        print cancer_factor
        print cancer_count
        a = a + 1

    #bad_journals = sorted(list(set(bad_journals)))
    cancers[columntitleIF] = IFs
    cancers[columntitlecount] = article_count



    return cancers
b = 0
print b
while b < len(RL.Search_Term):
    org = RL.iloc[b][1] + '[AD] '
    print org
    orgshort = ' ' + RL.iloc[b][5]
    print orgshort
    for PT in types:
        cancers = getfactors(cancers, PT, org = org, orgshort = orgshort)
        cancers.to_csv('C:\Users\JAG\USN-dz\Cancers_Impacts_Orgb.csv', sep = ',' , index = False)
    b = b + 1

cancers.to_csv('C:\Users\JAG\USN-dz\Cancers_Impacts_Orgb.csv', sep = ',' , index = False)