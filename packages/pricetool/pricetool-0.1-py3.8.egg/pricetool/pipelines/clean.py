from typing import Any, Dict, List
from kedro.extras.datasets.pandas import ParquetDataSet

# from kedro.io import ParquetLocalDataSet
import pandas as pd
from builtins import dict, str
import six
from pathlib import Path, PurePosixPath
from kedro.io import AbstractDataSet

# _dict = {
#   "server": "tst-sql-0585",
#   "source_database": "49547_GPR_Tabular_4",
#   "PMLPeriod": "20200102"}

# """Bulding a parquet file formate from the dictionary with keys:server, source_database,PMLPeriod """
# def fileNameCreator (_dict):
#     PREFIX = "Contracts_File_"
#     lst = []

#     for key in six.iterkeys(_dict):
#         value = _dict[key]
#         lst.append(value)

#     pq_file = PREFIX + '_'.join(i for i in lst) + '_Terms'
#     #print(pq_file)
#     print (pq_file)

#     return dict(name=pq_file)


# fileNameCreator(_dict)


PMLPeriod = "20200102"
source_database = "49547_GPR_Tabular_4"
server = "tst-sql-0585"


def nodeName(PMLPeriod: str, source_database: str, server: str) -> Dict[str, Any]:
    pq_file = f"Contracts_File_{server}_{source_database}_{str(PMLPeriod)}"
    print(pq_file)
    # return (dict(name=pq_file))
    return dict(testfile=pq_file)


def Get_dimBusiness_Extended(nodeName) -> Dict[str, Any]:
    xxx = nodeName(PMLPeriod, source_database, server)
    # print(xxx)
    data_file_name = xxx["testfile"] + "_Terms"
    # print(data_file_name)
    print(dict(xyz=data_file_name))
    return dict(xyz=data_file_name)


# print(xxx)
# print(xxx['namefile'])
# print(data_file_name)
Get_dimBusiness_Extended(nodeName)
