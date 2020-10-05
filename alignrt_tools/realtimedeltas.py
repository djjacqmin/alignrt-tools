"""
This module is under development. It contains code to open and analyze AlignRT
Advance real-time delta files.

Copyright (C) 2020, Dustin Jacqmin, PhD

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Import helpful libraries
import typing
import pathlib
import pandas as pd
import logging

# import dateutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def convert_realtimedelta_file_to_dataframe(
    rtd_filename: typing.Union[str, pathlib.Path]
) -> pd.DataFrame:
    """Takes an AlignRT Advance real-time delta file and returns a dataframe.

    """

    if isinstance(rtd_filename, str):
        rtd_filename = pathlib.Path(rtd_filename)
        logger.debug(f"{rtd_filename} was converted from str to Path object")

    assert rtd_filename.is_file(), f"{str(rtd_filename)} is not a file"

    df = pd.read_csv(rtd_filename)

    # Process strings to datetimes
    format_str = "%d-%m-%y %I:%M:%S.%f %p"
    df["Date Time (ms)"] = pd.to_datetime(df["Date Time (ms)"], format=format_str)

    # Convert columns to category data type to reduce memory usage.
    df["Patient ID(GUID)"] = df["Patient ID(GUID)"].astype("category")

    return df
