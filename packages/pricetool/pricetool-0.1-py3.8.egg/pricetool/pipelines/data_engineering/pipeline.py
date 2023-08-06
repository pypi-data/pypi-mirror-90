"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

# from kedro.pipeline import Pipeline, node

# from .nodes import split_data
# from .nodes import load_pq
# from .nodes import fileNameCreator


# # _dict = {
# #   "server": "tst-sql-0585",
# #   "source_database": "49547_GPR_Tabular_4",
# #   "PMLPeriod": "20200102"}


# def create_pipeline(**kwargs):
#     return Pipeline(
#         [
#             #node(func=load_pq, inputs=[], outputs="example_pq_data_output"),

#             node(func=fileNameCreator, inputs=[{
#   "server": "tst-sql-0585",
#   "source_database": "49547_GPR_Tabular_4",
#   "PMLPeriod": "20200102"}], outputs=[]),

#         ]
#     )

# from kedro.pipeline import Pipeline, node

# from .nodes import fileName

# def create_pipeline(**kwargs):
#     return Pipeline(
#         [
#             node(
#                 fileName,
#                 ["params:PMLPeriod", "params:source_database", "params:server"],
#                 # dict(
#                 #     train_x="example_train_x",
#                 #     train_y="example_train_y",
#                 #     test_x="example_test_x",
#                 #     test_y="example_test_y",
#                 # ),
#                 #dict(pq_file = f"Contracts_File_{server}_{source_database}_{str(PMLPeriod)}".replace(",","_")),
#                 dict('pq_file'=str),
#             )
#         ]
#     )

# from kedro.pipeline import Pipeline, node
# from pricetool.pipelines.data_engineering.nodes import (fileName,)


from kedro.pipeline import Pipeline, node

from .nodes import (
    Loss_contract,
    db_connection,
    runCalc
    #fileNameCreator,
    #nodeName,
    #Get_dimBusiness_Extended,
    #create_portfolio,
    #return_path,
    #calculate,
    #naiveFilePath,
    #GetDataFromPQ_pf,
    #platform_path,
)

from typing import Any, Dict, List


def create_pipeline(**kwargs):
    return Pipeline(
        [

            # node(
            #     func=Loss_contract.calculate,
            #     inputs=["params:period", "params:fname", "params:l"],
            #     outputs="calculate",
            #     name="calculate"
            # ),

            node(
                func=runCalc.contracts_func,
                inputs=["params:period", "params:rps", "params:list_businessid_exclude_from_portfolio", "params:fname", "params:l"],
                outputs="contracts",
                name="contracts"
            ),
            # node(
            #     func=db_connection.create_portfolio,
            #     inputs=["params:list_businessid_exclude_from_portfolio"],
            #     outputs="calculate",
            #     name="calculate"
            # ),
            # node(naiveFilePath, inputs=["raw_car_data", "params:PMLPeriod", "params:source_database", "params:server"], outputs=None, name="test_filepath"),
            # node(
            #     func=nodeName,
            #     inputs=["params:PMLPeriod", "params:source_database", "params:server", "params:data_folder"],
            #     outputs=dict(namefile="pq_file_output"),
            #     name="pq_file_node",
            # ),

            # node(
            #     func=fileNameCreator,
            #     inputs=["params:_dict"],
            #     # outputs=dict(xyz='pq_file_output1'),
            #     outputs="fileNameCreator",
            #     name="fileNameCreator",
            # ),

            # node(
            #     func=Get_dimBusiness_Extended,
            #     inputs=["params:PMLPeriod", "params:source_database", "params:server", "params:data_path"],
            #     # outputs=dict(xyz='pq_file_output1'),
            #     outputs="Get_dimBusiness_Extended",
            #     name="getdimBus",
            # ),
            # node(
            #     create_portfolio,
            #     inputs= ["params:param", "params:list_businessid_exclude_from_portfolio"],
            #     # outputs=dict(xyz='pq_file_output1'),
            #     outputs="create_portfolio",
            #     name="createPortfolio",
            # ),
            # node(
            #     return_path,
            #     inputs=[
            #         "params:fname",
            #         "params:period",
            #         "params:path_loc_win",
            #         "params:path_loc_linux",
            #     ],
            #     # outputs=dict(xyz='pq_file_output1'),
            #     # outputs=dict(namefile = 'path_file_period'),
            #     outputs="return_path",
            #     name="return_path",
            # ),
            # node(
            #     calculate,
            #     inputs=[
            #         "params:param",
            #         "params:list_businessid_exclude_from_portfolio",
            #     ],
            #     # outputs=dict(xyz='pq_file_output1'),
            #     # outputs=dict(namefile = 'path_file_period'),
            #     outputs="calculate",
            #     name="calculate",
            # ),

            # node(
            #     GetDataFromPQ_pf,
            #     inputs=["params:PMLPeriod", "params:source_database", "params:server",
            #         "params:cols", None
            #     ],
            #     # outputs=dict(xyz='pq_file_output1'),
            #     # outputs=dict(namefile = 'path_file_period'),
            #     outputs="GetDataFromPQ_pf",
            #     name="GetDataFromPQ_pf",
            # ),


        ]
    )
