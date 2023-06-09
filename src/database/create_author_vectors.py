#!/usr/bin/env python3
import numpy as np
import pandas as pd


def load_document_vectors_csv(path:str) -> pd.DataFrame:
    """Loads a provided CSV as a DataFrame"""
    return pd.read_csv(path)

def get_author_ids(doc_df:pd.DataFrame) -> np.ndarray:
    return doc_df.authorIDs.unique()

def make_author_vector(author_id:str, doc_df:pd.DataFrame) -> np.ndarray:
    author_document_vectors = doc_df.loc[doc_df['authorIDs'] == author_id]
    return author_document_vectors.mean(axis=0, numeric_only=True)

def make_author_vector_df(doc_df:pd.DataFrame) -> pd.DataFrame:
    """Creates author vectors by averaging each author's documents into one"""
    author_ids = get_author_ids(doc_df)
    author_ids_to_avs = {}
    for author_id in author_ids:
        author_ids_to_avs[author_id] = make_author_vector(author_id, doc_df)    
    av_df = pd.DataFrame(author_ids_to_avs).T
    return av_df