
import plotly.express as px
import pandas as pd

# project
from .processing import authors_df, processed_author_vectors, author_kmeans
from .processing import docs_df, processed_doc_vectors, doc_kmeans


#~~~Helpers~~~

def get_docs_given_author(author_index:int, df:pd.DataFrame) -> pd.DataFrame:
    """Retrieves document records written by a given author"""
    return df.loc[df['author_id'] == authors_df.iloc[author_index].author_id]


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
        hoverlabel = dict(font_size = 16,font_family = "Sitka Small")
        )

    return fig

def document_vector_plot(selected_author=None):
    
    df = pd.DataFrame({"author_id":docs_df["author_id"],
                       "TSNE Dim 1":processed_doc_vectors[:,0],
                       "TSNE Dim 2": processed_doc_vectors[:,1],
                       "K Cluster":doc_kmeans.labels_})
    df_to_show = df if selected_author is None else get_docs_given_author(selected_author, df)
    
    fig = px.scatter(
        data_frame = df_to_show,
        x="TSNE Dim 1",
        y="TSNE Dim 2",
        color="K Cluster",
        color_continuous_scale="fall",
        hover_data={
            "TSNE Dim 1":False,
            "TSNE Dim 2":False,
            "author_id":True}
    )
    fig.update_layout(
        title="Document Vectors",
        title_x=0.5,
        autosize=False,
        width=900,
        height=350,
        margin=dict(l=0, r=0),
        font_family="Courier New",
        title_font_family="Courier New",
        hoverlabel = dict(font_size = 16,font_family = "Sitka Small")
        )
    
    return fig