"""
patient.py
This module defines the Patient class, which stores information about individual AlignRT patients. In addition, this class contains methods for deriving information about the patient from its constituant data structures.

Copyright (C) 2018, Dustin Jacqmin, PhD

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Import helpful libraries
import xml.etree.ElementTree as ET
from datetime import datetime
import dateutil.parser

class Patient:
    """The Patient class contains attributes and methods that pertain to an individual AlignRT patient"""
        
    # Methods
    def __init__(self,path=None):
        
        if path is None:
            # Create an empty patient  
            self.create_empty_patient()
        else:
            # Create patient using the path provided
            self.create_patient_from_directory(path)
            
    def create_empty_patient(self):
        self.guid = None
        self.description = None
        self.is_from_dicom = None
        self.first_name = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.patient_id = None
        self.patient_version = None
        self.patient_version = None
        self.notes = None
        self.sex = None
        self.date_of_birth = None
        self.latest_approved_record_surface_timestamp = None
        self.last_used_plotter_type = None
        self.patient_texture_luminosity = None
        self.sites = []
            
    def create_patient_from_directory(self,path):
        
        self.path = path
        
        # Load the Patient Details XML to populate the rest of the 
        try: 
            root = ET.parse('{0}/Patient Details.vpax'.format(path)).getroot()
        except:
            root = ET.parse('{0}/Patient_Details.vpax'.format(path)).getroot()
        
        # Collect patient attributes from the Patient Details file
        self.guid = self.get_patient_attribute_from_vpax(root,'GUID')
        self.description = self.get_patient_attribute_from_vpax(root,'Description')
        self.is_from_dicom = self.get_patient_attribute_from_vpax(root,'IsFromDicom')
        self.first_name = self.get_patient_attribute_from_vpax(root,'FirstName')
        self.first_name = self.get_patient_attribute_from_vpax(root,'FirstName')
        self.middle_name = self.get_patient_attribute_from_vpax(root,'MiddleName')
        self.last_name = self.get_patient_attribute_from_vpax(root,'Surname')
        self.patient_id = self.get_patient_attribute_from_vpax(root,'PatientID')
        self.patient_version = self.get_patient_attribute_from_vpax(root,'PatientVersion')
        self.patient_version = self.get_patient_attribute_from_vpax(root,'PatientVersion')
        self.notes = self.get_patient_attribute_from_vpax(root,'Notes')
        self.sex = self.get_patient_attribute_from_vpax(root,'Sex')
        self.date_of_birth = self.get_patient_attribute_from_vpax(root,'DOB')
        self.latest_approved_record_surface_timestamp = self.get_patient_attribute_from_vpax(root,
                                                           'LatestApprovedRecordSurfaceTimestamp')
        self.last_used_plotter_type = self.get_patient_attribute_from_vpax(root,'LastUsedPlotterType')
        self.patient_texture_luminosity = self.get_patient_attribute_from_vpax(root,'PatientTextureLuminosity')
        
        # Convert attribute strings to other types, where applicable
        if self.date_of_birth is not None: 
            self.date_of_birth = dateutil.parser.parse(self.date_of_birth)
        if self.latest_approved_record_surface_timestamp is not None: 
            self.latest_approved_record_surface_timestamp = dateutil.parser.parse(self.latest_approved_record_surface_timestamp)
        if self.is_from_dicom == 'true':
            self.is_from_dicom = True
        elif self.is_from_dicom == 'false':
            self.is_from_dicom = False
            
        # Populate the sites array
        self.sites = []
        
    def get_patient_attribute_from_vpax(self,tree,vpax_string):
        if tree.find(vpax_string) is not None: 
            return tree.find(vpax_string).text
        else:
            return None
        
        
    
