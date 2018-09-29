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
import pandas as pd
import numpy as np


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
            determines whether the real-time deltas are loaded into a dataframe during initialization (default is False)
        """
        self.path = path
        self.surface_details = {}
        self.site_details = {}

        # To reduce memory overhead and loading time, we will only
        # load a surface mesh and realtimedelta dataframe when requested
        self.surface_mesh = None
        self.realtimedeltas = None

        if path is not None:

            # Read capture.ini and convert to dictionary
            with open(
                "{0}/capture.ini".format(path), "r", encoding="latin-1"
            ) as capt_ini:
                try:
                    for line in capt_ini:

                        pieces = line.split("=")
                        if len(pieces) > 1:
                            self.surface_details[pieces[0]] = pieces[1].split("\n")[
                                0]
                        else:
                            self.surface_details[pieces[0]] = None
                except UnicodeDecodeError:
                    print(
                        "Parsing {} resulted in unicode error".format(
                            "{0}/capture.ini".format(path)
                        )
                    )

            # Read site.ini and convert to dictionary
            with open("{0}/site.ini".format(path), "r", encoding="latin-1") as site_ini:
                try:
                    for line in site_ini:
                        pieces = line.split("=")
                        if len(pieces) > 1:
                            self.site_details[pieces[0]] = pieces[1].split("\n")[
                                0]
                        else:
                            self.site_details[pieces[0]] = None

                    # In site.ini, the Phase and Field have surrounding quotes that get included in the dictionary values. This can complicate the matching process. Let's remove them
                    self.site_details['Phase'] = self.site_details['Phase'][1:-1]
                    self.site_details['Field'] = self.site_details['Field'][1:-1]

                except UnicodeDecodeError:
                    print(
                        "Parsing {} resulted in Unicode decode error".format(
                            "{0}/site.ini".format(path)
                        )
                    )

            if load_rtds:
                self._load_rtds_as_dataframe()

    def get_surface_details_as_dataframe(self):
        """
        Returns the surface details dictionary as a dataframe item

        Parameters
        ----------
        None

        Returns
        -------
        A dataframe containing the surface details for this surface

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

        Returns
        -------
        A dataframe containing the site details for this field

        """

        # First, we will first have to convert each dictionary value to
        # an array with a single item
        temp_dict = {}
        for key, value in self.site_details.items():
            temp_dict[key] = [value]

        # Finally, return the dataframe
        return pd.DataFrame.from_dict(temp_dict)

    def get_realtimedeltas_as_dataframe(self):
        """
        Returns the real time deltas as a dataframe

        Parameters
        ----------
        None

        Returns
        -------
        A dataframe containing all of the real-time deltas for this surface

        """

        # If the dataframe does not exist, create it
        if self.realtimedeltas is None:
            self._load_rtds_as_dataframe()

        # After _load_rtds_as_dataframe(), the realtimedeltas may
        # still be None if this surface does not have real-time deltas
        if self.realtimedeltas is not None:
            # Append the site details and surface details
            for key, value in self.site_details.items():
                super_key = 'site.ini details - ' + key
                self.realtimedeltas[super_key] = value
            for key, value in self.surface_details.items():
                super_key = 'Surface Details - ' + key
                self.realtimedeltas[super_key] = value

        return self.realtimedeltas

    def _load_rtds_as_dataframe(self):

            # Verify that the collection is empty
        if self.realtimedeltas is None:

            # Set df to None
            df = None

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

                    # Determine if the file exists
                    if os.path.isfile(rtd_path):

                        # Read the real-time deltas header
                        rtd_details = {}
                        with open(rtd_path, "r") as rtd:
                            header_lines = rtd.readlines()[0:11]

                            for line in header_lines:
                                pieces = line.split(":, ")
                                if len(pieces) > 1:
                                    rtd_details[pieces[0]] = (
                                        pieces[1].split(
                                            "\n")[0].split("\x00")[0]
                                    )
                                else:
                                    rtd_details[pieces[0]] = None

                        # Change Start Time and End Time to datetime objects
                        rtd_details["Start Time"] = datetime.strptime(
                            rtd_details["Start Time"], "%y%m%d_%H%M%S"
                        )
                        rtd_details["End Time"] = datetime.strptime(
                            rtd_details["End Time"], "%y%m%d_%H%M%S"
                        )

                        # Next, open the rest of a the file as a dataframe
                        temp_df = pd.read_csv(rtd_path, header=11)

                        # Some early patient may have deltas in mm. Convert to cm.
                        if " D.VRT (mm)" in temp_df:
                            temp_df[" D.VRT (cm)"] = temp_df[" D.VRT (mm)"] / 10.0
                        if " D.LAT (mm)" in temp_df:
                            temp_df[" D.LAT (cm)"] = temp_df[" D.LAT (mm)"] / 10.0
                        if " D.VRT (mm)" in temp_df:
                            temp_df[" D.LNG (cm)"] = temp_df[" D.LNG (mm)"] / 10.0

                        # Add a column for magnitude

                        temp_df[" D.MAG (cm)"] = (
                            temp_df[" D.VRT (cm)"] * temp_df[" D.VRT (cm)"]
                            + temp_df[" D.LAT (cm)"] * temp_df[" D.LAT (cm)"]
                            + temp_df[" D.LNG (cm)"] * temp_df[" D.LNG (cm)"]
                        )
                        temp_df[" D.MAG (cm)"] = temp_df[" D.MAG (cm)"].apply(
                            np.sqrt)

                        # Add a column for the Clock Time
                        start_time = rtd_details["Start Time"]
                        elapsed_time = pd.to_timedelta(
                            temp_df["Elapsed Time (sec)"], "s")
                        temp_df["Clock Time"] = start_time + elapsed_time

                        # Add the rtd_details to the dataframe
                        for key, value in rtd_details.items():
                            temp_df[key] = value

                        # Append values to the real time deltas dataframe
                        if df is None:
                            df = temp_df
                        else:
                            df = df.append(temp_df, ignore_index=True)

            self.realtimedeltas = df
