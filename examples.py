""" Examples demonstrating how to use alignrt_tools"""

# Import alignrt_tools Libraries
import alignrt_tools as art

# Define a path containing alignrt data
sgrt_path = '../alignrt-playground/Sample_Directory'

# Create a patient collection using the PatientCollection class constuctor
pc = art.PatientCollection(sgrt_path)

# Create and display a pandas dataframe of the patient collection
df = pc.get_collection_as_dataframe()
print(df)