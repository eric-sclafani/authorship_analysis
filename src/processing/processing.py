from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

SEED = 42

def has_high_dimensions(df:pd.DataFrame, threshhold=100) -> bool:
    """Determines if a df crosses over a dimensionality threshold"""
    return df.shape[1] > threshhold

def apply_dv_pipeline(df:pd.DataFrame) -> np.ndarray:
    """
    Applies dimensionality reduction to document vectors. If the df dimensionality is higher, also use TruncatedSVD 
    (as instructed by the TSNE documentation)
    """
    if has_high_dimensions(df):
        doc_pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("TruncatedSVD", TruncatedSVD(n_components=50, random_state=SEED)),
            ("TSNE", TSNE(random_state=SEED))
        ])
    else:
        doc_pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("TSNE", TSNE(random_state=SEED))
        ])
    reduced = doc_pipeline.fit_transform(df.select_dtypes(include=np.number))
    return pd.DataFrame({
        "author_id" : df["author_id"],
        "TSNE Dim 1" : reduced[:, 0],
        "TSNE Dim 2" : reduced[:, 1]
    },
                        index=df.index)
   
def apply_av_kmeans(dim_reduced_df:pd.DataFrame, k=6) -> KMeans:
    """Applies KMeans to cluster authors with more similar writing styles together based off vector similarity"""
    kmeans = KMeans(n_clusters=k, random_state=SEED)
    return kmeans.fit(dim_reduced_df) 

def apply_av_pipeline(df:pd.DataFrame) -> pd.DataFrame:
    """Applies dimensionality reduction to author vectors"""
    author_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("MDS", MDS(random_state=SEED))
    ])
    reduced = author_pipeline.fit_transform(df.select_dtypes(include=np.number))
    kmeans = apply_av_kmeans(reduced)
    return pd.DataFrame({
        "MDS Dim 1" : reduced[:, 0],
        "MDS Dim 2" : reduced[:, 1],
        "K Cluster" : kmeans.labels_
    }, 
                        index=df.index)

