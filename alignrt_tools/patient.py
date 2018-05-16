"""
patient.py

This module defines the Patient class, which stores information about individual AlignRT patients. In addition, this class contains methods for deriving information about the patient from its constituant data structures.
"""

# Import helpful libraries
import xml.etree.ElementTree as ET
from datetime import datetime
import dateutil.parser

class Patient:
    """The Patient class contains attributes and methods that pertain to an individual AlignRT patient"""
    
    # Attributes
    path = None # the full path to this patient
    guid = None # the GUID found in the Patient Details.vpax file
    description = None # the Description found in the Patient Details.vpax file
    is_from_dicom = None # the IsFromDicom found in the Patient Details.vpax file
    firs_tname = None # the FirstName found in the Patient Details.vpax file
    middle_name = None # the MiddleName found in the Patient Details.vpax file
    surname = None # the Surname found in the Patient Details.vpax file
    patient_id = None # the PatientID found in the Patient Details.vpax file
    patient_version = None # the PatientVersion found in the Patient Details.vpax file
    notes = None # the Notes found in the Patient Details.vpax file
    sites = [] # the Sites, stored in a list, found in the Patient Details.vpax file
    sex = None # the Sex found in the Patient Details.vpax file
    dob = None # the DOB found in the Patient Details.vpax file
    latest_approved_record_surface_timestamp = None # the LatestApprovedRecordSurfaceTimestamp found in the Patient Details.vpax file
    
    
    # Methods
    def __init__(self,path):
        self.path = path
        
        # Load the Patient Details XML to populate the rest of the 
        try: 
            root = ET.parse('{0}/Patient Details.vpax'.format(path)).getroot()
        except:
            root = ET.parse('{0}/Patient_Details.vpax'.format(path)).getroot()
        
        self.dob = dateutil.parser.parse(root.find('DOB').text)
        self.guid = root.find('GUID').text
        