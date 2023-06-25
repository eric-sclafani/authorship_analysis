from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from typing import List
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
            ("TruncatedSVD", TruncatedSVD(n=50, random_state=SEED)),
            ("TSNE", TSNE(random_state=SEED))
        ])
    else:
        doc_pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("TSNE", TSNE(random_state=SEED))
        ])
    return doc_pipeline.fit_transform(df.select_dtypes(include=np.number))
    
def apply_av_pipeline(df:pd.DataFrame) -> np.ndarray:
    """"""
    author_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("MDS", MDS(random_state=SEED))
    ])
    return author_pipeline.fit_transform(df.select_dtypes(include=np.number))

def apply_av_kmeans(dim_reduced_df:pd.DataFrame, k=6) -> KMeans:
    """"""
    kmeans = KMeans(n_clusters=k, random_state=SEED)
    return kmeans.fit(dim_reduced_df)


#~~~Author level data~~~
authors_df = pd.read_csv("data/features/author_vectors.csv")
author_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("MDS", MDS(random_state=42))
    ])
author_vectors = authors_df.loc[:, ~authors_df.columns.isin(['author_id'])]
processed_author_vectors = author_pipeline.fit_transform(author_vectors)
author_kmeans = KMeans(n_clusters=6, random_state=42)
author_kmeans.fit(processed_author_vectors) 


#~~~Document level data~~~
docs_df = pd.read_csv("data/features/document_vectors.csv")
doc_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("PCA", PCA(n_components=50, random_state=42)),
    ("TSNE", TSNE(random_state=42))
    ])
doc_vectors = docs_df.loc[:, ~docs_df.columns.isin(['doc_id', 'author_id'])]
processed_doc_vectors = doc_pipeline.fit_transform(doc_vectors)


#~~~Text documents~~~
# unvectorized text documents (data is not publicly available, so I cannot version control it)
text_docs_df = pd.read_json("data/documents/pan22_preprocessed.jsonl", lines=True)


# #~~~Helper functions~~~
# def get_author_id(author_index:int) -> str:
#     """Gets the author id given a DataFrame index"""
#     return authors_df.iloc[author_index].author_id if author_index is not None else "None"

# def get_doc_ids_given_author(author_index:int, doc_df:pd.DataFrame) -> List[str]:
#     """Retrieves the document IDs for all documents written by a given author"""
#     return doc_df.loc[doc_df['author_id'] == authors_df.iloc[author_index].author_id]["doc_id"].to_list()

# def get_author_entries(author_id:str, type="vectors") -> pd.DataFrame:
#     """Returns document vectors or text docs from a given author"""
#     if type == "vectors":
#         return docs_df.loc[docs_df["author_id"] == author_id]
#     elif type == "docs":
#         return text_docs_df.loc[text_docs_df["authorIDs"] == author_id]