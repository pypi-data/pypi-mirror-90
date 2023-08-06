import platform
from pathlib import Path, PurePosixPath


def data_f():
if path_type == PathType.WINDOWS:
    data_folder = pathlib.PureWindowsPath("//sirius.local/data/Group/GPI Reporting/Capital cost project/Cube_Data/")
    return data_folder
elif path_type == PathType.LINUX:
    data_folder = pathlib.PurePosixPath("/data/Cube_Data/"
    return data_folder
else:
    raise RuntimeError("Unknown platform") 