"""
This module defines the Patient class and PatientCollection class, which store 
information about AlignRT patients. In addition, this class contains methods 
for deriving information about the patient from its constituent data structures.

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
from pathlib import Path
from alignrt_tools.generic import GenericAlignRTClass
from alignrt_tools.site import Site
from alignrt_tools.surface import Surface
from alignrt_tools.treatment import TreatmentCalendar
from IPython.display import clear_output


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
    def __init__(self, tree=None, patient_path=None):
        """
        Parameters
        ----------
        tree : ElementTree
            an ElementTree object created from Patient_Details.vpax, 
            the root of which is an individual patient (default is None)
        patient_path : str
            the path to the directory which contains the patient's 
            files
        """

        # Instantiate the Patient using the generic class
        super().__init__(tree)

        self.patient_path = patient_path
        self.sites = []

        # Create an array of sites for the patient
        if tree is not None:

            # Iterate through the ElementTree to create a Site object for each site
            for site_tree in tree.find('Sites'):
                self.sites.append(Site(site_tree))

        if patient_path is not None:

            # Create a Path object from alignrt_path
            r = Path(patient_path)

            # Get a list of the subdirectories in the path
            folders = [ item for item in r.iterdir() if item.is_dir() ]

            # Determine if the folders are surfaces
            for folder in folders:
                if (folder / "capture.obj").is_file():
                    # Create a new surface
                    temp_surface = Surface(folder)

                    # Identify the Site, Phase and Field for the surface
                    for site in self.sites:
                        if site.details['Description'] == temp_surface.site_details['Treatment Site']:
                            for phase in site.phases:
                                if phase.details['Description'] == temp_surface.site_details['Phase']:
                                    for field in phase.fields:
                                        if field.details['Description'] == temp_surface.site_details['Field']:
                                            # Append the surface to this field
                                            field.surfaces.append(temp_surface)

    def get_realtimedeltas_as_dataframe(self):
        """
        Returns the real-time deltas for this patient as a dataframe

        Parameters
        ----------
        None

        Returns
        -------
        A dataframe containing all of the real-time deltas for this patient

        """
        df = None

        for site in self.sites:

            if df is None:
                df = site.get_realtimedeltas_as_dataframe()
            else:
                df = df.append(
                    site.get_realtimedeltas_as_dataframe(), ignore_index=True)

        # At this point, df may still yet be None
        # if this Patient does not have real-time deltas
        if df is not None:
            # Append the field details
            for key, value in self.details.items():
                super_key = 'Patient Details - ' + key
                df[super_key] = value

        return df

    def get_treatment_calendar(self):
        """
        Returns a TreatmentCalendar for this patient

        Parameters
        ----------
        None

        Returns
        -------
        A TreatmentCalendar object for this patient. It may be empty if there are no real-time deltas for this patient.

        """

        return TreatmentCalendar(self.get_realtimedeltas_as_dataframe())


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

    def __init__(self, alignrt_path=None):

        self.patients = []

        if alignrt_path is not None:
            # Create patient collection using the path provided
            self._create_patient_collection_from_directory(alignrt_path)

    def get_num_patients(self):
        return len(self.patients)
    
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

    def _create_patient_collection_from_directory(self, alignrt_path):
        # Creates a patient collection from the directories within path.

        # Create a Path object from alignrt_path
        r = Path(alignrt_path)

        # Get a list of the subdirectories in the path
        folders = [ item for item in r.iterdir() if item.is_dir() ]

        # Determine which of the folders correspond to patients
        count = 1

        for folder in folders:
            # Print the progress of the patient data structure creation
            clear_output()
            print("Processing folder {} of {}".format(count, len(folders)))
            count = count + 1

            # Check to see if Patient Details.vpax is in the folder
            if (folder / "Patient Details.vpax").is_file():
                self.patients.append(
                    Patient(ET.parse(folder / "Patient Details.vpax").getroot(), folder))

            # Check to see if Patient_Details.vpax is in the folder
            if (folder / "Patient_Details.vpax").is_file():
                self.patients.append(
                    Patient(ET.parse(folder / "Patient_Details.vpax").getroot(), folder))