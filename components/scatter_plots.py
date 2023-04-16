
from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
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
    df = pd.DataFrame({"author_id":docs_df["author_id"],
                       "TSNE Dim 1":transformed_data[:,0],
                       "TSNE Dim 2": transformed_data[:,1],})
    
    fig = px.scatter(
        data_frame = df,
        x="TSNE Dim 1",
        y="TSNE Dim 2",
        color="author_id"
    )
    
    return fig
    
    

def author_vector_plot():
    pass

