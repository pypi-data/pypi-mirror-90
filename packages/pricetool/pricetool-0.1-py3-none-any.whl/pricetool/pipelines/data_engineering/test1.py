import pandas as pd

# # df = pd.read_parquet('C:\\workspace\\cubeData\\Contracts_File_tst-sql-0285_GPR_Tabular_3_20191003_Terms\\0fe5a2ee868f4a4d8cbf7fecebb868a2.parquet')

# # #print(df.head(10))

# # print(df.columns)
# from pathlib import Path
# import pyarrow.parquet as pq

# # data_folder = Path ("C:\\workspace\\cubeData\\")
# #data_path: 'C:\\workspace\\cubeData\\'

# PMLPeriod = '20200102'
# source_database = '49547_GPR_Tabular_4'
# server = 'tst-sql-0585'
# data_path='C:\\workspace\\cubeData\\'

# def nodeName(PMLPeriod: str, source_database: str, server: str, data_folder: str, pf = None):

#     # PMLPeriod = '20200102'
#     # source_database = '49547_GPR_Tabular_4'
#     # server = 'tst-sql-0585'
#     # data_path = 'C:\\workspace\\cubeData\\'
#     pq_file = f"Contracts_File_{server}_{source_database}_{str(PMLPeriod)}"

#     data_folder_name = pq_file + "_Terms"

#     print(data_folder_name)

#     pq_file_to_read = str(Path(data_path)/data_folder_name)

#     print(pq_file_to_read)

#     ds = pq.ParquetDataset(pq_file_to_read)
#     tab = ds.read().to_pandas()

#     if pf is not None:
#         # .load() converts Pandas.ParquetDataSet into Pandas.DataFrame
#         #res = data_set[data_set.index.isin(pf)].load()
#         res = tab[tab.index.isin(pf)]
        
#     else:
#         res = tab
#     return res

#     #return (dict(name=pq_file))
#     #return dict(namefile = pq_file)
#     #contractFileName = dict(namefile = pq_file)
#     #file_to_read = dict(namefile = str(Path(data_folder) / data_file_name))
#     #print(file_to_read['namefile'])


#     # return contractFileName


# #nodeName('20200102', '49547_GPR_Tabular_4', 'tst-sql-0585', 'C:\\workspace\\cubeData\\')
# nodeName(PMLPeriod, source_database, server, data_path)


from kedro.extras.datasets.pandas import (
    CSVDataSet,
    SQLTableDataSet,
    SQLQueryDataSet,
    ParquetDataSet,
)


# ds = ParquetDataSet(filepath='C:\\workspace\\cubeData\\Contracts_File_tst-sql-0585_49547_GPR_Tabular_4_20200102_Terms\\0fe5a2ee868f4a4d8cbf7fecebb868a2.parquet')

# df = ds.load()
# print(df.head(5))

list_businessid_exclude_from_portfolio = ['ITPR405990','ITPR405991','IDPR201687',
                   'IDPR400396','ITPR228563','ITPR322837',
                   'ITPR228953','ITPR401322','ITPR400640',
                   'ITPR228201','ITPR229063','ITPR228548',
                   'ITPR228114','ITPR228115','ITPR228025',
                   'ITPR228026','ITPR228027'
]



# if 'Excl' in l:
#     print('works')
#     [i for i in ['RU', 'Office', 'Type', 'BusinessId', 'ProgramId', 'contract_id'] if l[1]==i]



# def create_portfolio(param = ['Excl', 'BusinessId']):
#     if param is not None:
#         Incls = [x for x in param if x[0] == 'Incl']
#         Excls = [x for x in param if x[0] == 'Excl']

#         print(Incls)



# create_portfolio(param = ['Excl', 'BusinessId'])


df = pd.read_parquet ('C:\\workspace\\cubeData\\Contracts_File_tst-sql-0585_49547_GPR_Tabular_4_20200102_Terms\\0fe5a2ee868f4a4d8cbf7fecebb868a2.parquet')

df.head(5)

dict_input = {'RU': 'ReportingUnit',
               'Office': 'OfficeName',
                'Type': 'TypeOfParticipation',
                'BusinessId':'BusinessId',
                'ProgramId':'ProgramId',
                'contract_id':'index'}

l = ['Excl', 'BusinessId']

fff = set(l).intersection(dict_input)
print(fff)
#print(next(iter(fff)))

col = dict_input[next(iter(fff))]
#print(type(col))
#print(df[col])

#r = df[~ df.col.isin(list_businessid_exclude_from_portfolio)]
#r = df.drop(df[df.BusinessId.isin(list_businessid_exclude_from_portfolio)].index)

#print(r)
# cols = df.columns.values
# r = pd.DataFrame(columns=cols)
# r = r.append(df[df[col].isin(list_businessid_exclude_from_portfolio)])
# print(r)
# i = r.index.unique()
# print(i.values.tolist())
# r = df
# r = r[~ r.col.isin(list_businessid_exclude_from_portfolio)]
# print(r.head(5))





# for i in xyz:
#     print(i[0][:1])
# list4 = []

# for i in list3:
#     print(i[0])

# #list(zip(s1, s2))

# [x for x in [i[0]] print('hurray') if x in l ]

# # i[0] in l:
# #     print('hurray')