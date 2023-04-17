
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
docs_df = pd.read_csv("data/document_vectors.csv")
authors_df = pd.read_csv("data/author_vectors.csv")

# ~~~Pipelines~~~

doc_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("PCA", PCA(n_components=50)),
    ("TSNE", TSNE())
    ])

author_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("MDS", MDS())
    ])

   
 
#~~~ Plot functions ~~~   
def document_vector_plot():
    
    docs_values = docs_df.loc[:, ~docs_df.columns.isin(['doc_id', 'author_id'])]
    transformed_data = doc_pipeline.fit_transform(docs_values)
    
    kmeans = KMeans(n_clusters=6, random_state=42)
    kmeans.fit(transformed_data)
    df = pd.DataFrame({"author_id":docs_df["author_id"],
                       "TSNE Dim 1":transformed_data[:,0],
                       "TSNE Dim 2": transformed_data[:,1],
                       "K Cluster":kmeans.labels_})
    fig = px.scatter(
        data_frame = df,
        x="TSNE Dim 1",
        y="TSNE Dim 2",
        color="K Cluster",
        color_continuous_scale="fall"
    )
    
    fig.update_layout(
        title="Document Vectors",
        title_x=0.5)
    return fig
    
    
def author_vector_plot():

    authors_values = authors_df.loc[:, ~authors_df.columns.isin(['author_id'])]
    transformed_data = author_pipeline.fit_transform(authors_values)
    
    kmeans = KMeans(n_clusters=6, random_state=42)
    kmeans.fit(transformed_data)
    df = pd.DataFrame({"author_id":authors_df["author_id"],
                       "MDS Dim 1":transformed_data[:,0],
                       "MDS Dim 2": transformed_data[:,1],
                       "K Cluster": kmeans.labels_})
    fig = px.scatter(
        data_frame = df,
        x="MDS Dim 1",
        y="MDS Dim 2",  
        color="K Cluster",
        color_continuous_scale="fall"
    )
    
    fig.update_layout(
        title="Author Vectors",
        title_x=0.5)
    return fig

