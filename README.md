# AlignRT Tools

The alignrt-tools module is a package of tools for analyzing data from [AlignRT®](http://www.visionrt.com/product/alignrt/), a video-based three-dimensional (3D) surface imaging system that is used to image the skin surface of a patient in 3D before and during radiotherapy treatment.

# Usage

You can load your patient database by importing alignrt_tools, then creating a PatientCollection as follows:

```
# Import AlignRT Libraries
import sys
sys.path.append('../alignrt-tools')
import alignrt_tools as art

# Define AlignRT data path
alignrt_pdata = "/Pdata"

px_collection = art.PatientCollection(alignrt_pdata)
```

# Data Model
Once you have a PatientCollection, you can use Python to access the AlignRT data. The data is stored in a heirarchical format with the following structure:
* PatientCollection
  * Patient
    * Site
      * Phase
        * Field
          * Surface
    * TreatmentCalendar
      * TreatmentDay
        * TreatmentSession

As you can see above there are two hierarchical representations of the data within the Patient object. The first mimics the data tree used in AlignRT (Patient > Site > Phase > Field > Surface). The real-time delta information is associated with the Surface objects. This hierarchy is created first when a Patient object is first instantiated. 

The second representation of the data is created by reprocessing the data in the Patient object into a calendar-like structure (TreatmentCalendar > TreatmentDay > TreatmentSession). This representation is more natural for looking what happens during the course of a single treatment fraction or over a full course of treatment. The real-time delta information is associated with the TreatmentSession objects at the bottom of the hierarchy.

# Security Concerns

The alignrt-tools module is designed to allow users to load and view their AlignRT data for quality assurance and process improvement activities. This data may be sensitive and require special considerations to ensure HIPAA compliance. The end user is entirely liable for ensuring the security of their patient data.
