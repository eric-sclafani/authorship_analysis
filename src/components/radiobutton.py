from dash import dcc, html
import dash_bootstrap_components as dbc
from typing import List, Dict

DATASETS = {
    "PAN22 Authorship Verification" : "pan2022",
    "Blogs Authorship Corpus" : "blogs",
    "IMDB Reviews" : "imdb_reviews",
    "HRS Release 03-20-2023" : "hrs_release_3-20-2023"
}

def make_radio_options() -> List[Dict]:
    options = []
    for clean_name, raw_name in DATASETS.items():
        options.append({"label": clean_name, "value": raw_name })
    return options
    

def make_dataset_radio():
    options = make_radio_options()
    return dcc.RadioItems(
        options=options,
        value="pan2022",
        className="dataset-radio",
        id="dataset-radio",
        inputStyle={"margin-right": "10px"}

    )