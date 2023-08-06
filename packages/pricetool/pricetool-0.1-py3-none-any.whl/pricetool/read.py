# from __future__ import absolute_import, print_function, unicode_literals
# #from builtins import dict, str
# import os
# import pandas
# import logging
# import requests
# from collections import defaultdict

# import six
# from collections import OrderedDict, Mapping, MutableSequence, Iterable
# from datetime import datetime
# import pytz
# import itertools

# #"Contracts_File_{self.server}_{self.source_database}_{str(self.PMLPeriod)}"
# #"Contracts_File_tst-sql-0285_GPR_Tabular_3_20191003_Terms"

# # def _indent(text, amount, ch=' '):
# #     s = '_'
# #     print('Contracts_File_'.join(s.join(lst)))


# def repr_dict(_dict):

#     prefix = "Contracts_File_"
#     lst = []

#     for key in six.iterkeys(_dict):
#         value = _dict[key]
#         lst.append(value)

#     pq_file = prefix + '_'.join(i for i in lst) + '_Terms'
#     print(pq_file)

# _dict = {
#   "server": "tst-sql-0585",
#   "source_database": "49547_GPR_Tabular_4",
#   "PMLPeriod": "20200102"}


# #repr_dict(_dict)


# conn = {
#   "PMLPeriod": ["20200102", "20191003"],
#   "source_database": ["49547_GPR_Tabular_4", "GPR_Tabular_3"],
#   "server": ["tst-sql-0585", "tst-sql-0285"]}

# def testIReadMapping(conn):
#     prefix = "Contracts_File_"
#     lst = []
#     for key in six.iterkeys(conn):
#         value = conn[key]
#         #print( conn[key])
#         lst.append(value)
#     for item in itertools.chain.from_iterable(lst):
#         print(item)


#     pq_file = prefix + '_'.join(i for i in lst) + '_Terms'
#     print(pq_file)

#     map(lambda line: print line, lines)

# #something = testIReadMapping(conn)

# testIReadMapping(conn)


# # class DictWatch(dict):

# #     @staticmethod
# #     def __init__():
# #         dict.__init__(self, args)

# #     def __getitem__(self, key):
# #         val = dict.__getitem__(self, key)
# #         return val


# # def testIReadMapping(conn):
# #     for key in conn:
# #         print(conn[key])

# def testIReadMapping(conn):
#     for key in conn:
#         def __getitem__(key):
#             val = dict.__getitem__(self, key)
#             return val

# conn = {
#   "PMLPeriod": "20200102",
#   "source_database": "49547_GPR_Tabular_4",
#   "server": "tst-sql-0585"}


# something = testIReadMapping(conn)


# #someshit.__getitem__()
# #DictWatch(conn)

# # def get(self, key):
# #         "Find the first value within the tree which has the key."
# #         if key in self.keys():
# #             return self[key]
# #         else:
# #             res = None
# #             for v in self.values():
# #                 # This could get weird if the actual expected returned value
# #                 # is None, especially in teh case of overlap. Any ambiguity
# #                 # would be resolved by get_path(s).
# #                 if hasattr(v, 'get'):
# #                     res = v.get(key)
# #                 if res is not None:
# #                     break
# #             return res


# # def send_request(**kwargs):
# #     res = requests.get(cbio_url, params=kwargs)
# #     csv_StringIO = StringIO(res.text)
# #     df = pandas.read_csv(csv_StringIO, sep='\t', skiprows=skiprows)
# #     return df

# # def get_genetic_profiles(study_id, profile_filter=None):
# #     data = {'cmd': 'getGeneticProfiles',
# #             'cancer_study_id': study_id}

# #     df = send_request(**data)

# #     genetic_profiles = list(df['genetic_profile_id'].values())
# #     return genetic_profiles

# # #get_genetic_profiles()


# # d = {'PMLPeriod': '20200102, 20191003',
# #  'source_database': '49547_GPR_Tabular_4, GPR_Tabular_3',
# #  'server': 'tst-sql-0585, tst-sql-0285'}

# # conn = {
# #   "PMLPeriod": ["20200102", "20191003"],
# #   "source_database": ["49547_GPR_Tabular_4", "GPR_Tabular_3"],
# #   "server": ["tst-sql-0585", "tst-sql-0285"]
# # }


# # def __getitem__(self, key):
# #     self.key = key
# #     #key = {k for k, v in d.items() for key in v.split(',')}
# #     if key not in self.keys():
# #         val = self.__class__()
# #         self.__setitem__(key, val)
# #     else:
# #         val = dict.__getitem__(self, key)
# #     return val

# # key = {k for k, v in conn.items() for key in v.split(',')}

# #d.__getitem__(key)

# # key = [k for k in conn.keys()]

# #key = conn.keys()


#     # def __setitem__(self, key, val):
#     #     dict.__setitem__(self, key, val)

from pathlib import Path, PurePath, PurePosixPath
import pandas as pd
from kedro.io import AbstractDataSet
from kedro.extras.datasets.pandas import ParquetDataSet

# class MyOwnDataSet(AbstractDataSet):
#     def __init__(self, filepath, param1, param2=True):
#         self._filepath = PurePosixPath(filepath)
#         self._param1 = param1
#         self._param2 = param2

#     def _load(self) -> pd.DataFrame:
#         return pd.read_csv(self._filepath)

# def Get_dimBusiness_Extended(self, pf = None):
#     data_file_name = self.pq_file + "_Terms"
#     file_to_read = str(data_folder / data_file_name)
#     ds = pq.ParquetDataset(file_to_read)
#     tab = ds.read().to_pandas()

#     if pf is not None:
#         res = tab[tab.index.isin(pf)]
#     else:
#         res = tab
#     return res


from kedro.extras.datasets.pandas import ParquetDataSet
import pandas as pd

data_set = ParquetDataSet(
    filepath="C:\\workspace\\pricetool\\price-traget-tool\\data\\01_raw\\some.parquet"
)

print(data_set)

reloaded = data_set.load()
print(reloaded)

# pq_file = data_set.load()

# data = pd.DataFrame({'col1': [1, 2], 'col2': [4, 5],
#                              'col3': [5, 6]})

#         # data_set = ParquetDataSet(filepath="gcs://bucket/test.parquet")
# data_set = ParquetDataSet(filepath="test.parquet")
# data_set.save(data)
# reloaded = data_set.load()
# # #assert data.equals(reloaded)
# print(reloaded)
