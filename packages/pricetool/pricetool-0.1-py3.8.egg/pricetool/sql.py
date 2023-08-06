from kedro.io import DataCatalog
from kedro.extras.datasets.pandas import (
    CSVDataSet,
    SQLTableDataSet,
    SQLQueryDataSet,
    ParquetDataSet,
)

from .nodes import nodeName


def Get_dimBusiness_Extended(
    PMLPeriod: str, source_database: str, server: str, pf=None
) -> Dict[str, Any]:
    nName = nodeName(PMLPeriod, source_database, server)
    data_file_name = nName["namefile"] + "_Terms"
    file_to_read = dict(xyz=data_file_name)
    return file_to_read


io = DataCatalog(
    {
        "example_iris_data": CSVDataSet(
            filepath="C://workspace//pricetool//price-traget-tool//data//01_raw//iris.csv"
        ),
        # "scooters_query": SQLQueryDataSet(sql="select * from example_iris_data", credentials=dict(con="sqlite:///kedro.db"),),
    }
)

iris = io.load("example_iris_data")
# scooter = io.load("scooters_query")

print(iris)
