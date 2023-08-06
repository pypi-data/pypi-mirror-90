from typing import Any, Dict, List
import os
import os.path
import platform
#from kedro.extras.datasets.pandas import ParquetDataSet  
#from kedro.io import ParquetLocalDataSet
import pandas as pd  
from builtins import dict, str
import six
from pathlib import Path, PurePosixPath, PurePath
from kedro.io import AbstractDataSet, DataCatalog
import pyarrow.parquet as pq
#import platform
#from kedro.io import DataCatalog
from kedro.extras.datasets.pandas import (
    CSVDataSet,
    SQLTableDataSet,
    SQLQueryDataSet,
    ParquetDataSet,
)
#from utils.util import data_f


# def platform_path ():
#     if platform.system() == 'Windows':
#         data_folder = Path("C:\\workspace\\Cube_Data")
#     else:
#         data_folder = Path("/data/Cube_Data/")
#     return data_folder

# def data_f():
#     if platform.system() == 'Windows':
#         data_folder = Path("C:\\workspace\\cubeData")
#     else:
#         data_folder = Path("/data/Cube_Data/")
#     return data_folder

# _dict = {
#   "server": "tst-sql-0585",  
#   "source_database": "49547_GPR_Tabular_4",
#   "PMLPeriod": "20200102"}
  
# # """Bulding a parquet file formate from the dictionary with keys:server, source_database,PMLPeriod """



# def naiveFilePath (raw_car_data, PMLPeriod, source_database, server):
#     return raw_car_data


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





# def nodeName(PMLPeriod: str, source_database: str, server: str, data_folder: str) -> Dict[str, Any]:
    
#     pq_file = f"Contracts_File_{server}_{source_database}_{str(PMLPeriod)}"
#     #contractFileName = dict(namefile = pq_file)
#     data_file_name = pq_file + "_Terms"
#     file_to_read = dict(namefile = str(Path(data_folder) / data_file_name))
#     return file_to_read



# def fileNameCreator(_dict) -> List[str]:
#     PREFIX = "Contracts_File_"
#     lst = []

#     for key in six.iterkeys(_dict):
#         value = _dict[key]
#         lst.append(value)

#     pq_file = PREFIX+ '_'.join(i for i in lst) + '_Terms'

#     print(pq_file)

#     return pq_file



def Get_dimBusiness_Extended (PMLPeriod: str, source_database: str, server: str, data_path: str, pf = None) -> pd.DataFrame:


    pq_file = f"Contracts_File_{server}_{source_database}_{str(PMLPeriod)}"
    data_folder_name = pq_file + "_Terms"
    print(data_folder_name)
    #data_path=Path('C:\\workspace\\cubeData\\')
    data_path = Path(data_path)
    pq_file_to_read = str(data_path/data_folder_name)
    print(pq_file_to_read)

    ds = ParquetDataSet(filepath=pq_file_to_read)
    tab = ds.load()
    #ds = pq.ParquetDataset(Path(pq_file_to_read))
    #tab = ds.read().to_pandas()

    if pf is not None:
        # .load() converts Pandas.ParquetDataSet into Pandas.DataFrame
        #res = data_set[data_set.index.isin(pf)].load()
        res = tab[tab.index.isin(pf)]
        
    else:
        res = tab
    return res


def create_portfolio(param: List[str], list_businessid_exclude_from_portfolio: List[str]) -> pd.DataFrame:

    """there is bug in lin, as a workaround, hard codded the values of aruments in method Get_dimBusiness_Extended()"""

    df = Get_dimBusiness_Extended('20200102', '49547_GPR_Tabular_4', 'tst-sql-0585', 'C:\\workspace\\cubeData\\')
    #df = Get_dimBusiness_Extended()
    cols = df.columns.values

    dict_input = {'RU': 'ReportingUnit',
               'Office': 'OfficeName',
                'Type': 'TypeOfParticipation',
                'BusinessId':'BusinessId',
                'ProgramId':'ProgramId',
                'contract_id':'index'}

    fff = set(param).intersection(dict_input)
    col = dict_input[next(iter(fff))]

    r = df
    if param is not None:
        if param[0] == 'Excl':
            r = df.drop(df[df[col].isin(list_businessid_exclude_from_portfolio)].index)
        elif param[0] == 'Incl':
            r = pd.DataFrame(columns=cols)
            r = r.append(df[df[col].isin(list_businessid_exclude_from_portfolio)])

    else:
        r = df
        #print(r)

    i = r.index.unique()
    print('Print unique Contract ids:- ', i)
    return i.values.tolist()



# def return_path(fname:str, period:str, path_loc_win:str, path_loc_linux:str=None):
#     if platform.system() == 'Windows':
#         #data_f = Path("//sirius.local/data/Group/GPI Reporting/Capital cost project/Cube_Data/")
#         data_f = Path(path_loc_win)
#     else:
#         #data_f = Path("/data/Cube_Data/")
#         data_f = Path(path_loc_linux)

#     path_file_period = os.path.join(data_f, f"{fname}_{period}")
#     #ppp = Path(path_file_period)    
#     #return path_file_period
#     print(path_file_period)
#     return path_file_period


# def GetDataFromPQ_pf(PMLPeriod, source_database, server, cols , pf) -> pd.DataFrame:
#     cols = ['GrossLoss' if x == 'GrossAmountUSD' else x for x in cols]
#     cols = ['GrossNetLoss' if x == 'GrossNetAmountUSD' else x for x in cols]
#     cols = ['NetNetLoss' if x == 'NetNetAmountUSD' else x for x in cols]

#     #data_file_name = nodeName['']
#     data_file_name = nodeName(PMLPeriod, source_database, server)
#     data_file_name = data_file_name['namefile']+ "_OEP"

#     data_folder = Path("C:\\workspace\\pricetool\\price-traget-tool\\data\\Cube_Data")

#     file_to_read = str(data_folder/data_file_name)
#     #print(file_to_read)
#     o=[]
#     for x in pf:
#         if self.PMLPeriod == '20191003':
#             o.append([('contract_id', '=', x)])
#         else:
#             o.append([('Contract_Id', '=', x)])

#     if o is not None:
#         ds = pq.ParquetDataset(file_to_read, filters=o)
#     else:
#         ds = pq.ParquetDataset(file_to_read)

#     tab = ds.read(columns=cols).to_pandas()

#     return tab

def calculate(param: List[str], list_businessid_exclude_from_portfolio:List[str]) -> pd.DataFrame:
    #print(f"calculating contract margtvar for period {PMLPeriod}")
    #fname = 'All_Contracts_loss_area_evtsource'
    #data_f = db.data_f()
    #l = []
    #l.append(['Incl', 'Office', ['Sirius International (Liege)']])
    #l.append(['Excl', 'BusinessId', runoff_contracts])
    #pf = create_portfolio(l)

    # returnpath1 = return_path(fname, period, path_loc_win)

    # if os.path.exists(returnpath1):
    #     print("yet to implement this part")
    # else:
    #     print("noooooooooooo")

    pf = create_portfolio(['Excl', 'BusinessId'], ['ITPR405990','ITPR405991','IDPR201687',
                   'IDPR400396','ITPR228563','ITPR322837',
                   'ITPR228953','ITPR401322','ITPR400640',
                   'ITPR228201','ITPR229063','ITPR228548',
                   'ITPR228114','ITPR228115','ITPR228025',
                   'ITPR228026','ITPR228027'])
    tab = Get_dimBusiness_Extended('20200102', '49547_GPR_Tabular_4', 'tst-sql-0585', 'C:\\workspace\\cubeData\\',pf)
    tab = tab[tab.Basis.isin(['Assumed', 'Prop Retro'])]
    print(tab.head(5))
    return tab



   # PMLPeriod: str, source_database: str, server: str, data_path: str, pf = None