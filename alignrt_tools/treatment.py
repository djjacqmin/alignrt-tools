"""Classes for organizing AlignRT data into a calendar of fractions"""

from math import ceil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class TreatmentCalendar:
    """AlignRT treatment data organized into a calendar

    The TreatmentCalendar organizes a patient's treatment history
    into a collection of individual treatment days.

    Note
    ----
    The get_treatment_calendar() method of the Patient class is the most
    convenient way to obtain a TreatmentCalendar because it also
    obtains the real-time deltas DataFrame needed to instantiate the
    object.

    Parameters
    ----------
     df : DataFrame
        A pandas DataFrame containing the patient's full history of
        real-time deltas

    Attributes
    ----------
    treatment_days : list of TreatmentDay
        A list of TreatmentDay objects, which collectively constitute
        the treatment calendar

    """

    def __init__(self, df):
        # A TreatmentCalendar is a collection of TreatmentDay objects.
        # Let's create an empty array for the treatment days.
        self.treatment_days = []

        # Check to see if the df is None
        if df is not None:
            # Create a new row in the DataFrame called "Date" from "DateTime"
            df["Date"] = df["Clock Time"].apply(datetime.date)

            for day in df["Date"].unique():
                # Create a TreatmentDay using the subset of the DataFrame
                # that includes the date
                self.treatment_days.append(TreatmentDay(df[df["Date"] == day]))

            # Sort the days
            self.treatment_days.sort(key=lambda td: td.treatment_date)

    def get_treatment_day_by_date(self, tx_date):
        """Returns a TreatmentDay object with the same tx_date, if
        present

        Parameters
        ----------
        tx_date: datetime.date
            The date of the TreatmentDay object being requested

        Returns
        -------
        A TreatmentDay object with the requested date, or None if the
        the date is not found

        """
        if not isinstance(tx_date, datetime.date):
            raise TypeError("tx_date must be of type datetime.date")

        for td in self.treatment_days:
            if td.treatment_date == tx_date:
                return td

        return None


class TreatmentDay:
    """AlignRT treatment data from one calendar day of treatment

    A TreatmentDay organizes a patient's treatment history into a
    collection of individual treatment fractions. For most patients,
    there is one fraction per day, so this class may seem redundant.
    However, some patients are treated twice per day (BID), and the
    inclusion of separate TreatmentDay and TreatmentSession objects
    is designed to account for this scenario. At this time, this class
    does not correctly account for BID treatments, but will be modified
    to do so in the future.

    Note
    ----
    The constructor for this class is called during the instantiation of
    the TreatmentCalendar class, and will rarely be called outside of
    this context.

    Parameters
    ----------
     df : DataFrame
            A pandas DataFrame containing the real-time deltas for one
            calendar day of treatment

    Attributes
    ----------
    treatment_date : date
        The date of treatment
    treatment_sessions : list of TreatmentSession
        A list of TreatmentSession object, which collectively
        constitute the treatment day
    """

    def __init__(self, df):
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
            self.treatment_date = df["Clock Time"].min().date()

            # Sort the treatment sessions by time
            self.treatment_sessions.sort(key=lambda ts: ts.treatment_time)


class TreatmentSession:
    """AlignRT treatment data from one treatment session

    A TreatmentSession contains data for a single treatment fraction.

    Note
    ----
    The constructor for this class is called during the instantiation of
    the TreatmentDay class, and will rarely be called outside of this
    context.

    Parameters
    ----------
     df : DataFrame
            A pandas DataFrame containing the real-time deltas for one
            fraction of treatment

    Attributes
    ----------
    treatment_time : datetime.datetime
        The date and time when the treatment session began, which
        corresonds to the moment when the AlignRT cameras were turned on

     """

    def __init__(self, df):

        # Check to see if the df is None
        if df is not None:

            self.treatment_time = df["Clock Time"].min()

            # First, set the "Clock Time" to the index and sort by index
            df = df.set_index("Clock Time")
            df = df.sort_index()

            # Next, let's add a new column called "True Elapsed Time (min)"
            df["True Elapsed Time (min)"] = (
                (df.index - df.index.min()).microseconds / 1000000
                + (df.index - df.index.min()).seconds
            ) / 60

            self._df = df

    def get_treatment_session_as_dataframe(self):
        """Get a DataFrame containing the treatment session data

        Returns
        -------
        DataFrame
            The pandas DataFrame that was used to create this treatment
            session

        """

        return self._df

    def get_translations_and_rotations_plot(self):
        """Get a plot of tranlations and rotations

        Returns matplotlib figure, axes tuple that contains a plot of
        the real-time delta translations and rotations for this session.

        Returns
        -------
        fig : Figure
            A matplotlib.pylot figure
        axes : Axes
            A matplotlib.pylot axes that contains plots of the real-time
            delta translations and rotations for this session

        """

        # Create a figure with two rows and one column
        fig, axs = plt.subplots(2, 1, figsize=[12, 6])

        # Grab a subset of the dataframe that exludes the 999 values
        # that are used when the patient is not found
        dfplot = self._df[self._df[" D.MAG (cm)"] < 999.0]

        # Create a subset of dfplot that includes only beam-on time
        dfbo = dfplot[dfplot[" XRayState"] == 1]

        # Set plot parameters
        lw = 0.5  # line width for raw data
        lw_rw = 2  # line width for rolling average data
        alp = 0.3  # alpha for raw data
        alp_rw = 1  # alpha for rolling average data
        rw = 20  # rolling window width

        # Plot the raw VRT and the VRT rolling average
        axs[0].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.VRT (cm)"],
            color="#5654F7",
            linewidth=lw,
            alpha=alp,
            label="_nolegend_",
        )
        axs[0].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.VRT (cm)"].rolling(rw, center=True).mean(),
            color="#5654F7",
            linewidth=lw_rw,
            alpha=alp_rw,
            label="Vertical",
        )

        # Plot the raw LNG and the LNG rolling average
        axs[0].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.LNG (cm)"],
            color="#CF161E",
            linewidth=lw,
            alpha=alp,
            label="_nolegend_",
        )
        axs[0].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.LNG (cm)"].rolling(rw, center=True).mean(),
            color="#CF161E",
            linewidth=lw_rw,
            alpha=alp_rw,
            label="Longitudinal",
        )

        # Plot the raw LAT and the LAT rolling average
        axs[0].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.LAT (cm)"],
            color="#41bf71",
            linewidth=lw,
            alpha=alp,
            label="_nolegend_",
        )
        axs[0].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.LAT (cm)"].rolling(rw, center=True).mean(),
            color="#41bf71",
            linewidth=lw_rw,
            alpha=alp_rw,
            label="Lateral",
        )

        # Plot the raw MAG and the MAG rolling average
        axs[0].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.MAG (cm)"],
            color="#000000",
            linewidth=lw,
            alpha=alp,
            label="_nolegend_",
        )
        axs[0].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.MAG (cm)"].rolling(rw, center=True).mean(),
            color="#000000",
            linewidth=lw_rw,
            alpha=alp_rw,
            label="Magnitude",
        )

        # Add beam-on time
        axs[0].fill_between(
            dfplot["True Elapsed Time (min)"],
            -10 * np.ones(len(dfplot)),
            20 * dfplot[" XRayState"] - 10,
            color="r",
            alpha=0.4,
        )

        # Add labels for the first plot
        axs[0].set_xlabel("Time (min)")
        axs[0].set_ylabel("Real-time Position (cm)")

        # Set x axis limits
        axs[0].set_xlim(0, ceil(dfbo["True Elapsed Time (min)"].max()) + 0.2)

        # Determine maximum magnitude during beam-on time
        max_beam_on_mag = dfbo[" D.MAG (cm)"].max()

        # Set y axis limits
        axs[0].set_ylim(-1.5 * max_beam_on_mag, 1.5 * max_beam_on_mag)
        axs[0].legend(ncol=4)

        # Plot the raw Rtn and the Rtn rolling average
        axs[1].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.Rtn (deg)"],
            color="#5654F7",
            linewidth=lw,
            alpha=alp,
            label="_nolegend_",
        )
        axs[1].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.Rtn (deg)"].rolling(rw, center=True).mean(),
            color="#5654F7",
            linewidth=lw_rw,
            alpha=alp_rw,
            label="Rotation",
        )

        # Plot the raw Roll and the Roll rolling average
        axs[1].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.Roll (deg)"],
            color="#CF161E",
            linewidth=lw,
            alpha=alp,
            label="_nolegend_",
        )
        axs[1].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.Roll (deg)"].rolling(rw, center=True).mean(),
            color="#CF161E",
            linewidth=lw_rw,
            alpha=alp_rw,
            label="Roll",
        )

        # Plot the raw Pitch and the Pitch rolling average
        axs[1].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.Pitch (deg)"],
            color="#41bf71",
            linewidth=lw,
            alpha=alp,
            label="_nolegend_",
        )
        axs[1].plot(
            dfplot["True Elapsed Time (min)"],
            dfplot[" D.Pitch (deg)"].rolling(rw, center=True).mean(),
            color="#41bf71",
            linewidth=lw_rw,
            alpha=alp_rw,
            label="Pitch",
        )

        # Add beam-on time
        axs[1].fill_between(
            dfplot["True Elapsed Time (min)"],
            -10 * np.ones(len(dfplot)),
            20 * dfplot[" XRayState"] - 10,
            color="r",
            alpha=0.4,
        )

        # Add labels for the second plot
        axs[1].set_xlabel("Time (min)")
        axs[1].set_ylabel("Real-time Rotation (deg)")

        # Set x axis limits
        axs[1].set_xlim(0, ceil(dfbo["True Elapsed Time (min)"].max()) + 0.2)

        # Determine maximum absolute pitch, roll or rotation:
        max_of_all = (
            np.abs(dfbo[[" D.Rtn (deg)", " D.Pitch (deg)", " D.Roll (deg)"]])
            .max()
            .max()
        )

        # Set y axis limits
        axs[1].set_ylim(-1.5 * max_of_all, 1.5 * max_of_all)

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
