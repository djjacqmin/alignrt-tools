""" Examples demonstrating how to use alignrt_tools"""
import time

# Import alignrt_tools Libraries
import alignrt_tools as art

# Define a path containing alignrt data
# sgrt_path = '../alignrt-playground/Sample_Directory'
sgrt_path = 'X:\\Dustin\\OSMS\\RoomD\\PData'

# Create a patient collection using the PatientCollection class constructor
start = time.time()
pc = art.PatientCollection(sgrt_path)
end = time.time()


# Create and display a pandas dataframe of the patient collection
df = pc.get_collection_as_dataframe()

for px in pc.patients:
    print("{}, {}, has {} sites".format(
        px.details['Surname'], px.details['FirstName'], len(px.sites)))
    for sx in px.sites:
        print(
            " * {} has {} phases".format(sx.details['Description'], len(sx.phases)))
        for fx in sx.phases:
            print(
                "  ** {} has {} fields".format(fx.details['Description'], len(fx.fields)))
            for fl in fx.fields:
                print(
                    "   *** {} has {} surfaces".format(fl.details['Description'], len(fl.surfaces)))
                for su in fl.surfaces:
                    print(
                        "    **** {}".format(su.surface_details['Label']))

print(end - start)


def get_first_plan(pc):

    for px in pc.patients:
        for sx in px.sites:
            for fx in sx.phases:
                if "SRS_" in fx.details['Description']:
                    return px


first_px = get_first_plan(pc)
print(first_px)
