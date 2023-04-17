
from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
import plotly.express as px
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)


#~~~Data~~~

authors_df = pd.read_csv("data/author_vectors.csv")
author_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("MDS", MDS())
    ])
author_vectors = authors_df.loc[:, ~authors_df.columns.isin(['author_id'])]
processed_author_vectors = author_pipeline.fit_transform(author_vectors)
author_kmeans = KMeans(n_clusters=6, random_state=42)
author_kmeans.fit(processed_author_vectors) 


docs_df = pd.read_csv("data/document_vectors.csv")
doc_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("PCA", PCA(n_components=50)),
    ("TSNE", TSNE())
    ])
doc_vectors = docs_df.loc[:, ~docs_df.columns.isin(['doc_id', 'author_id'])]
processed_doc_vectors = doc_pipeline.fit_transform(doc_vectors)
doc_kmeans = KMeans(n_clusters=6, random_state=42)
doc_kmeans.fit(processed_doc_vectors)


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
        color_continuous_scale="fall"
    )
    
    fig.update_layout(
        title="Author Vectors",
        title_x=0.2,
        autosize=False,
        width=500,
        height=350,
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
        color_continuous_scale="fall"
    )
    fig.update_layout(
        title="Document Vectors",
        title_x=0.5,
        autosize=False,
        width=750,
        height=350,
        margin=dict(l=0, r=0))
    
    return fig