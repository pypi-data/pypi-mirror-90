
from typing import Any, Dict, List
import os
import os.path
import platform
#from kedro.extras.datasets.pandas import ParquetDataSet  
#from kedro.io import ParquetLocalDataSet
import pandas as pd  
import numpy as np
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

if platform.system() == 'Windows':
    data_folder = Path("C:\\workspace\\cubeData\\")

class db_connection():
    def __init__(self, source_database, server, PMLPeriod):
        self.PMLPeriod = PMLPeriod
        self.source_database =source_database
        self.server = server

        self.pq_file = f"Contracts_File_{server}_{source_database}_{str(PMLPeriod)}"
        #data_folder_name = pq_file + "_Terms"

    def data_f():
        if platform.system() == 'Windows':
            data_folder = Path("C:\\workspace\\cubeData\\")
        else:
             data_folder = Path("/data/Cube_Data/")
        return data_folder

    def Get_dimBusiness_Extended (self, pf = None) -> pd.DataFrame:
        data_file_name = self.pq_file + "_Terms"
        #data_path = Path(data_path)
        file_to_read = str(data_folder / data_file_name)
        ds = ParquetDataSet(filepath=file_to_read)
        tab = ds.load()

        

        if pf is not None:
            # .load() converts Pandas.ParquetDataSet into Pandas.DataFrame
            #res = data_set[data_set.index.isin(pf)].load()
            res = tab[tab.index.isin(pf)]

        else:
            res = tab
        return res


    def create_portfolio(self, param = None) -> pd.DataFrame:
        df = self.Get_dimBusiness_Extended()
        cols = df.columns.values

        list_businessid_exclude_from_portfolio = ['ITPR405990','ITPR405991','IDPR201687',
                   'IDPR400396','ITPR228563','ITPR322837',
                   'ITPR228953','ITPR401322','ITPR400640',
                   'ITPR228201','ITPR229063','ITPR228548',
                   'ITPR228114','ITPR228115','ITPR228025',
                   'ITPR228026','ITPR228027']

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


    def GetSavedDataFromPQ(self, saved_file):
        try:
            file_to_read = str(data_folder / saved_file)
            ds = ParquetDataSet(filepath=file_to_read)
            tab = ds.load()
        except Exception:
            traceback.print_exc()
            return False
        return tab

    def GetDataFromPQ_pf(self, pf, cols = ['Trial_Id', 'Event_Id', 'GrossAmountUSD'], save = None, appendfile = False):
        cols = ['GrossLoss' if x == 'GrossAmountUSD' else x for x in cols]
        cols = ['GrossNetLoss' if x == 'GrossNetAmountUSD' else x for x in cols]
        cols = ['NetNetLoss' if x == 'NetNetAmountUSD' else x for x in cols]

        data_file_name = self.pq_file + "_OEP"
        #data_folder = Path(data_folder)
        file_to_read = Path(str(data_folder / data_file_name))

        o=[]
        for x in pf:
            if self.PMLPeriod == '20191003':
                o.append([('contract_id', '=', x)])
            else:
                o.append([('Contract_Id', '=', x)])

        if o is not None:
            #ds = ParquetDataset(filepath=file_to_read, filters=o)
            ds = ParquetDataset(filepath=file_to_read)
        else:
            ds = ParquetDataset(filepath=file_to_read)
            tab = ds.load(columns=cols)
        return tab



class Loss_contract:
    def __init__(self, period, rps, list_businessid_exclude_from_portfolio, measure = 'marginal_tvar'):
        self.period = period
        self.measure = measure
        self.resultfolder = f'result_{period}'
        self.rps = rps
        self.list_businessid_exclude_from_portfolio = list_businessid_exclude_from_portfolio

        if not os.path.exists(os.path.join('result', self.resultfolder)):
            os.mkdir(os.path.join('C:\\workspace\\cubeData\\result\\', self.resultfolder))

    def testrun(self):
        print('I am printed')

    def calculate(self, period, fname, l) -> pd.DataFrame:
    
        print(f'calculating contract margtvar for period {period}')
        
        conn = db_connection("Cube", "Test", int(self.period))
        data_f = db_connection.data_f()

        pf = conn.create_portfolio(l)

        if os.path.exists(os.path.join(data_f, f"{fname}_{self.period}")):
            #dfloss = conn.GetSavedDataFromPQ(f'{fname}_{self.period}')
            pass
        else:
            print('do else')
            dfloss = conn.GetDataFromPQ_pf(pf, 
                                            cols=['Trial_Id', 'Contract_Id', 'PMLArea_Id', 'GrossNetLoss', 'EventSource_Id'], appendfile = False)

            dfloss.rename(columns = {'Trial_Id': 'trialid', 'PMLArea_Id': 'pmlareaid', 'PerilModel_Id' : 'perilmodelid', 'Event_Id': 'eventid', 'GrossNetLoss':'amount',
                                      'GrossLoss':'amount', 'NetNetLoss':'amount', 'contract_id':'contractid', 'Contract_Id' : 'contractid',
                                         'GrossAmountUSD':'amount', 'GrossNetAmountUSD':'amount', 'NetNetAmountUSD':'amount'}, inplace=True)

            dfloss.contractid = dfloss.contractid.astype('int64')

            dfloss.EventSource_Id = dfloss.EventSource_Id.astype('int64')
            dfloss = dfloss[dfloss.EventSource_Id != 1]
            dfloss = dfloss.drop(columns = ['EventSource_Id'])
            dfloss = dfloss[['trialid', 'contractid', 'amount']]
            dfloss = dfloss.rename(columns = {'contractid' : 'id'})

            dfloss = dfloss.groupby(['id', 'trialid'], as_index=False)['amount'].sum()
            dfr = dfloss

            dfr['amount'] = - dfr['amount']

            dfrg = dfr.groupby('id', as_index=False)['amount'].sum()
            dfrg['amount'] = dfrg['amount']/20000

            print('finished dfr')

            for rp in self.rps:
                if self.measure == 'marginal_tvar':
                    dfmargtvar=Allocations.marginalmeasure(dfr, tvar, measurekwargs = {'rp' : rp})
                    print(f"marginal tvar {rp} calculated!")
                elif self.measure == 'co_tvar':
                    dfmargtvar = Allocations.comeasure(dfr, tvar, measurekwargs={'rp' : rp})
                    print(f"co_tvar {rp} calculated!")
                else:
                    print('no correct measure specified!')
                
                dff = dfmargtvar.merge(dfrg, on = 'id')
                dff.rename(columns = {'amount': 'loss_exadhoc'})
                dff.to_csv(f"result/{self.resultfolder}/{self.measure}_{rp}_all_contract_loss.csv")
                gc.collect()



class Allocations:
    def marginalmeasure(dfdata, measure, measureargs = [] , measurekwargs = {}, id=None, inf=False):
        dfdata = Probability_Measures.sum_per_id_trial(dfdata)
        
        if inf==False:
            inf_factor =1 
        elif inf==True:
            inf_factor = 1e-6
        elif not (isinstance(inf, float) or isinstance(inf, int)):
            raise TypeError('inf must be either True, False or a float')
        
        if id is None:
            id = dfdata.id.drop_duplicates().values

        if isinstance(id,int):
            id = [id]

        totalmeasure = measure(dfdata, *measureargs, **measurekwargs)
        totalsum_per_trial = sum_per_trial(dfdata).set_index('trialid')

        dfoutput = pd.DataFrame([], columns = ['id', f'marginal_{measure.__name__}'])
        dfdata.set_index('id', inplace=True)

        for idvalue in id:
            try:
                sum_per_trial_id = sum_per_trial(dfdata.loc[idvalue]).set_index('trialid')

                totalsum_per_trial_minus_id = totalsum_per_trial.copy()
                totalsum_per_trial_minus_id= totalsum_per_trial_minus_id.add(-sum_per_trial_id, fill_value=0).reset_index()
            except:
                sum_per_trial_id = sum_per_trial(dfdata.loc[idvalue:idvalue]).set_index('trialid')

                totalsum_per_trial_minus_id = totalsum_per_trial.copy()
                totalsum_per_trial_minus_id= totalsum_per_trial_minus_id.add(-sum_per_trial_id, fill_value=0).reset_index()
            
            totalmeasure_minus_id = measure(totalsum_per_trial_minus_id, *measureargs, **measurekwargs)
            marginalmeasure = (totalmeasure - inf_factor * totalmeasure_minus_id)/inf_factor
            dfoutput = dfoutput.append({'id' : idvalue, f'marginal_{measure.__name__}' : marginalmeasure}, ignore_index=True)

        dfoutput = dfoutput.reset_index(drop=True)
        dfoutput.id = dfoutput.id.astype('int64')

        return dfoutput

    def comeasure(dfdata, measure, measureargs = [], measurekwargs = {}, id=None):
        dfdata = Probability_Measures.sum_per_id_trial(dfdata)
        if id is None:
            id = dfdata.id.drop_duplicates().values
        if isinstance(id, int):
            id = [id]

        rounds = measure(dfdata, *measureargs, **measurekwargs, output_rounds=True)
        print('rounds found')
        if not isinstance(rounds, pd.DataFrame):
            rounds = rounds.to_frame()

        dfinputrounds= dfdata.merge(rounds, on='trialid')
        print('start measure per id')
        dfoutput = split_measure_per_id(dfinputrounds, measure, measureargs = measureargs , measurekwargs = measurekwargs, id = id)
        dfoutput = dfoutput.rename(columns = {measure.__name__ : 'co_' + measure.__name__})
        dfoutput.id = dfoutput.id.astype('int64')
        return dfoutput



class Probability_Measures:
    def select_id(dfdata, id=None):
        if id is not None:
            if isinstance(id, list):
                dfoutput = dfdata[dfdata.id.isin(id)]
            else:
                try:
                    dfoutput = dfdata[dfdata.id==id]
                except:
                    raise TypeError('Error - wrong is type')
        else:
            dfoutput = dfdata
        dfoutput = dfoutput.reset_index(drop=True)
        return dfoutput

    def sum_per_id_trial(df):
        cols = list(df.columns.values)
        assert('trialid' in cols and 'amount' in cols and 'id' in cols), 'Dataframe must contain columns trialid, amount and id'

        if 'cocofactor' not in df.columns:
            df = df.groupby(['id', 'trialid'], as_index=False)['amount'].sum()
        else:
            df = df.groupby(['id', 'trailid', 'cocofactor'], as_index=False)['amount'].sum()

        return df


    def sum_per_trail(df, id=None):
        cols = list(df.columns.values)
        assert('trialid' in cols and 'amount' in cols), 'Dataframe must contain columns trialid and amount'
        
        df = select_id(df, id)

        if 'cocofactor' not in df.columns:
            df = df.groupby("trialid", as_index=False)['amount'].sum()
        else:
            df=df.groupby(["trialid", "cocofactor"], as_index=False)["amount"].sum()
        return df

    def rp_for_trial(df, numberofrounds = 20000):
        cols = list(df.columns.values)
        assert('trialid' in cols and 'amount' in cols), 'Dataframe must contain columns trialid and amount'
        # assert(df.groupby("trialid").agg({"trialid": pd.Series.nunique}).shape[0] == len(df)), 'Must have one value per trial'
        if df.groupby("trialid").agg({"trialid": pd.Series.nunique}).shape[0] != len(df):
            raise ValueError('df must have only one value per trial, take either max per trial or sum per trial first')
        
        dfsort = df.sort_values('amount', ascending=True).reset_index(drop=True)
        dfsort['rp']=numberofrounds/(dfsort.index + 1)
        return dfsort

    def aep(df, numberofrounds = 20000, rp=True):
        cols = list(df.columns.values)
        assert('trialid' in cols and 'amount' in cols), 'Dataframe must contain columns trialid and amount'

        dfaep = sum_per_trail(df)

        dfaep = rp_for_trial(dfaep, numberofrounds)

        if not rp:
            dfaep['exceedence_probability'] = 1/dfaep['rp']
            dfaep = dfaep.drop(columns = 'rp')
        
        return dfaep




class runCalc:
    def contracts_func(period, rps, list_businessid_exclude_from_portfolio, fname, l):
        contracts = Loss_contract(period, rps, list_businessid_exclude_from_portfolio)
        #contracts.testrun()
        contracts.calculate(period, fname, l)

    

