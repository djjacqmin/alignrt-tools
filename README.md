# AlignRT Tools

The alignrt-tools module is a package of tools for analyzing data from [AlignRT®](http://www.visionrt.com/product/alignrt/), a video-based three-dimensional (3D) surface imaging system that is used to image the skin surface of a patient in 3D before and during radiotherapy treatment. 

# Usage
You can load your patient database by importing alignrt_tools, then creating a PatientCollection using as follows:
```
# Import AlignRT Libraries
import sys
sys.path.append('../alignrt-tools')
import alignrt_tools

# Define AlignRT data path
alignrt_pdata = './Pdata'

px_collection = alignrt_tools.PatientCollection(alignrt_pdata)
```
