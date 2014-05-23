import xml.etree.ElementTree as etree
import pandas as pd
import os

input_path = 'C:\Users\JAG\USnewsy\Clinicaltrials\\'
output_path = 'C:\Users\JAG\USnewsy\Clinicaltrials\CTgovDz'
attributes = ['id_info/nct_id', 'brief_title', 'source', 'start_date', 'completion_date', 'phase']

cancers = [['colon', 'colorectal', 'rectal'], ['ovary', 'ovarian', 'endometrioid'], 
        ['breast', 'ductal carcinoma', 'DCIS'], ['lung', 'pulmonary', 'small cell'],
        ['lymphoma', 'leukemia', 'leukaemia'], ['brain', 'glioblastoma', 'astrocytoma', 'glioma'],
        ['pancreas', 'pancreatic'], ['melanoma'], ['basal cell', 'squamous cell', 'actinic keratosis', 'skin'],
        ['pediatric', 'ewing', 'neuroblastoma', 'rhabdomyosarcoma'], ['head and neck'],
        ['prostate', 'prostatic'], ['soft tissue', 'sarcoma'], ['esophagus', 'esophagael', 'esophageal', 'barrett'],
        ['kidney', 'renal', 'clear cell'], ['multiple myeloma', 'myeloma'], 
        ['bladder', 'transitional', 'uroepithelial'], ['liver', 'hepatic', 'hepatocellular'], ['thyroid'],
        ['cervical', 'cervix'], ['metastatic'], ['uterus', 'uterine', 'endometrial'],
        ['gastric', 'pyloric', 'pylori', 'stomach'], ['unknown primary'], ['pheochromocytoma'],
        ['mesothelioma'], ['testicular', 'testicle'], 
        ['myeloproliferative', 'myelodysplastic', 'polycythemia', 'thrombocytosis', 'thrombocythemia', 'mds', 'myelodysplasia'],
        ['hiv'], ['sinonasal', 'nasopharyngeal', 'nasopharyngael'], ['meningioma', 'leoptomeninges']]

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
        for synonym in cancer:
            if keywords.count(synonym) > 0:
                if dz == '':
                    dz = cancer[0]
                else:
                    dz = dz + ' ' + cancer[0]
                    multiple = True
    if len(dz) == 0:
        dz = 'Other / Unknown'
        print keywords
    if multiple:
        dz = 'Multiple: ' + dz
    return dz

def CTgov_append (directory, target_dir, attributes, cancers):
    paths = os.listdir(directory)
    xmls = [path for path in paths if path[-3:] == "xml"]
    misses = 0
    hits = 0
    for path in xmls:
        values = parse_ctgov(directory + path, attributes)
        disease = getdisease(directory + path, cancers)
        if disease == 'Other / Unknown':
            misses = misses + 1
        else:
            hits = hits + 1
        values.append(disease)
        trial = {'nct_id' : values[0], 'Title' : values[1], 'Institution' : values[2],
         'Start_date' : values[3], 'End_date' : values[4], 'Phase' : values[5], 'Disease' : values[6]}
        df = pd.DataFrame(trial, index = [0])
        path = target_dir + '_all_b.csv'
        df.to_csv(path, sep = ',', index = False, mode = 'a', encoding = 'utf-8')
        for cancer in cancers:
            if disease.count(cancer[0]) > 0:
                path = target_dir + '_' + cancer[0] + '_b.csv'
                df.to_csv(path, sep = ',' , index = False, mode = 'a', encoding = 'utf-8')
            else:
                pass
    print 'Misses: ' + str(misses)
    print 'Hits: ' + str(hits)
    return



CTgov_append(input_path, output_path, attributes, cancers)