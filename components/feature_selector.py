from scipy.stats import zscore
from typing import List
import plotly.express as px
import plotly.graph_objects as go

# project imports
from .processing import author_vectors, authors_df
from .processing import get_author_entries, get_author_id


def get_threshold_zscores_idxs(zscores, threshold:float):
    """Gets indices for abs(zscores) that meet a threshold"""
    selected = []
    for i, zscore in enumerate(zscores):
        if abs(zscore) > threshold:
            selected.append(i)
    return selected

def get_identifying_features(author_id:str, threshold=2.0):
    """
    Given an author, calculates their zscores for all features and selects the ones that deviate the most from the 
    mean. These features are what separate this author from the average author
    """
    zscores = zscore(author_vectors)
    print(author_id)
    author_idx = authors_df.loc[authors_df["author_id"] == author_id].index[0]    
    author_zscores = zscores.iloc[author_idx]
    selected_zscores = get_threshold_zscores_idxs(author_zscores, threshold)
    return author_zscores.iloc[selected_zscores]

def features_to_show(author_id:str) -> List[str]:
    """Given an author id, returns n amount of this author's most identifying features"""
    features = get_identifying_features(author_id).index.to_list()
    if len(features) > 10:
        return features[:12]
    return features

def style_pcp_label(label:str) -> str:
    """Prepends a feature with <br> for better styling"""
    if label.count(":") > 1:
        return label
    else:    
        feat_type, feat = label.split(":")
        feat = "<br>" + feat
        return f"{feat_type}:{feat}"
    
    
def author_identifying_features_pcp(clicked_author=None):
    """Given an author, retrieves their most identifying features and displays them in a pcp"""
    author_id = get_author_id(clicked_author)
    author_entries = get_author_entries(author_id)
    author_features = features_to_show(author_id)
    
    fig = px.parallel_coordinates(
        author_entries,
        dimensions=author_features,
        labels={label:style_pcp_label(label) for label in author_features}
    )
    fig.update_layout(
        font=dict(size=10)
    )
    return fig


def default_pcp_plot():
    fig = go.Figure()
    fig.update_layout(
        xaxis =  { "visible": False },
        yaxis = { "visible": False },
        annotations = [
            {"text": "Please select an author from the Author Vector plot",
             "xref": "paper",
             "yref": "paper",
             "showarrow": False,
             "font": {"size": 28}
            }
        ]
    )
    return fig