""" Examples demonstrating how to use alignrt_tools"""
import time
from open3d import *
import numpy as np

# Import alignrt_tools Libraries
import alignrt_tools as art

# Define a path containing alignrt data
sgrt_path = "../alignrt-playground/Sample_Directory"
# sgrt_path = 'X:\\Dustin\\OSMS\\RoomA\\PData'

# Create a patient collection using the PatientCollection class constructor
start = time.time()
pc = art.PatientCollection(sgrt_path)
end = time.time()


# Create and display a pandas dataframe of the patient collection
df = pc.get_collection_as_dataframe()

for px in pc.patients:
    print(
        "{}, {}, has {} sites".format(
            px.details["Surname"], px.details["FirstName"], len(px.sites)
        )
    )
    for sx in px.sites:
        print(" * {} has {} phases".format(sx.details["Description"], len(sx.phases)))
        for fx in sx.phases:
            print(
                "  ** {} has {} fields".format(
                    fx.details["Description"], len(fx.fields)
                )
            )
            for fl in fx.fields:
                print(
                    "   *** {} has {} surfaces".format(
                        fl.details["Description"], len(fl.surfaces)
                    )
                )
                for su in fl.surfaces:
                    print("    **** {}".format(su.surface_details["Label"]))

print(f"The PatientCollection for {sgrt_path} was created in {end - start} seconds.")


def get_first_plan(pc):

    for px in pc.patients:
        for sx in px.sites:
            for fx in sx.phases:
                if "BreR" in fx.details["Description"]:
                    return px


def get_first_surface(px):

    for sx in px.sites:
        for phx in sx.phases:
            for fx in phx.fields:
                for ux in fx.surfaces:
                    return ux.get_surface_mesh()


def mag_to_color(x):
    if x < 10:
        return (0, 0, 1)
    if x < 15:
        return (0, 1, 0)
    else:
        return (1, 0, 0)


first_px = get_first_plan(pc)

ply = get_first_surface(first_px)
ply.compute_vertex_normals()
origin = create_mesh_coordinate_frame(size=100, origin=[0, 0, 0])
# open3d.draw_geometries([ply, origin])

pcd = PointCloud()
pcd2 = PointCloud()
pcd.points = ply.vertices
xyz = np.asarray(pcd.points) + 10
pcd2.points = Vector3dVector(xyz)
# open3d.draw_geometries([pcd, pcd2])
start = time.time()
diff = compute_point_cloud_to_point_cloud_distance(pcd2, pcd)
end = time.time()

print(f"The difference calculation was computed in {end - start} seconds.")
print(f"The min and max differences are {min(diff)} and {max(diff)}")

ply.vertex_colors = Vector3dVector(np.array(list(map(mag_to_color, diff))))

draw_geometries([ply, pcd2, origin], width=1080, height=640)
