"""
This module defines the Site class and SiteCollection class, which store
information about AlignRT sites. In addition, this class contains methods
for deriving information about the sites from its constituant data structures.

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
from alignrt_tools.phase import Phase


class Site(GenericAlignRTClass):
    """The Site class contains attributes and methods that
    pertain to an individual AlignRT site

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
            the root of which is an individual site (default is None)
        """

        super().__init__(tree)
        self.phases = []

        # Create an array for the phases that belong to this site
        if tree is not None:

            # Iterate through the ElementTree to create a Phase object for each phase
            for phase_tree in tree.find('Phases'):
                self.phases.append(Phase(phase_tree))
