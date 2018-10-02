"""
This module defines a GenericAlignRTClass class. This class will
be used to create subclasses for each item in the AlignRT data tree.

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

class GenericAlignRTClass:
    """The GenericAlignRTClass class is used to form the
    Patient, Site, Phase and Field subclasses.

    ...

    Attributes
    ----------
    alignrt_data_tags : list(str)
        a list of data tags that are common in Patient_Details.vpax 
        files

    Methods
    -------
    get_details_as_dataframe()
        Returns the patient details as a pandas dataframe
    """
    # Attributes
    alignrt_data_tags = (['Patient',
                        'GUID',
                        'Description',
                        'IsFromDicom',
                        'FirstName',
                        'MiddleName',
                        'Surname',
                        'PatientID',
                        'PatientVersion',
                        'Notes',
                        'Site',
                        'Phase',
                        'Field',
                        'IsoRotValue',
                        'LatestApprovedSurfaceDateTimeStamp',
                        'IsIsoCenterField',
                        'RepresentedCouchRotation',
                        'IsoXValue',
                        'IsoYValue',
                        'IsoZValue',
                        'IsApproved',
                        'DicomRTPlanUID',
                        'Sex',
                        'DOB',
                        'LatestApprovedRecordSurfaceTimestamp',
                        'IsDynamicBeamType',
                        'LastUsedPlotterType',
                        'PatientTextureLuminosity'])

    # Methods
    def __init__(self, tree=None):
        """
        Parameters
        ----------
        tree : ElementTree
            an ElementTree object created from details.vpax, 
            the root of which is an individual patient, site, phase 
            or field
        """
        self.details = {}

        if tree is None:
            # Create an empty object
            pass

        else:
            # Create an object using the ElementTree provided
            for tag in GenericAlignRTClass.alignrt_data_tags:
                if tree.find(tag) is not None:
                    self.details[tag] = tree.find(tag).text

        self._perform_type_conversions()

    def get_details_as_dataframe(self):
        """
        Returns the details dictionary as a dataframe item

        Parameters
        ----------
        None
        
        """

        # First, we will first have to convert each dictionary value to 
        # an array with a single item
        temp_dict = {}
        for key, value in self.details.items():
            temp_dict[key] = [value]

        # Finally, return the dataframe
        return pd.DataFrame.from_dict(temp_dict)

    def __str__(self):
        """
        Returns a string representation of the object

        Parameters
        ----------
        None

        """

        obj_str = '**********\n'
        for key, value in self.details.items():
            if value is not None:
                obj_str = obj_str + key + ': ' + str(value) +'\n'

        obj_str = obj_str + '**********\n'
        return obj_str
    
    def _perform_type_conversions(self):
        """
        A private method that converts some of the patient details
        elements into more useful datatypes

        Parameters
        ----------
        None

        """

        # Convert Date of birth to datetime object
        if 'DOB' in self.details.keys():
            self.details['DOB'] = dateutil.parser.parse(
                self.details['DOB'])

        # Convert LatestApprovedSurfaceDateTimeStamp to datetime object
        shorter_name = 'LatestApprovedSurfaceDateTimeStamp'
        if shorter_name in self.details.keys():
            self.details[shorter_name] = dateutil.parser.parse(
                self.details[shorter_name])

        # Convert LatestApprovedRecordSurfaceTimestamp to datetime object
        shorter_name = 'LatestApprovedRecordSurfaceTimestamp'
        if shorter_name in self.details.keys():
            self.details[shorter_name] = dateutil.parser.parse(
                self.details[shorter_name])

        # Convert IsFromDicom to boolean
        if 'IsFromDicom' in self.details.keys():
            if self.details['IsFromDicom'] == 'true':
                self.details['IsFromDicom'] = True
            elif self.details['IsFromDicom'] == 'false':
                self.details['IsFromDicom'] = False