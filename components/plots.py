
from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)


#~~~Data~~~
docs_df = pd.read_csv("data/document_vectors.csv")
authors_df = pd.read_csv("data/author_vectors.csv")



# ~~~Helpers~~~

def reduce_dimensions(df:pd.DataFrame) -> np.ndarray:
    pca = PCA(n_components=50, random_state=42)
    tsne = TSNE(n_components=2, random_state=42)
    sc = StandardScaler()
    return pd.DataFrame(tsne.fit_transform(sc.fit_transform(df.values)),
                        columns=["TSNE Dim 1", "TSNE Dim 2"])
   
 
#~~~ Plot functions ~~~   
def document_vector_plot():
    
    docs_values= docs_df.loc[:, ~docs_df.columns.isin(['doc_id', 'author_id'])]
    reduced_data = reduce_dimensions(docs_values)
    
    fig = px.scatter(
        data_frame = reduced_data,
        x="TSNE Dim 1",
        y="TSNE Dim 2"
        
    )
    
    return fig
    
    

def author_vector_plot():
    pass


document_vector_plot()