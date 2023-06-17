from dash import dcc, html
from typing import List

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



def make_checklist_items():
    features = []
    for clean_name, feat_name in FEATURE_NAMES.items():
        features.append({
            "label": html.Div([clean_name], className = "feature-checklist-item"),
            "value": feat_name
        })
    return features


def feature_checklist() -> dcc.Checklist:
    features = make_checklist_items()
    return dcc.Checklist(
        options=features,
        value=[feat["value"] for feat in features],
        labelStyle={"display": "flex", "align-items": "center"}
    )
