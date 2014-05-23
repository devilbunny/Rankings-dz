Rankings-dz
===========

Generate hospital rankings based on clinical trials for specific cancers

Method: 
* Download a set of clinical trials from clinicaltrials.gov
  I did this by searching for 'cancer', which generated ~40,000 hits
  You can choose to download in a variety of formats - select all data types XML

* Unzip
  I was too lazy to put in the capability for this project

* Run CTgov-Wrangle-dz-any-diag
  The title reflects a long set of evolutions.
  Specify the input and output paths based on your file names
  Attributes are the XML tags that will be extracted.
    Currently: NCT ID - unique ID; brief_title - EWISOTT;
                source - the institution which I credit;
                start and completion dates - EWISOTT
                phase - the clinical trial phase.  CTgov allows N/A, Phase 0-4, Phase 1 / Phase 2, Phase 2 / Phase 3
  Cancers are the cancers studied.  This is currently set as a list of lists.  Each sublist is the list of words
    that define the diagnosis cluster, e.g. colon, colorectal, rectal.  If any word in the sublist is present, the
    trial is tagged with the first word in the cluster.  e.g. if a trial has 'colorectal' in its keywords, it will
    be taged as a 'colon' type trial.
  
  parse_ctgov returns the values given in tags for the clinical trial.  
  The inputs are 'path' - the location of the XML file to be parsed and 'attributes' the names of the tags to be
  interrogated.  path is a string, attributes is a series.
  It returns a series with the values associated with each tag in the same order as in the 'attributes' series.
  If an attribute is not found, 'Not found' is inserted into the series.
  
  It has 2 v. important limitations
    1. Only the 1st tag is returned, so if a trial has several keywords, only the first will be returned
    2. It usually only scans the top-level tags, so if the desired piece of information is a sub-tag, it has
        to be called explicitly.  e.g. nct_id returns nothing, however id_info/nct_id does, because nct_id is 
        a child tag within the id_info tag
  
  parseall_ctgov - basically the same as parse_ctgov, except it finds all instances of a tag and returns all the
    associated values.  returns as a series of series (one for each attribute in 'attributes'
    
  getdisease is complicated.
  it takes the path of the XML to be studied as a string
  and cancers, as a list of lists, formatted as explained above.
  
  Then it calls parseall to get all the different values for the condition tags.
  The conditions are then joined into a single string and set to lowercase.
  For each synonym in each cancer series, we check whether the synonym is present in the strin of conditions
  If yes, the first cancer in the cancer series is associated with the trial.
  If multiple cancer series are associated, the word, 'Multiple' is added to the begining of the disease
    Right now, this does nothing.
  If no cancers are associated, the string 'Other / Unknown' is returned.
  
  CTgov_append
    directory - location of XML files
    target_dir - location for .csv files describing different trials
    attributes - series as above
    cancers - series of series as above
    
    for each XML file in 'directory' identified the attributes listed in attributes, as well as the condition being
    studied (using cancers and the 'getdisease' function)
    
    For each XML file / trial, the record is added to the file for 'all' trials, as well as _each_ file associated for
    the cancers present.  e.g. if a trial studies lung and colon cancer, then it will be added to all.csv, lung.csv and
    colon.csv
    

* CTgov-pivot-dz
  Simplicity itself.  For each different cancer, creates a pivot table of institution and phase, such that
  you get a list of institutions and how many trials they did for each disease.  This also cleans up the phases
  such that phase 0, 4, and N/A are combined, and phase 1/2 and 2/3 are demoted.

* Dictmerge
  Also relatively simple.  For each pivoted file, merges onto a dictionary of institutions, then groups so that all of 
  the trials from a single institution are brought together under a single name.  The dictionary is a stand-alone .csv
  file to allow updating and rerunning.  These are then merged onto the USNews rank-list so the ranks can be compared
  to what USN got.  Finally, all the lists are concatenated to produce a 'sum' sheet with all the different cancers
  on the same page.
    
    
    
    
    
    
    
    
    
    
