"""
This module defines the Patient class and PatientCollection class, which store 
information about AlignRT patients. In addition, this class contains methods 
for deriving information about the patient from its constituant data structures.

Copyright (C) 2018, Dustin Jacqmin, PhD

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE. See the GNU General Public License for more details. 

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Import helpful libraries
import xml.etree.ElementTree as ET
from datetime import datetime
import dateutil.parser
import pandas as pd
import os.path
from alignrt_tools import site


class Patient:
    """The Patient class contains attributes and methods that pertain to an 
    individual AlignRT patient

    ...

    Attributes
    ----------
    patient_data_tags : list(str)
        a list of data tags that are common to most patients

    Methods
    -------
    get_patient_details_as_dataframe()
        Returns a pandas dataframe object containing information about a patient

    """
    # Attributes
    patient_data_tags = (['GUID',
                          'Description',
                          'IsFromDicom',
                          'FirstName',
                          'MiddleName',
                          'Surname',
                          'PatientID',
                          'PatientVersion',
                          'Notes',
                          'Sex',
                          'DOB',
                          'LatestApprovedRecordSurfaceTimestamp',
                          'LastUsedPlotterType',
                          'PatientTextureLuminosity'])

    # Methods
    def __init__(self, path=None):

        if path is None:
            self.patient_details = {}

            for tag in Patient.patient_data_tags:
                self.patient_details[tag] = None

            self.path = None
            self.site_collection = site.SiteCollection()
        else:
            # Create patient using the path provided
            self._create_patient_from_directory(path)

    def get_patient_details_as_dataframe(self):
        # There is no pd.Series.from_dict(), so we will use pd.DataFrame.from_dict()
        # First, we will first have to convert each dictionary value to an array
        temp_dict = {}
        for key, value in self.patient_details.items():
            temp_dict[key] = [value]

        return pd.DataFrame.from_dict(temp_dict)

    def _create_patient_from_directory(self, path):

        self.path = path

        # Load the Patient Details XML to populate the rest of the
        try:
            root = ET.parse('{0}/Patient Details.vpax'.format(path)).getroot()
        except:
            root = ET.parse('{0}/Patient_Details.vpax'.format(path)).getroot()

        self.patient_details = {}

        for tag in Patient.patient_data_tags:
            self.patient_details[tag] = self._get_patient_attribute_from_vpax(
                root, tag)

        # Convert Date of birth to datetime object
        if self.patient_details['DOB'] is not None:
            self.patient_details['DOB'] = dateutil.parser.parse(
                self.patient_details['DOB'])

        # Convert LatestApprovedRecordSurfaceTimestamp to datetime object
        shorter_name = self.patient_details['LatestApprovedRecordSurfaceTimestamp']
        if shorter_name is not None:
            self.patient_details['LatestApprovedRecordSurfaceTimestamp'] = dateutil.parser.parse(
                shorter_name)

        # Convert IsFromDicom to boolean
        if self.patient_details['IsFromDicom'] == 'true':
            self.patient_details['IsFromDicom'] = True
        elif self.patient_details['IsFromDicom'] == 'false':
            self.patient_details['IsFromDicom'] = False

        # Create a SiteCollection for the patient
        self.site_collection = site.SiteCollection(root.find("Sites"))

    def _get_patient_attribute_from_vpax(self, tree, vpax_string):

        if tree.find(vpax_string) is not None:
            return tree.find(vpax_string).text
        else:
            return None


class PatientCollection:
    """The PatientCollection class contains attributes and methods that pertain to an a collection of AlignRT patients. """

    def __init__(self, path=None):

        if path is None:
            # Create an empty patient collection
            self.num_patients = 0
            self.patients = []
        else:
            # Create patient collection using the path provided
            self._create_patient_collection_from_directory(path)

    def get_patient_collection_as_dataframe(self):
        # Create an empty dataframe
        df = None

        for patient in self.patients:
            if df is None:
                df = patient.get_patient_details_as_dataframe()
            else:
                df = df.append(
                    patient.get_patient_details_as_dataframe(), ignore_index=True)

        return df

    def _create_patient_collection_from_directory(self, path):
        # Creates a patient collection from the directories within path.

        # Get a list of the subdirectories in the path
        folders = [name for name in os.listdir(
            path) if os.path.isdir(os.path.join(path, name))]

        # Determine which of the folders correspond to patients
        self.patients = []
        for folder in folders:
            if (os.path.isfile('{0}/{1}/Patient Details.vpax'.format(path, folder)) or
                    os.path.isfile('{0}/{1}/Patient_Details.vpax'.format(path, folder))):

                self.patients.append(Patient('{0}/{1}'.format(path, folder)))

        self.num_patients = len(self.patients)
