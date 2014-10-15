import xml.etree.ElementTree as etree
import pandas as pd
import numpy as np
import os
import re

input_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\\'
output_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\Revised\CTgovDz_vp_'
attributes = ['id_info/nct_id', 'brief_title', 'source', 'start_date', 
            'completion_date', 'phase', 'enrollment', 'overall_status',
            'sponsors/lead_sponsor/agency']


cancer_path = 'C:\Users\JAG\USN-dz\cancers_cases_keys_lymphofix.csv'
cancers = pd.read_csv(cancer_path, index_col=False, header=0)


def parse_ctgov (path, attributes):
    ''' *path* of XML file, *array* of attributes - parses a file from 
    clinicaltrials.gov and extracts the attributes'''
    tree = etree.parse(path)
    root = tree.getroot()
    values = []
    for attribute in attributes:
        try:
            deet = root.find(attribute).text
            values.append(deet)
        except AttributeError:
            values.append('Not found')
    return values


def parseall_ctgov (path, attributes):
    ''' *path* of XML file, *array* of attributes - parses a file from 
    clinicaltrials.gov and extracts the attributes'''
    tree = etree.parse(path)
    root = tree.getroot()
    values = []
    for attribute in attributes:
        atts = []
        try:
            deets = root.findall(attribute)
            for deet in deets:
                atts.append(deet.text)
        except AttributeError:
            atts.append('Not found')
        values.append(atts)
    return values

def salvagedz(keywords, cancers):
    # Uses regular expressions to identify diseases in otherwise failed matches
    # the regular expressions are of the format tissue.{1,100} cancer, where tissue
    # is the tissue type, '.' means 'any character', {1,100} means up to 100 of 'any character'
    # and cancer is usually 'cancer' but is 'leukemia' or 'lymphoma' as appropriate
    dz = []
    a = 0
    while a < len(cancers['re']):
        match = re.findall(cancers['re'][a], keywords, re.DOTALL)
        if len(match) > 0:
            dz.append(cancers['kw1'][a])
        a = a + 1
    return dz

def fix_lymphoma(keywords): 
    # takes a data string pruportedly pointing to hodking dz or NHL and disambiguates
    hl =  'non-hodgkin lymphoma'
    hodgkin_keys = ['hodgkin','nodular sclerosing', 'reed sternberg',' nodular lymphocyte',
                    'lymphocyte depleted', 'lymphocyte depletion']
    
    non_hodgkin_keys = ['diffuse small lymphoid', 'cleaved cell', 'diffuse large b cell',
                    'lymphocytic histiocytic', 'mixed lymphoma', 'pleomorphic lymphoma',
                    'mantle cell lymphoma', 'burkitt', 'mononucleosis', 
                    'hiv related lymphoma', 'aids related lymphoma', 'primary cns lymphoma']
    
    for key in hodgkin_keys:
        if keywords.count(key) > 0:
            hl = "hodgkin's lymphoma"
            #print 'Hodgkin: ' + key
    if keywords.count('non hodgkin') > keywords.count('hodgkin') / 2:
            #print 'NHL by count'
            hl = 'non-hodgkin lymphoma'
    for key in non_hodgkin_keys:
        if keywords.count(key) > 0:
            hl = "non-hodgkin lymphoma"
            #print 'NHL: ' + key
            
    return hl

def getdisease(path, cancers):
    #This ugly block of code puts together the textblock, breif title, and any entries for condition into one long string
    details = parseall_ctgov(path, ['brief_summary/textblock', 'brief_title', 'condition'])
    condition = ' '.join(details[2])
    '''
    title = details[1]
    keywords = title[0] + ' ' + condition
    try: #Apparently this is a null for some conditions?
        textblock = details[0][0]
        keywords = keywords + ' ' + textblock
    except IndexError:
        pass
    '''
    keywords = condition # change the search rules so we only look at condition
    print keywords
    
    keywords = keywords.lower()
    keywords = keywords.replace(',' , ' ')
    keywords = keywords.replace('-', ' ')
    keywords = keywords.replace('.', ' ')
    keywords = keywords.replace("'s", " ")
    
    dz = []
    a = 0
    while a < len(cancers.kw1) :
        hit = False
        
        # Generate synonym list.  Ponderous to redo the cancer / carcinoma / malignancy every time, but feh
        synonyms = cancers.iloc[a][2:9]
        appendix = []
        for synonym in synonyms:
            if str(synonym) == 'nan':
                pass
            elif synonym[-6:] == 'cancer':
                appendix.append(synonym)
                appendix.append(synonym[:-6] + 'carcinoma')
                appendix.append(synonym[:-6] + 'malignancy')
            else:
                appendix.append(synonym)
        synonyms = appendix
        
        
        for synonym in synonyms: # each cancer has multiple synonyms.  we check each synonym separately
            if str(synonym) == 'nan':
                pass
            elif keywords.count(synonym) > 0: # if the synonym is present, we set a flag called hit
                hit = True
            else:
                pass
        if hit: # if the flag is set, then we append the 1st synonym.  in this way, the disease is only added once
            dz.append(synonyms[0])
        else:
            pass
        a = a + 1
    
    if len(dz) == 0:
        dz = salvagedz(keywords, cancers)
    if len(dz) == 0:
        dz = ['Other_Unknown']
    
    if dz.count("hodgkin's lymphoma") >0 :
        dz.remove("hodgkin's lymphoma")
        hl = fix_lymphoma(keywords)
        dz.append(hl)
    if dz.count('non-hodgkin lymphoma') > 0:
        dz.remove("non-hodgkin lymphoma")
        hl = fix_lymphoma(keywords)
        dz.append(hl)
    
    '''
    if (keywords.count('screening') >0 or keywords.count('prevent') > 0):
        newdz = []
        for deet in dz:
            deet = 'screening_' + deet
            newdz.append(deet)
        dz = newdz
    '''
    '''
    if (keywords.count('metastatic') > 0 or keywords.count('advanced') > 0):
        newdz = []
        for deet in dz:
            deet = 'advanced_' + deet
            newdz.append(deet)
        dz = newdz
    '''
            
    return dz

def fixmayo(path):
    attributes = ['source', 'location/facility/address/city']
    values = parse_ctgov(path, attributes)
    if values[0] != 'Mayo Clinic':
        return values[0]
    else:
        return ' '.join(values)
    
def CTgov_append (directory, target_dir, attributes, cancers):
    paths = os.listdir(directory)
    xmls = [path for path in paths if path[-3:] == "xml"]
    misses = 0
    hits = 0
    for path in xmls:
        values = parse_ctgov(directory + path, attributes)
        if values[2] == 'Mayo Clinic': #fixing the mayo clinic problem, potentiall
            values[2] = fixmayo(directory + path)
        else:
            pass
            
        disease = getdisease(directory + path, cancers)
        if disease == ['Other_Unknown']:
            misses = misses + 1
        else:
            hits = hits + 1
        for dz in disease:
            trial = {'nct_id' : values[0], 'Title' : values[1], 'Institution' : values[2],
            'Start_date' : values[3], 'End_date' : values[4], 'Phase' : values[5],
            'Enrollment' : values[6], 'Status' : values[7], 'Lead' : values[8], 'Disease' : dz}
            df = pd.DataFrame(trial, index = [0])
            #path = target_dir + 'all.csv'
            #df.to_csv(path, sep = ',', index = False, mode = 'a', encoding = 'utf-8')
            path = target_dir + dz + '.csv'
            df.to_csv(path, sep = ',' , index = False, mode = 'a', encoding = 'utf-8')

    print 'Misses: ' + str(misses)
    print 'Hits: ' + str(hits)

    return



CTgov_append(input_path, output_path, attributes, cancers)