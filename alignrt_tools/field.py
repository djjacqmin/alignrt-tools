"""
This module defines the Field class and FieldCollection class, which store 
information about AlignRT fields. In addition, this class contains methods 
for deriving information about the fields from its constituent data structures.

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

from alignrt_tools.generic import GenericAlignRTClass


class Field(GenericAlignRTClass):
    """The Field class contains attributes and methods that 
    pertain to an individual AlignRT field

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
    def __init__(self, tree=None):
        """
        Parameters
        ----------
        tree : ElementTree
            an ElementTree object created from Patient_Details.vpax, 
            the root of which is an individual field (default is None)
        """

        super().__init__(tree)
        self.surfaces = []

    def get_realtimedeltas_as_dataframe(self):
        """
        Returns the real-time deltas for this field as a dataframe

        Parameters
        ----------
        None

        Returns
        -------
        A dataframe containing all of the real-time deltas for this field

        """
        df = None

        for surface in self.surfaces:

            if df is None:
                df = surface.get_realtimedeltas_as_dataframe()
            else:
                df = df.append(
                    surface.get_realtimedeltas_as_dataframe(), ignore_index=True
                )

        # At this point, df may still yet be None
        # if this Field does not have real-time deltas
        if df is not None:
            for key, value in self.details.items():
                super_key = "Field Details - " + key
                df[super_key] = value

        return df
