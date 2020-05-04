import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append("../alignrt-tools")
import alignrt_tools
import datetime
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)


pdata = [
    r"\\uwhis.hosp.wisc.edu\UNC1\RadOnc\AlignRT\PData",
    r"\\uwhis.hosp.wisc.edu\UNC1\RadOnc\AlignRT\PData\Legacy Room D",
]

pdata = [
    r"\\uwhis.hosp.wisc.edu\UNC1\RadOnc\AlignRT\PData",
]

px_col = alignrt_tools.PatientCollection(pdata)
logging.debug(f"There are {px_col.get_num_patients()} total patients")

srs_col = px_col.get_filtered_patient_collection(
    phase_filter="_SRS_", include_numerical_patient_id_only=True
)

logging.debug(f"There are {srs_col.get_num_patients()} SRS patients")

df_beam_on = None

for px in srs_col.patients:
    logging.debug(f"Analyzing {px.details['PatientID']}")
    tc = px.get_treatment_calendar()
    if tc is not None:
        for td in tc.treatment_days:
            for ts in td.treatment_sessions:
                df = ts.get_treatment_session_as_dataframe()
                logging.debug(f"df has a size of {len(df)}")
                dfb = df[(df[" XRayState"] == 1) & (df[" D.MAG (cm)"] < 999)]
                logging.debug(f"dfb has a size of {len(dfb)}")
                if df_beam_on is None:
                    df_beam_on = dfb
                else:
                    df_beam_on = df_beam_on.append(dfb, ignore_index=True)
                    logging.debug(f"df_beam_on has a size of {len(df_beam_on)}")

fig, ax = plt.subplots()
ax = sns.distplot(
    df_beam_on[" D.MAG (cm)"],
    color="black",
    bins=30,
    hist_kws=dict(cumulative=True),
    kde_kws=dict(cumulative=True),
)
ax.set(xlabel="Magnitude of Deviation (cm)", ylabel="CDF")

plt.savefig("Magnitude.png")

fig, ax = plt.subplots()

bins = 45

ax = sns.distplot(
    df_beam_on[" D.Rtn (deg)"],
    bins=bins,
    color="Blue",
    label="Rotation",
    hist_kws={"cumulative": False, "alpha": 0.15},
    kde_kws=dict(cumulative=False),
)

ax = sns.distplot(
    df_beam_on[" D.Roll (deg)"],
    bins=bins,
    color="Red",
    label="Roll",
    hist_kws={"cumulative": False, "alpha": 0.15},
    kde_kws=dict(cumulative=False),
)

ax = sns.distplot(
    df_beam_on[" D.Pitch (deg)"],
    bins=bins,
    color="Green",
    label="Pitch",
    hist_kws={"cumulative": False, "alpha": 0.15},
    kde_kws=dict(cumulative=False),
)

ax.set(xlabel="Rotational Deviation (deg)", ylabel="Relative Probability")

fig.set_size_inches([8, 8])

plt.legend()
plt.savefig("Rotations.png")


fig, ax = plt.subplots()

ax = sns.distplot(
    df_beam_on[" D.VRT (cm)"],
    color="Blue",
    label="Vertical",
    hist_kws={"cumulative": False, "alpha": 0.15},
    kde_kws=dict(cumulative=False),
)

ax = sns.distplot(
    df_beam_on[" D.LNG (cm)"],
    color="Red",
    label="Longitudinal",
    hist_kws={"cumulative": False, "alpha": 0.15},
    kde_kws=dict(cumulative=False),
)

ax = sns.distplot(
    df_beam_on[" D.LAT (cm)"],
    color="Green",
    label="Lateral",
    hist_kws={"cumulative": False, "alpha": 0.15},
    kde_kws=dict(cumulative=False),
)


ax.set(xlabel="Translational Deviation (cm)", ylabel="Relative Probability")

plt.legend()

fig.set_size_inches([8, 8])

plt.savefig("Translations.png")
