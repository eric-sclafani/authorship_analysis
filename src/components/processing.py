from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from typing import List
import pandas as pd
import warnings
import joblib
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)


def default_vectors_dim_reduced(df:pd.DataFrame) -> pd.DataFrame:
    pass


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