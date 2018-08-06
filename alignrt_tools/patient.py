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
from alignrt_tools.site import SiteCollection
from alignrt_tools.generic import GenericAlignRTClass


class Patient(GenericAlignRTClass):
    """The Patient class contains attributes and methods that pertain 
    to an individual AlignRT patient

    ...

    Attributes
    ----------
    alignrt_data_tags : list(str)
        a list of data tags inherited from the superclass

    Methods
    -------
    get_details_as_dataframe()
        Returns the patient details as a pandas dataframe
    """

    # Methods
    def __init__(self, tree=None, path=None):
        """
        Parameters
        ----------
        tree : ElementTree
            an ElementTree object created from Patient_Details.vpax, 
            the root of which is an individual patient (default is None)
        """

        super().__init__(tree)

        self.path = path

        # Create a SiteCollection for the patient
        if tree is None:
            # Create an empty object
           self.site_collection = None

        else:
            # Create an SiteCollection using the ElementTree provided
            self.site_collection = SiteCollection(tree.find("Sites"))

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
            if os.path.isfile('{0}/{1}/Patient Details.vpax'.format(path, folder)):
                pd_path = '{0}/{1}/Patient Details.vpax'.format(path, folder)
                self.patients.append(Patient(ET.parse(pd_path).getroot(),path))

            elif os.path.isfile('{0}/{1}/Patient_Details.vpax'.format(path, folder)):
                pd_path = '{0}/{1}/Patient_Details.vpax'.format(path, folder)
                self.patients.append(Patient(ET.parse(pd_path).getroot(),path))
                
        self.num_patients = len(self.patients)
