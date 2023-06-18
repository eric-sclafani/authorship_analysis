import dash_bootstrap_components as dbc

from .checklist import make_feature_checklist, make_checklist_button
from .dropdown import make_dataset_dropdown


feature_checklist = dbc.Col(
    [make_feature_checklist(), 
     make_checklist_button()], 
    className="checklist", 
    )

dataset_dropdown = dbc.Col(
    [make_dataset_dropdown()],
    className="dataset-dropdown"
)