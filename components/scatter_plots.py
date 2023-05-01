
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List

# project
from .processing import authors_df, processed_author_vectors, author_kmeans
from .processing import docs_df, processed_doc_vectors
from .processing import get_author_id, get_doc_ids_given_author


#~~~ Plot functions ~~~   
  
def author_vector_plot(clicked_author=None):

    df = pd.DataFrame({"author_id":authors_df["author_id"],
                       "MDS Dim 1":processed_author_vectors[:,0],
                       "MDS Dim 2": processed_author_vectors[:,1],
                       "K Cluster": author_kmeans.labels_})
    
    fig = go.Figure(go.Scatter(
        mode="markers",
        x=df["MDS Dim 1"],
        y=df["MDS Dim 2"],
        text=df["author_id"],
        marker_color=df["K Cluster"],
        marker=dict(colorscale=["blue", "red", "orange", "green"]),
        hovertemplate="<b>Author</b>: %{text}<extra></extra>",
        showlegend=False
        
    ))
    fig.update_layout(
        title="Author Vectors",
        title_x=0.47,
        autosize=False,
        width=500,
        height=350,
        font_family = "Courier New",
        title_font_family = "Courier New",
        hoverlabel = dict(font_size = 16,font_family = "Sitka Small"),
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(t=20, l=20, b=150)
        )
    
    if clicked_author:
        x = clicked_author["points"][0]["x"]
        y = clicked_author["points"][0]["y"]
        author_index = clicked_author["points"][0]["pointIndex"]
        fig.add_trace(
            go.Scatter(
                x = [x],
                y = [y],
                mode="markers",
                marker_symbol="circle-open",
                marker_size=16,
                text=get_author_id(author_index),
                hoverinfo="skip",
                showlegend=False
            )
            )
    
    return fig

def document_vector_plot(clicked_author=None):
    
    df = pd.DataFrame({"author_id":docs_df["author_id"],
                       "TSNE Dim 1":processed_doc_vectors[:,0],
                       "TSNE Dim 2": processed_doc_vectors[:,1],
                       })
    
    author_id = get_author_id(clicked_author)
    author_col = f"From Author: {author_id}"
    if clicked_author is not None:
        doc_ids = get_doc_ids_given_author(clicked_author, docs_df)
        df[author_col] = [1 if n in doc_ids else 0 for n in docs_df["doc_id"]]
        df["opacity"] = np.where(df[author_col] == 1, 1, .45)
    else:
        df[author_col] = 1
        df["opacity"] = 1
    
    fig = go.Figure(go.Scatter(
        mode="markers",
        x=df["TSNE Dim 1"],
        y=df["TSNE Dim 2"],
        text=df["author_id"],
        marker_color=df[author_col],
        marker=dict(colorscale=["lightgray", "red"], opacity=df["opacity"], color="lightgray"),
        hovertemplate="<b>Author</b>: %{text}<extra></extra>" 
    ))
    fig.update_layout(
        title="Document Vectors",
        title_x=0.5,
        autosize=False,
        width=950,
        height=350,
        font_family="Courier New",
        title_font_family="Courier New",
        hoverlabel=dict(font_size = 16,font_family = "Sitka Small"),
        coloraxis_showscale=False,
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, t=20, b=150)
        )
    return fig