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

from math import ceil
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

            # Sort the days
            self.treatment_days.sort(key=lambda td: td.treatment_date)


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
            self.treatment_date = df['Clock Time'].min().date()

            # Sort the treatment sessions by time
            self.treatment_sessions.sort(key=lambda ts: ts.treatment_time)


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

        # Check to see if the df is None
        if df is not None:

            self.treatment_time = df['Clock Time'].min().time()

            # First, set the "Clock Time" to the index and sort by index
            df = df.set_index('Clock Time')
            df = df.sort_index()

            # Next, let's add a new column called "True Elapsed Time (min)"
            df['True Elapsed Time (min)'] = (
                (df.index - df.index.min()).microseconds/1000000 + (df.index - df.index.min()).seconds)/60

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

    def get_translations_and_rotations_plot(self):
        """
        Returns matplotlib figure, axes tuple that contains a plot of
        the real-time delta translations and rotations for this session

        Parameters
        ----------
        None

        Returns
        -------
        A matplotlib figure, axes tuple that contains a plot of
        the real-time delta translations and rotations for this session

        """

        # Create a figure with two rows and one column
        fig, axs = plt.subplots(2, 1, figsize=[12, 6])

        # Grab a subset of the dataframe that exludes the 999 values
        # that are used when the patient is not found
        dfplot = self._df[self._df[" D.MAG (cm)"] < 999.0]

        # Create a subset of dfplot that includes only beam-on time
        dfbo = dfplot[dfplot[' XRayState'] == 1]

        # Set plot parameters
        lw = 0.5    # line width for raw data
        lw_rw = 2   # line width for rolling average data
        alp = 0.3   # alpha for raw data
        alp_rw = 1  # alpha for rolling average data
        rw = 20     # rolling window width

        # Plot the raw VRT and the VRT rolling average
        axs[0].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.VRT (cm)'],
                    color="#5654F7",
                    linewidth=lw,
                    alpha=alp,
                    label='_nolegend_')
        axs[0].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.VRT (cm)'].rolling(rw, center=True).mean(),
                    color="#5654F7",
                    linewidth=lw_rw,
                    alpha=alp_rw,
                    label='Vertical')

        # Plot the raw LNG and the LNG rolling average
        axs[0].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.LNG (cm)'],
                    color="#CF161E",
                    linewidth=lw,
                    alpha=alp,
                    label='_nolegend_')
        axs[0].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.LNG (cm)'].rolling(rw, center=True).mean(), color="#CF161E",
                    linewidth=lw_rw,
                    alpha=alp_rw,
                    label='Longitudinal')

        # Plot the raw LAT and the LAT rolling average
        axs[0].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.LAT (cm)'],
                    color="#41bf71",
                    linewidth=lw,
                    alpha=alp,
                    label='_nolegend_')
        axs[0].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.LAT (cm)'].rolling(rw, center=True).mean(), color="#41bf71",
                    linewidth=lw_rw,
                    alpha=alp_rw,
                    label='Lateral')

        # Plot the raw MAG and the MAG rolling average
        axs[0].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.MAG (cm)'],
                    color="#000000",
                    linewidth=lw,
                    alpha=alp,
                    label='_nolegend_')
        axs[0].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.MAG (cm)'].rolling(rw, center=True).mean(), color="#000000",
                    linewidth=lw_rw,
                    alpha=alp_rw,
                    label='Magnitude')

        # Add beam-on time
        axs[0].fill_between(dfplot['True Elapsed Time (min)'],
                            -10*np.ones(len(dfplot)),
                            20*dfplot[' XRayState']-10,
                            color='r',
                            alpha=.4)

        # Add labels for the first plot
        axs[0].set_xlabel("Time (min)")
        axs[0].set_ylabel("Real-time Position (cm)")

        # Set x axis limits
        axs[0].set_xlim(0, ceil(dfbo['True Elapsed Time (min)'].max())+0.2)

        # Determine maximum magnitude during beam-on time
        max_beam_on_mag = dfbo[" D.MAG (cm)"].max()

        # Set y axis limits
        axs[0].set_ylim(-1.5*max_beam_on_mag, 1.5*max_beam_on_mag)
        axs[0].legend(ncol=4)

        # Plot the raw Rtn and the Rtn rolling average
        axs[1].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.Rtn (deg)'],
                    color="#5654F7",
                    linewidth=lw,
                    alpha=alp,
                    label='_nolegend_')
        axs[1].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.Rtn (deg)'].rolling(rw, center=True).mean(), color="#5654F7",
                    linewidth=lw_rw,
                    alpha=alp_rw,
                    label="Rotation")

        # Plot the raw Roll and the Roll rolling average
        axs[1].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.Roll (deg)'],
                    color="#CF161E",
                    linewidth=lw,
                    alpha=alp,
                    label='_nolegend_')
        axs[1].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.Roll (deg)'].rolling(rw, center=True).mean(), color="#CF161E",
                    linewidth=lw_rw,
                    alpha=alp_rw,
                    label="Roll")

        # Plot the raw Pitch and the Pitch rolling average
        axs[1].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.Pitch (deg)'],
                    color="#41bf71",
                    linewidth=lw,
                    alpha=alp,
                    label='_nolegend_')
        axs[1].plot(dfplot['True Elapsed Time (min)'],
                    dfplot[' D.Pitch (deg)'].rolling(rw, center=True).mean(), color="#41bf71",
                    linewidth=lw_rw,
                    alpha=alp_rw,
                    label="Pitch")

        # Add beam-on time
        axs[1].fill_between(dfplot['True Elapsed Time (min)'],
                            -10*np.ones(len(dfplot)),
                            20*dfplot[' XRayState']-10,
                            color='r',
                            alpha=.4)

        # Add labels for the second plot
        axs[1].set_xlabel("Time (min)")
        axs[1].set_ylabel("Real-time Rotation (deg)")

        # Set x axis limits
        axs[1].set_xlim(0, ceil(dfbo['True Elapsed Time (min)'].max())+0.2)

        # Determine maximum absolute pitch, roll or rotation:
        max_of_all = np.abs(
            dfbo[[' D.Rtn (deg)', ' D.Pitch (deg)', ' D.Roll (deg)']]).max().max()

        # Set y axis limits
        axs[1].set_ylim(-1.5*max_of_all, 1.5*max_of_all)

        # Add the legend
        axs[1].legend(ncol=3)

        return fig, axs

    def get_translations_plot(self):
        pass

    def get_rotations_plot(self):
        pass

    def get_beam_on_histogram(self):
        pass

    def get_position_cdf(self):
        pass
