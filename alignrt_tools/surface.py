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
import os.path
from datetime import datetime
import dateutil.parser
from alignrt_tools.realtimedeltas import RealTimeDeltas
import pandas as pd


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

    def __init__(self, path=None, load_rtds=False):
        """
        Parameters
        ----------
        path : str
            the path to the directory which contains the surface 
            files
        load_rtds : bool
            determines whether the RealTimeDelta objects are created during initialization (default is False)
        """
        self.path = path
        self.surface_details = {}
        self.site_details = {}
        self.realtimedeltas_collection = {}

        # To reduce memory overhead and loading time, we will only
        # load a surface mesh when requested
        self.surface_mesh = None

        if path is not None:

            # Read capture.ini and convert to dictionary
            with open(
                "{0}/capture.ini".format(path), "r", encoding="latin-1"
            ) as capt_ini:
                try:
                    for line in capt_ini:

                        pieces = line.split("=")
                        if len(pieces) > 1:
                            self.surface_details[pieces[0]] = pieces[1].split("\n")[0]
                        else:
                            self.surface_details[pieces[0]] = None
                except UnicodeDecodeError:
                    print(
                        "Parsing {} resulted in unicode error".format(
                            "{0}/capture.ini".format(path)
                        )
                    )
                capt_ini.close()

            # Read site.ini and convert to dictionary
            with open("{0}/site.ini".format(path), "r", encoding="latin-1") as site_ini:
                try:
                    for line in site_ini:
                        pieces = line.split("=")
                        if len(pieces) > 1:
                            self.site_details[pieces[0]] = pieces[1].split("\n")[0]
                        else:
                            self.site_details[pieces[0]] = None
                except UnicodeDecodeError:
                    print(
                        "Parsing {} resulted in Unicode decode error".format(
                            "{0}/site.ini".format(path)
                        )
                    )
                site_ini.close()

            if load_rtds:
                self.load_realtimedeltas()

    def load_realtimedeltas(self):

        # Verify that the collection is empty
        if not self.realtimedeltas_collection:
            # Get a list of the subdirectories in the surface folder path
            folders = [
                name
                for name in os.listdir(self.path)
                if os.path.isdir(os.path.join(self.path, name))
            ]

            # Determine if any of the folders contain
            # RealTimeDeltas_DATE_TIME.txt files
            for folder in folders:
                """ 
                The name of a RealTimeDeltas folder is 
                Monitoring_DATE_TIME. The name of the file within will 
                be RealTimeDeltas_DATE_TIME.txt. First, let's extract 
                the DATE_TIME string. 
                """

                # Check to see if this a monitoring folder
                if folder[0:10] == "Monitoring":

                    # Construct the likely RealTimeDeltas file path
                    date_time_str = folder.split("Monitoring_")[1]
                    rtd_path = (
                        self.path
                        + "/"
                        + folder
                        + "/"
                        + "RealTimeDeltas_"
                        + date_time_str
                        + ".txt"
                    )
                    if os.path.isfile(rtd_path):
                        # Create a new RealTimeDeltas object
                        self.realtimedeltas_collection[date_time_str] = RealTimeDeltas(
                            rtd_path
                        )

    def get_surface_details_as_dataframe(self):
        """
        Returns the surface details dictionary as a dataframe item

        Parameters
        ----------
        None
        
        """

        # First, we will first have to convert each dictionary value to
        # an array with a single item
        temp_dict = {}
        for key, value in self.surface_details.items():
            temp_dict[key] = [value]

        # Finally, return the dataframe
        return pd.DataFrame.from_dict(temp_dict)

    def get_site_details_as_dataframe(self):
        """
        Returns the site details dictionary as a dataframe item

        Parameters
        ----------
        None
        
        """

        # First, we will first have to convert each dictionary value to
        # an array with a single item
        temp_dict = {}
        for key, value in self.site_details.items():
            temp_dict[key] = [value]

        # Finally, return the dataframe
        return pd.DataFrame.from_dict(temp_dict)
