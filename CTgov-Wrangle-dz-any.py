import xml.etree.ElementTree as etree
import pandas as pd
import os

input_path = 'C:\Users\JAG\USnewsy\Clinicaltrials\\'
output_path = 'C:\Users\JAG\USnewsy\Clinicaltrials\CTgovDz'
attributes = ['id_info/nct_id', 'brief_title', 'source', 'start_date', 'completion_date', 'phase']
cancers = ['ovarian','breast','lung','lymphoma','leukemia','brain','pancreatic','melanoma','colon',
            'head and neck', 'prostate', 'soft tissue', 'esophageal','kidney', 'multiple myeloma',
            'ewing', 'rhabdomyosarcoma', 'bladder', 'liver', 'thyroid']

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

def getdisease(path, cancers):
    keywords = parseall_ctgov(path, ['condition'])
    keywords = keywords[0]
    keywords = ' '.join(keywords)
    keywords = keywords.lower()
    dz = ''
    multiple = False
    for cancer in cancers:
        if keywords.count(cancer) > 0:
            if dz == '':
                dz = cancer
            else:
                dz = dz + ' ' + cancer
                multiple = True
    if len(dz) == 0:
        dz = 'Other / Unknown'
        print keywords
    if multiple:
        dz = 'Multiple: ' + dz
    print dz
    return dz

def CTgov_append (directory, target_dir, attributes, cancers):
    paths = os.listdir(directory)
    xmls = [path for path in paths if path[-3:] == "xml"]
    for path in xmls:
        values = parse_ctgov(directory + path, attributes)
        disease = getdisease(directory + path, cancers)
        values.append(disease)
        trial = {'nct_id' : values[0], 'Title' : values[1], 'Institution' : values[2],
         'Start_date' : values[3], 'End_date' : values[4], 'Phase' : values[5], 'Disease' : values[6]}
        df = pd.DataFrame(trial, index = [0])
        path = target_dir + '_all.csv'
        df.to_csv(path, sep = ',', index = False, mode = 'a', encoding = 'utf-8')
        for cancer in cancers:
            if disease.count(cancer) > 0:
                path = target_dir + '_' + cancer + '.csv'
                df.to_csv(path, sep = ',' , index = False, mode = 'a', encoding = 'utf-8')
            else:
                pass
    return



CTgov_append(input_path, output_path, attributes, cancers)