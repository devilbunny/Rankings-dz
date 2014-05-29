import xml.etree.ElementTree as etree
import pandas as pd
import os

input_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\\'
output_path = 'C:\Users\JAG\USN-dz\Clinicaltrials\CTgovDz_agg_'
attributes = ['id_info/nct_id', 'brief_title', 'source', 'start_date', 
            'completion_date', 'phase', 'enrollment', 'overall_status']

top_cancers = [['lung', 'bronch', 'small-cell', 'small cell'],
            ['prostate', 'prostatic'],
            ['breast', 'ductal carcinoma', 'DCIS'],
            ['colon', 'colorectal', 'rectal', 'rectum'],
            ['pancreas', 'pancreatic'],
            ['liver', 'hepatocellular', 'intrahepatic bile', 'cholangio'],
            ['ovary', 'ovarian'],
            ['leukemia', 'cml', 'cll', 'hairy cell'],
            ['esophagus', 'esophagael', 'esophageal', 'barrett'],
            ['uterus', 'uterine'],
            ['bladder', 'urinary', 'transitional', 'uroepithelial'],
            ['non-hodgkin', 'nhl', 'burkitt', 
                'chronic lymphocytic', 'small lymphocytic',
                'diffuse large B-cell', 'follicular lymphoma',
                'immunoblastic large cell lymphoma',
                'precursor B-lymphoblastic', 'mantle cell',
                'mycosis fungoides', 'cutaneous T-cell',
                'anaplastic large cell', 'precursor T-lymphoblastic', 'lymphoma'],
            ['kidney', 'renal', 'clear cell'],
            ['brain', 'glioblastoma', 'astrocytoma', 'glioma', 'cns',
                 'meningioma', 'leoptomeninges', 'spinal cord', 'choroid'],
            ['melanoma'],
            ['oral', 'pharynx', 'mouth', 'tongue']]


other_cancers = [['skin', 'basal cell', 'squamous cell', 'actinic keratosis'],
        ['head and neck'], ['soft tissue', 'sarcoma'],
        ['multiple myeloma', 'plasma cell'], 
        ['thyroid'],
        ['cervical', 'cervix'], 
        ['metastatic'],
        ['gastric', 'pyloric', 'pylori', 'stomach'], 
        ['unknown primary'], 
        ['mesothelioma'], 
        ['testicular', 'testicle'], 
        ['myeloproliferative', 'myelodysplastic', 'polycythemia', 'thrombocytosis', 'thrombocythemia', 'mds', 'myelodysplasia'],
        ['hiv', 'aids'], 
        ['sinonasal', 'nasopharyngeal', 'nasopharyngael'],
        ['pediatric', 'ewing', 'neuroblastoma', 'rhabdomyosarcoma'],
        ['retinoblastoma'],
        ['neuroendocrine', 'multiple endocrine', 'islet', 'pheochromocytoma', 'medullary thyroid']]

cancers = top_cancers + other_cancers


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
        hit = False
        for synonym in cancer: # each cancer has multiple synonyms.  we check each synonym separately
            if keywords.count(synonym) > 0: # if the synonym is present, we set a flag called hit
                hit = True
            else:
                pass
        if hit: # if the flag is set, then we append the 1st synonym.  in this way, the disease is only added once
            if dz == '':
               dz = cancer[0]
            else:
                dz = dz + ', ' + cancer[0]
                multiple = True
    if len(dz) == 0:
        dz = 'Other / Unknown'
    if multiple:
        dz = 'Multiple'
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

        try:
            values[6] = int(values[6])
        except ValueError:
            values[6] = 0

        trial = {'nct_id' : values[0], 'Title' : values[1], 'Institution' : values[2],
         'Start_date' : values[3], 'End_date' : values[4], 'Phase' : values[5],
         'Enrollment' : values[6], 'Status' : values[7], 'Disease' : disease}
        df = pd.DataFrame(trial, index = [0])
        path = target_dir + '_all.csv'
        df.to_csv(path, sep = ',', index = False, mode = 'a', encoding = 'utf-8')
        
        '''
        for cancer in cancers:
            if disease.count(cancer[0]) > 0:
                path = target_dir + '_' + cancer[0] + '.csv'
                df.to_csv(path, sep = ',' , index = False, mode = 'a', encoding = 'utf-8')
            else:
                pass
        '''
    print 'Misses: ' + str(misses)
    print 'Hits: ' + str(hits)
    return



CTgov_append(input_path, output_path, attributes, cancers)