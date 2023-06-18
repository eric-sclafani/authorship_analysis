from dash import dcc, html
import dash_bootstrap_components as dbc
from typing import List, Dict

DATASETS = {
    "PAN22 Authorship Verification" : "pan2022",
    "Blogs Authorship Corpus" : "blogs",
    "IMDB Reviews" : "imdb_reviews"
}

def make_dropdown_options() -> List[Dict]:
    options = []
    for clean_name, raw_name in DATASETS.items():
        options.append({
            "label": html.Div([clean_name], className="dropdown-item"),
            "value": raw_name
        })
    return options
    

def make_dataset_dropdown():
    options = make_dropdown_options()
    return dcc.Dropdown(
        options=options,
        value=["PAN22 Authorship Verification"],
        clearable=False,
        className="dataset-dropdown"
    )