
import plotly.express as px
import pandas as pd
from typing import List

# project
from .processing import authors_df, processed_author_vectors, author_kmeans
from .processing import docs_df, processed_doc_vectors


#~~~Helpers~~~

def get_doc_ids_given_author(author_index:int, doc_df:pd.DataFrame) -> List[str]:
    """Retrieves the document IDs for all documents written by a given author"""
    return doc_df.loc[doc_df['author_id'] == authors_df.iloc[author_index].author_id]["doc_id"].to_list()

#~~~ Plot functions ~~~   
  
def author_vector_plot():

    df = pd.DataFrame({"author_id":authors_df["author_id"],
                       "MDS Dim 1":processed_author_vectors[:,0],
                       "MDS Dim 2": processed_author_vectors[:,1],
                       "K Cluster": author_kmeans.labels_})
    fig = px.scatter(
        data_frame = df,
        x="MDS Dim 1",
        y="MDS Dim 2",  
        color="K Cluster",
        color_continuous_scale="fall",
        hover_data={
            "MDS Dim 1":False,
            "MDS Dim 2":False,
            "author_id":True},
    )
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
        yaxis_title=None
        )

    return fig

def document_vector_plot(hovered_author=None):
    
    df = pd.DataFrame({"author_id":docs_df["author_id"],
                       "TSNE Dim 1":processed_doc_vectors[:,0],
                       "TSNE Dim 2": processed_doc_vectors[:,1],
                       })

    if hovered_author is not None:
        doc_ids = get_doc_ids_given_author(hovered_author, docs_df)
        df["Is Foreground Author"] = ["True" if n in doc_ids else "False" for n in docs_df["doc_id"]]
    else:
        df["Is Foreground Author"] = "False"

    fig = px.scatter(
        data_frame = df,
        x="TSNE Dim 1",
        y="TSNE Dim 2",
        hover_data={
            "TSNE Dim 1":False,
            "TSNE Dim 2":False,
            "author_id":True},
        color=df["Is Foreground Author"], 
        color_discrete_map={"False":"lightgray", "True":"red"},
        
    )
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
        yaxis_title=None
        )
    
    fig.update_coloraxes(showscale=False)
    

    
    return fig