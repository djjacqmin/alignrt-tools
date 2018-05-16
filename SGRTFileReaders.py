"""
SGRTFileReaders.py
This python file contains functions that read the many types of files in the AlignRT patient data tree.
"""

import xml.etree.ElementTree as ET

""" Helper functions """

def anydup(thelist):
    seen = set()
    for x in thelist:
        if x in seen: return True
        seen.add(x)
    return False

def etree_to_dict(t,enumerated=False):
    d={}
    count=1
    
    for child in t:
        # Construct key name
        if enumerated:
            key = '{}-{}'.format(child.tag,count)
        else: 
            key = child.tag
        
        # Determine if the child has children
        if len(child)>0:
            # enumberate the children?
            enum = anydup([ele.tag for ele in child])
            d[key] = etree_to_dict(child,enum)
            count=count+1
        else:
            d[child.tag] = child.text
        
    return d


""" Patient directory file readers """

# ini files
def read_PatientDetails_ini(path):
    
    try: 
        thisfile = open('{0}/Patient Details.ini'.format(path),'r')
    except:
        thisfile = open('{0}/Patient_Details.ini'.format(path),'r')
           
    d = {}

    for line in thisfile:
        pieces = line.split('=')
        if len(pieces) > 1:
            d[pieces[0]] = pieces[1].split("\n")[0]
    
    return d

# xml files
def read_PatientDetails_vpax(path):
    
    try: 
        tree = ET.parse('{0}/Patient Details.vpax'.format(path)).getroot()
    except:
        tree = ET.parse('{0}/Patient_Details.vpax'.format(path)).getroot()
    
    return etree_to_dict(tree)

def read_PatientTreatmentThreshold_xml(path):
    pass

""" Reference surface directory file readers """

# ini files

def read_capture_ini(path):
    pass

def read_site_ini(path):
    pass

def read_Stereo_G_LB_ini(path):
    pass

# xml files

def read_baserotations_xml(path):
    pass

# trm files

def read_IsocenterShift_trm(path):
    pass

def read_IsocenterShift_timestamp_trm(path):
    pass

def read_DICOMRTIsoShift_tfm(path):
    pass

def read_VRTToIsoTransformation_tfm(path):
    pass

# obj-type files

def read_capture_obj(path):
    pass

def read_selection_roi(path):
    pass

# other files

def read_calib_clb(path):
    pass

def read_roilabels_txt(path):
    pass

""" Monitoring directory file readers """

def read_RealTimeDeltas_txt(path):
    pass

""" Dicom_Data directory file readers """

def read_RTPLAN_dcm(path):
    pass

# 