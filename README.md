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

# Security Concerns

The alignrt-tools module is designed to allow users to load and view their AlignRT data for quality assurance and process improvement activities. This data may be sensitive and require special considerations to ensure HIPAA compliance. The end user is entirely liable for ensuring the security of their patient data.