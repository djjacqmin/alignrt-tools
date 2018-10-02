"""
This module defines the TreatmentCalendar, TreatmentDay and 
TreatmentSession classes.

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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class TreatmentCalendar:
    """ The TreatmentCalendar organizes a patient's treatment history 
    into a collection of individual fractions.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    None

    """

    def __init__(self, df):
        """
        Instantiates a TreatmentCalendar object using a Pandas dataframe that includes the patient's full history of real-time deltas. 

        Parameters
        ----------
        df : Pandas DataFrame
            A DataFrame containing the real-time deltas for this patient
        """

        # A TreatmentCalendar is a collection of TreatmentDay objects.
        # Let's create an empty array for the treatment days.
        self.treatment_days = []

        # Check to see if the df is None
        if df is not None:
            # Create a new row in the DataFrame called "Date" from "DateTime"
            df['Date'] = df['Clock Time'].apply(pd.datetime.date)

            for day in df['Date'].unique():
                # Create a TreatmentDay using the subset of the DataFrame
                # that includes the date
                self.treatment_days.append(
                    TreatmentDay(df[df['Date'] == day]))


class TreatmentDay:
    """ The TreatmentDay organizes a single day of real-time delta 
    data into TreatmentSessions objects. The class also contains methods
    for analyzing the constituent data.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    None

    """

    def __init__(self, df):
        """
        Instantiates a TreatmentDay object using a Pandas dataframe that includes the patient's real-time deltas for one day. 

        Parameters
        ----------
        df : Pandas DataFrame
            A DataFrame containing the real-time deltas for this day of
            treatment
        """

        # A TreatmentDay is a collection of TreatmentSession objects.
        # Let's create an empty array for the treatment sessions.
        self.treatment_sessions = []

        # Check to see if the df is None
        if df is not None:

            # FUTURE UPDATE
            # For now, we will assume a day and a session are the same
            # (i.e we will not yet acknowledge BID treatments, or
            # treatments that are interrupted and completed later in
            # day). This functionality will be added later.

            self.treatment_sessions.append(TreatmentSession(df))


class TreatmentSession:
    """ The TreatmentSession holds a single treatment session
    of real-time delta data, and contains methods to analyze 
    the real-time delta data in the session.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    None

    """

    def __init__(self, df):
        """
        Instantiates a TreatmentSession object using a Pandas dataframe that includes the patient's real-time deltas for one treatment session. 

        Parameters
        ----------
        df : Pandas DataFrame
            A DataFrame containing the real-time deltas for this
            session of treatment
        """

        self._df = df

    def get_treatment_session_as_dataframe(self):
        """
        Returns a DataFrame containing the treatment session data

        Parameters
        ----------
        None

        Returns
        -------
        The pandas DataFrame that was used to create this treatment 
        session

        """

        return self._df

    def get_translations_plot(self):
        pass

    def get_rotations_plot(self):
        pass

    def get_beam_on_histogram(self):
        pass

    def get_position_cdf(self):
        pass
