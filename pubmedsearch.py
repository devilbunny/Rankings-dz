#!/usr/bin/env python
# Copied from ehazlett with modifications
# numpy and biopython are required -- pip install numpy biopython

 
from Bio import Entrez
from Bio import Medline

 


def pubmedsearch (TERM, MAX_COUNT = 10000):
    # Returns an Entrez object matching *TERM*
    Entrez.email = 'jagstein@uchicago.edu'
    Entrez.tool = 'pm_impacts'
    h = Entrez.esearch(db='pubmed', retmax=MAX_COUNT, term=TERM)
    result = Entrez.read(h)
    ids = result['IdList']
    h = Entrez.efetch(db='pubmed', id=ids, rettype='medline', retmode='text') 
    records = Medline.parse(h)
    return records

def pmhits (TERM):
    # Returns the number of hits returned by searching pubmed for *TERM*
    Entrez.email = 'jagstein@uchicago.edu'
    Entrez.tool = 'pm_impacts'
    h = Entrez.esearch(db='pubmed', retmax=1000000, term=TERM)
    result = Entrez.read(h)
    return result['Count']

