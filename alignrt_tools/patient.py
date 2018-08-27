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
import pandas as pd
import os.path
from alignrt_tools.generic import GenericAlignRTClass
from alignrt_tools.site import Site
from alignrt_tools.surface import Surface


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
        path : str
            the path to the directory which contains the patient's 
            files
        """

        # Instantiate the Patient using the generic class
        super().__init__(tree)

        self.path = path
        self.sites = []
        self.surfaces = {}

        # Create an array of sites for the patient
        if tree is not None:

            # Iterate through the ElementTree to create a Site object for each site
            for site_tree in tree.find('Sites'):
                self.sites.append(Site(site_tree))

        if path is not None:

            # Get a list of the subdirectories in the path
            folders = [
                name
                for name in os.listdir(path)
                if os.path.isdir(os.path.join(path, name))
            ]

            # Determine if the folders are surfaces
            for folder in folders:
                if os.path.isfile("{0}/{1}/capture.obj".format(path, folder)):
                    # Create a new surface
                    self.surfaces[folder] = Surface(
                        "{0}/{1}".format(path,                                      folder))


class PatientCollection:
    """The PatientCollection class contains attributes and methods that pertain to an a collection of AlignRT patients. 

    ...

    Attributes
    ----------
    None

    Methods
    -------
    get_collection_as_dataframe()
        Returns the patient details as a pandas dataframe for all 
        patients in the collection
    """

    def __init__(self, path=None):

        if path is None:
            # Create an empty patient collection
            self.num_patients = 0
            self.patients = []
        else:
            # Create patient collection using the path provided
            self._create_patient_collection_from_directory(path)

    def get_collection_as_dataframe(self):
        # Create an empty dataframe
        df = None

        for patient in self.patients:
            if df is None:
                df = patient.get_details_as_dataframe()
            else:
                df = df.append(
                    patient.get_details_as_dataframe(), ignore_index=True)

        return df

    def _create_patient_collection_from_directory(self, path):
        # Creates a patient collection from the directories within path.

        # Get a list of the subdirectories in the path
        folders = [
            name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))
        ]

        # Determine which of the folders correspond to patients
        self.patients = []
        for folder in folders:
            if os.path.isfile("{0}/{1}/Patient Details.vpax".format(path, folder)):
                pd_path = "{0}/{1}/Patient Details.vpax".format(path, folder)
                px_path = "{0}/{1}/".format(path, folder)
                self.patients.append(
                    Patient(ET.parse(pd_path).getroot(), px_path))

            elif os.path.isfile("{0}/{1}/Patient_Details.vpax".format(path, folder)):
                pd_path = "{0}/{1}/Patient_Details.vpax".format(path, folder)
                px_path = "{0}/{1}/".format(path, folder)
                self.patients.append(
                    Patient(ET.parse(pd_path).getroot(), px_path))

        self.num_patients = len(self.patients)
