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

class Site:
    """The Site class contains attributes and methods that 
    pertain to an individual AlignRT site
    
    ...

    Attributes
    ----------
    site_data_tags : list(str)
        a list of data tags that are common to most sites

    Methods
    -------
    
    """
    # Attributes
    site_data_tags = (['GUID', 
                         'Description', 
                         'IsFromDicom'])

    # Methods
    def __init__(self,site_tree=None):
        """
        Parameters
        ----------
        site_tree : ElementTree
            an ElementTree object that contains site details (default is None)
        """

        if site_tree is None:
            # Create an empty site
            self.site_details = {}
            
            for tag in Site.site_data_tags:
                self.site_details[tag] = None

        else:
            # Create site using the ElementTree provided
            self._create_site_from_element_tree(site_tree)

    def _create_site_from_element_tree(self,site_tree):
        """ 
        A private method used to populate site details from an ElementTree object

        Parameters
        ----------
        site_tree : ElementTree
            an ElementTree object that contains site details
        """

        self.site_details = {}

        # Loop over site data tags
        for tag in Site.site_data_tags:
            if site_tree.find(tag) is not None: 
                self.site_details[tag] = site_tree.find(tag).text
            else:
                self.site_details[tag] = None
        
        # Convert IsFromDicom to boolean
        if self.site_details['IsFromDicom'] == 'true':
            self.site_details['IsFromDicom'] = True
        elif self.site_details['IsFromDicom'] == 'false':
            self.site_details['IsFromDicom'] = False

class SiteCollection:
    """The SiteCollection class contains attributes and methods that pertain to a collection of AlignRT sites for a given patient.
    
    ...

    Attributes
    ----------
    None

    Methods
    -------
    None
        
    """
    # Attributes