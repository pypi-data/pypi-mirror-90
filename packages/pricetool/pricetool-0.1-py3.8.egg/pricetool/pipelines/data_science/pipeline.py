"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""


# def create_pipeline(**kwargs):
#     return Pipeline(
#         [
#             # node(
#             #     train_model,
#             #     ["example_train_x", "example_train_y", "parameters"],
#             #     "example_model",
#             # ),
#             # node(
#             #     predict,
#             #     dict(model="example_model", test_x="example_test_x"),
#             #     "example_predictions",
#             # ),
#             # node(report_accuracy, ["example_predictions", "example_test_y"], None),
#         ]
#     )


from kedro.pipeline import Pipeline, node

from .nodes import fileName111


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                fileName111,
                ["params:PMLPeriod", "params:source_database", "params:server"],
                # dict(
                #     train_x="example_train_x",
                #     train_y="example_train_y",
                #     test_x="example_test_x",
                #     test_y="example_test_y",
                # ),
                dict(pq_file="pq_file"),
            )
        ]
    )
