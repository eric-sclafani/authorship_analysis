
import plotly.graph_objects as go
import pandas as pd
from typing import List



def author_vector_plot(df:pd.DataFrame):

    fig = go.Figure(
        go.Scatter(
            mode="markers",
            x=df["MDS Dim 1"],
            y=df["MDS Dim 2"],
            text=df.index,
            marker_color=df["K Cluster"],
            marker=dict(colorscale=["blue", "red", "orange", "green"]),
            hovertemplate="<b>Author</b>: %{text}<extra></extra>",
            showlegend=False   
    )
        )
    fig.update_layout(
        title="<b>Author Vectors</b>",
        title_x=0.47,
        title_y=.85,
        font_family = "Courier New",
        title_font_family = "Courier New",
        hoverlabel = dict(font_size = 16,font_family = "Sitka Small"),
        xaxis_title=None,
        yaxis_title=None,
        )    
    return fig

def document_vector_plot(df:pd.DataFrame):
    
    fig = go.Figure(go.Scatter(
        mode="markers",
        x=df["TSNE Dim 1"],
        y=df["TSNE Dim 2"],
        text=df["author_id"],
        marker_color="gray",
        marker=dict(colorscale=["gray", "red"], 
                    opacity=1, 
                    color="gray"),
        hovertemplate="<b>Author</b>: %{text}<extra></extra>"
    ))
    fig.update_layout(
        title="<b>Document Vectors</b>",
        title_x=0.5,
        title_y=.85,
        font_family="Courier New",
        title_font_family="Courier New",
        hoverlabel=dict(font_size = 16,font_family = "Sitka Small"),
        coloraxis_showscale=False,
        xaxis_title=None,
        yaxis_title=None,
        )
    return fig


# ~~~Helpers~~~

def get_doc_ids_given_author(author_index:int, 
                             doc_df:pd.DataFrame,
                             authors_df:pd.DataFrame) -> List[str]:
    """Retrieves the document IDs for all documents written by a given author"""    
    author_id = authors_df.iloc[author_index].name
    selected_doc_df = doc_df.loc[doc_df["author_id"] == author_id]
    return selected_doc_df.index.to_list()

def get_author_id(author_index:int, authors_df:pd.DataFrame) -> str:
    """Retrieves the author_id of an entry given that author's dataframe index"""
    return authors_df.iloc[author_index].name if author_index is not None else "None"

