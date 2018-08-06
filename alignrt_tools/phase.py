"""
This module defines the Phase class and PhaseCollection class, which store 
information about AlignRT phases. In addition, this class contains methods 
for deriving information about the phases from its constituant data structures.

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
from alignrt_tools.field import FieldCollection

class Phase(GenericAlignRTClass):
    """The Phase class contains attributes and methods that 
    pertain to an individual AlignRT phase (plan)

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
            the root of which is an individual phase (default is None)
        """

        super().__init__(tree)

        # Create a Field for the phase
        if tree is None:
            # Create an empty object
           self.field_collection = None

        else:
            # Create an SiteCollection using the ElementTree provided
            self.field_collection = FieldCollection(tree.find("Fields"))

class PhaseCollection:
    """The PhaseCollection class contains attributes and methods that 
    pertain to a collection of AlignRT phases for a given patient.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    None

    """
    # Attributes

    # Methods
    def __init__(self, collection_tree=None):
        """
        Parameters
        ----------
        collection_tree : ElementTree
            an ElementTree object created from Patient_Details.vpax, 
            the root of which is the Phases tag (default is None)
        """

        if collection_tree is None:
            # Create an empty phase collection
            self.num_phases = 0
            self.phases = []
        else:
            self.phases = []

            # Iterate through the ElementTree to create a Phase object for each site
            for tree in collection_tree:
                self.phases.append(Phase(tree))

            self.num_phases = len(self.phases)
