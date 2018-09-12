"""
This module defines a RealTimeDeltas class. This class contains reads 
RealTimeDelta files from AlignRT and contains methods to process the 
information.

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
import pandas as pd
import numpy as np


class RealTimeDeltas:
    """The RealTimeDeltas class contains properties and methods for
    working with AlignRT RealTimeDeltas_DATE_TIME.txt records.

    ...

    Attributes
    ----------
    header_lines : int
        The number of lines in the file header for 
        RealTimeDeltas_DATE_TIME.txt records

    Instance Variables
    ------------------
    path : str
        The file path to the RealTimeDeltas_DATE_TIME.txt record
    realtimedeltas_details : dict 
        A dictionary containing the header of the 
        RealTimeDeltas_DATE_TIME.txt record

    Methods
    -------
    get_realtimedeltas_as_dataframe()
        Returns the real-time delta file as a pandas dataframe
    """

    # Current file format uses 11 header lines
    header_len = 11

    def __init__(self, path=None):
        """
        Parameters
        ----------
        path : str
            The file path to the RealTimeDeltas_DATE_TIME.txt record
        """
        self.path = path
        self.realtimedeltas_details = {}

        if path is not None:

            with open(path, "r") as rtd:
                header_lines = rtd.readlines()[0 : RealTimeDeltas.header_len]

                for line in header_lines:
                    pieces = line.split(":, ")
                    if len(pieces) > 1:
                        self.realtimedeltas_details[pieces[0]] = (
                            pieces[1].split("\n")[0].split("\x00")[0]
                        )
                    else:
                        self.realtimedeltas_details[pieces[0]] = None


            # Change Start Time and End Time to datetime objects
            self.realtimedeltas_details["Start Time"] = datetime.strptime(
                self.realtimedeltas_details["Start Time"], "%y%m%d_%H%M%S"
            )
            self.realtimedeltas_details["End Time"] = datetime.strptime(
                self.realtimedeltas_details["End Time"], "%y%m%d_%H%M%S"
            )

    def get_realtimedeltas_as_dataframe(self):
        """
        Parameters
        ----------
        None
        
        Returns
        _______
        A dataframe containing the real time delta data
        
        """
        temp_df = pd.read_csv(self.path, header=11)

        # Add a column for magnitude
        temp_df[" D.MAG (cm)"] = (
            temp_df[" D.VRT (cm)"] * temp_df[" D.VRT (cm)"]
            + temp_df[" D.LAT (cm)"] * temp_df[" D.LAT (cm)"]
            + temp_df[" D.LNG (cm)"] * temp_df[" D.LNG (cm)"]
        )
        temp_df[" D.MAG (cm)"] = temp_df[" D.MAG (cm)"].apply(np.sqrt)

        # Add a column for the Clock Time
        start_time = self.realtimedeltas_details["Start Time"]
        elapsed_time = pd.to_timedelta(temp_df["Elapsed Time (sec)"], "s")
        temp_df["Clock Time"] = start_time + elapsed_time

        return temp_df
