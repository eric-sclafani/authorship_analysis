#!/usr/bin/env python3
"""
This script is for making postgres tables for a dataset on the document and author levels
"""
import pandas as pd
import numpy as np
import argparse
from sqlalchemy import create_engine
from dataclasses import dataclass

from typing import Dict

# project imports
from connect import config

def load_document_vectors(path:str) -> pd.DataFrame:
    return pd.read_csv(path)

def get_author_ids(doc_df:pd.DataFrame) -> np.ndarray:
    return doc_df.authorIDs.unique()

def make_author_vector(author_id:str, doc_df:pd.DataFrame) -> pd.Series:
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


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n",
                        "--name",
                        required=True,
                        help="Name of dataset")
    parser.add_argument("-d",
                        "--document_vectors_path",
                        required=True,
                        help="Path to a dataset's generated document vectors")
    
    args = parser.parse_args()
    
    document_vectors = load_document_vectors(args.document_vectors_path)
    author_vectors = make_author_vector_df(document_vectors)
    
    cfg = config()
    engine = create_engine(f'postgresql://{cfg["user"]}:{cfg["password"]}@{cfg["host"]}:{cfg["port"]}/{cfg["database"]}')
    

    
    document_vectors.to_sql(f"{args.name}_document_vectors", engine, index=False, if_exists="fail")
    #author_vectors.to_sql(f"{args.name}_author_vectors", engine, index=False, if_exists="fail")


if __name__ == "__main__":
    main()