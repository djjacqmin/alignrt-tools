"""
SGRTFileReaders.py
This python file contains functions that read the many types of files in the AlignRT patient data tree.
"""

import xml.etree.ElementTree as ET

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
    pass

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