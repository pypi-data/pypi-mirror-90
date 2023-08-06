from typing import Any, Dict, List
from kedro.extras.datasets.pandas import ParquetDataSet

# from kedro.io import ParquetLocalDataSet
import pandas as pd
from builtins import dict, str
import six


# _dict = {
#   "server": "tst-sql-0585",
#   "source_database": "49547_GPR_Tabular_4",
#   "PMLPeriod": "20200102"}

# # """Bulding a parquet file formate from the dictionary with keys:server, source_database,PMLPeriod """


# def load_pq():

#     data_set = ParquetDataSet(filepath="C:\\workspace\\pricetool\\price-traget-tool\\data\\01_raw\\test.parquet")
#     data_set.save("C:\\workspace\\pricetool\\price-traget-tool\\data\\01_raw\\some.parquet")
#     reloaded = data_set.load()


#     # data_set = ParquetDataSet(filepath="C:\\workspace\\pricetool\\price-traget-tool\\data\\01_raw\\some.parquet")
#     # reloaded = data_set.load()
#     # return reloaded

# def fileNameCreator (_dict) -> List[str]:
#     PREFIX = "Contracts_File_"
#     lst = []

#     for key in six.iterkeys(_dict):
#         value = _dict[key]
#         lst.append(value)

#     pq_file = PREFIX + '_'.join(i for i in lst) + '_Terms'
#     #print(pq_file)
#     return [pq_file]


def fileName111(PMLPeriod: str, source_database: str, server: str):
    # if str(PMLPeriod) == '20200102':
    #     self.source_database = '49547_GPR_Tabular_4'
    #     self.server ='tst-sql-0585'

    # if str(PMLPeriod) == '20191003':
    #     self.source_database = 'GPR_Tabular_3'
    #     self.server = 'tst-sql-0285'

    # self.PMLPeriod = PMLPeriod
    return dict(
        pq_file=f"Contracts_File_{server}_{source_database}_{str(PMLPeriod)}".replace(
            ",", "_"
        )
    )
    # return dict(pq_file)
