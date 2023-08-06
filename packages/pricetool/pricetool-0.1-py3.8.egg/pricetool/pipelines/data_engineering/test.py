from builtins import dict, str
from typing import Any, Dict, List

from pathlib import Path, PurePath
import pathlib
from kedro.extras.datasets.pandas import ParquetDataSet
import pandas as pd
import platform
import os


# def nodeName(PMLPeriod: str, source_database: str, server: str) -> Dict[str, Any]:
#     PMLPeriod = '20200102'
#     source_database ='49547_GPR_Tabular_4'
#     server='tst-sql-0585'


#     pq_file = f"Contracts_File_{server}_{source_database}_{str(PMLPeriod)}"

#     contractFileName = dict(namefile = pq_file)

#     print(contractFileName)
#     return contractFileName


# #nodeName('20200102', '49547_GPR_Tabular_4', 'tst-sql-0585')


# nName = nodeName('20200102', '49547_GPR_Tabular_4', 'tst-sql-0585')

# data_file_name = nName['namefile']+ "_Terms"
# print(data_file_name)

# data_folder = Path("C:\\workspace\\pricetool\\price-traget-tool\\data\\Cube_Data")

# file_to_read = str(data_folder/data_file_name)
# #print(file_to_read)
# #ds = pq.ParquetDataset(file_to_read)
# #tab = ds.read().to_pandas()

# print(file_to_read)

# data_set = ParquetDataSet(filepath=file_to_read)
# data_set.load()


print("lets start")


def return_path(fname: str, period: str, path_loc_win: str, path_loc_linux: str = None):

    # fname = 'All_Contracts_loss_area_evtsource'
    # period='20200102'
    # path_loc_win='C://workspace//pricetool//price-traget-tool//data//01_raw'

    if platform.system() == "Windows":
        # data_f = Path("//sirius.local/data/Group/GPI Reporting/Capital cost project/Cube_Data/")
        data_f = Path(path_loc_win)
        print(data_f)
    else:
        # data_f = Path("/data/Cube_Data/")
        data_f = Path(path_loc_linux)

    path_file_period = os.path.join(data_f, f"{fname}_{period}")
    #ppp = Path(path_file_period)
    #print(type(ppp))
    # return path_file_period
    print("no error")
    return path_file_period


fname = "All_Contracts_loss_area_evtsource"
period = "20200102"
path_loc_win = "C://workspace//pricetool//price-traget-tool//data//02_intermediate"

returnpath1 = return_path(fname, period, path_loc_win)

#returnpath1
# return_path('All_Contracts_loss_area_evtsource', '20200102', 'C://workspace//pricetool//price-traget-tool//data//01_raw')


# def calc():
#     y = return_path('All_Contracts_loss_area_evtsource', '20200102', 'C://workspace//pricetool//price-traget-tool//data//01_raw')
#     print(y)

# calc()

#if isinstance(returnpath1, pathlib.PurePath):
if os.path.exists(returnpath1):
    print("hi")
else:
    print("noooooooooooo")
