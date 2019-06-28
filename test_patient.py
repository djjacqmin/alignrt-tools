from alignrt_tools.patient import get_patient_list
import time


def test_get_patient_list():
    # Define AlignRT data path
    alignrt_pdata = [
        "/Volumes/Physics/Dustin/OSMS/RoomA/PData",
        "/Volumes/Physics/Dustin/OSMS/RoomD/PData",
        "/Volumes/Physics/Dustin/OSMS/EastClinic/PData",
    ]

    start = time.time()
    px_list = get_patient_list(alignrt_pdata)
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    test_get_patient_list()
