from dash import dcc, html
import dash_bootstrap_components as dbc
from typing import List, Dict


FEATURE_NAMES = {
    "POS unigrams" : "pos_unigrams", 
    "POS bigrams" : "pos_bigrams",
    "Function words" : "func_words",
    "Punctuation" : "punctuation",
    "Letters" : "letters",
    "Emojis" : "emojis",
    "Dependency labels":"dep_labels",
    "Morphology tags" : "morph_tags"
}

def make_checklist_items() -> List[Dict]:
    features = []
    for clean_name, raw_name in FEATURE_NAMES.items():
        features.append({
            "label": html.Div([clean_name], className="checklist-item"),
            "value": raw_name
        })
    return features

def make_feature_checklist() -> dcc.Checklist:
    features = make_checklist_items()
    return dcc.Checklist(
        id="checklist",
        options=features,
        value=[feat["value"] for feat in features],
        labelStyle={"display": "flex", "align-items": "center"},
        inputStyle={"margin-right": "10px"}
    )
    
def make_checklist_button() -> dbc.Button:
    return dbc.Button(
        "Submit",
        id="checklist-button",
        className="checklist-button",
    )
    