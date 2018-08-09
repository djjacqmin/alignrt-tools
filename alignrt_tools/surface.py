
"""
This module defines a Surface class. This class contains surfaces 
created by the AlignRT software.

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
from datetime import datetime
import dateutil.parser


class Surface:
    """The Surface class contains properties and methods for
    working with AlignRT surfaces

    ...

    Attributes
    ----------
    None

    Methods
    -------
    get_details_as_dataframe()
        Returns the surface details as a pandas dataframe
    """

    def __init__(self, path=None):
        """
        Parameters
        ----------
        path : str
            the path to the directory which contains the surface 
            files
        """
        self.path = path
        self.surface_details = {}
        self.site_details = {}

        # To reduce memory overhead and computation time, we will only 
        # load a surface mesh when requested
        self.surface_mesh = None

        if path is not None:

            # Read capture.ini and convert to dictionary
            capt_ini = open("{0}/capture.ini".format(path), "r")
            for line in capt_ini:
                pieces = line.split("=")
                if len(pieces) > 1:
                    self.surface_details[pieces[0]] = pieces[1].split("\n")[0]
                else:
                    self.surface_details[pieces[0]] = None
            # Read site.ini and convert to dictionary
            site_ini = open("{0}/capture.ini".format(path), "r")
            for line in site_ini:
                pieces = line.split("=")
                if len(pieces) > 1:
                    self.site_details[pieces[0]] = pieces[1].split("\n")[0]
                else:
                    self.site_details[pieces[0]] = None

