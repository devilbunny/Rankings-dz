# Runs through a list of cancers and determines the number and impact factor
# of their publications
# Impact factors from: http://www.citefactor.org/impact-factor-list-2012.html

import pandas as pd
from pubmedsearch import pubmedsearch, pmhits
from urllib2 import URLError

# Read in the list of cancers which includes the organizations
cancer_path = 'C:\Users\JAG\USN-dz\cancers_cases_keys.csv'
cancers = pd.read_csv(cancer_path, index_col=False, header=0)

# Get the rank list with list of organizations and synonyms
RL_path = 'C:\Users\JAG\USnewsy\RL_USN.csv'
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

types = ['Clinical Trial, Phase I', 'Clinical Trial, Phase II', 'Clinical Trial, Phase III']

# get publications for each organization
def getfactors (cancers, articletype, org = None, orgshort = None):
    
    article_count = []
    columntitlecount = 'Paper count - ' + articletype + orgshort
    
    if articletype != 'All':
        searchterm = "2008:2013 [DP] " + articletype + "[PT] "
    else:
        searchterm = "2008:2013 [DP] "

    
    a = 0
    while a < len(cancers.kw1) :
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
                
        keys = keys[:-4]
        keys = '(' + keys + ') '
        full_searchterm = org + searchterm + keys
        print full_searchterm

        try:
            cancer_count = pmhits(full_searchterm)
        except URLError:
            try:
                cancer_count = pmhits(full_searchterm)
            except URLError:
                pass
        article_count.append(cancer_count)
        print cancer_count
        a = a + 1

    cancers[columntitlecount] = article_count
    cancers.to_csv('C:\Users\JAG\USN-dz\Cancers_counts_orgs.csv', sep = ',' , index = False)
    return cancers


b = 0
while b < len(RL.Search_Term):
    org = '(' + RL.iloc[b][1] + '[AD]) '
    orgshort = ' ' + RL.iloc[b][5]
    print orgshort
    print org
    for PT in types:
        cancers = getfactors(cancers, PT, org = org, orgshort = orgshort)
    b = b + 1

cancers.to_csv('C:\Users\JAG\USN-dz\Cancers_counts_orgs.csv', sep = ',' , index = False)