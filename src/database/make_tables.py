#!/usr/bin/env python3
"""
This script is for making postgres tables for a dataset on the document and author levels
"""
import pandas as pd
import numpy as np
import argparse
from sqlalchemy import create_engine
from dataclasses import dataclass
from typing import List

# project imports
from connect import postgres_connection

@dataclass
class FeatureTable:
    feature:str
    data:pd.DataFrame

def load_document_vectors(path:str) -> pd.DataFrame:
    data = pd.read_csv(path, index_col="documentID")
    return data.rename(columns={"authorIDs":"author_id"})

def get_author_ids(doc_df:pd.DataFrame) -> np.ndarray:
    """Retrieves all author ids"""
    return doc_df.author_id.unique()

def create_author_vector(author_id:str, doc_df:pd.DataFrame) -> pd.Series:
    """Averages an author's document vectors to get an author vector"""
    author_document_vectors = doc_df.loc[doc_df['author_id'] == author_id]
    return author_document_vectors.mean(axis=0, numeric_only=True)

def create_author_vector_df(doc_df:pd.DataFrame) -> pd.DataFrame:
    """Creates author vectors by averaging each author's documents into one"""
    author_ids = get_author_ids(doc_df)
    author_ids_to_avs = {}
    for author_id in author_ids:
        author_ids_to_avs[author_id] = create_author_vector(author_id, doc_df)    
    av_df = pd.DataFrame(author_ids_to_avs).T
    return av_df.rename(columns={"authorIDs":"author_id"})

def create_feature_tables(df:pd.DataFrame, level:str) -> List[FeatureTable]:
    """Given a dataframe, create a new dataframe (wrapped in a FeatureTable instance) for each high level feature"""
    HIGH_LEVEL_FEATURES = ["pos_unigrams", 
                           "pos_bigrams", 
                           "letters", 
                           "emojis", 
                           "morph_tags", 
                           "dep_labels",
                           "punctuation", 
                           "func_words"]
    tables = []
    for feat_name in HIGH_LEVEL_FEATURES:
        data = df.filter(regex=f"{feat_name}")
        if level == "documents": 
            data.insert(0, "author_id", df["author_id"])

        tables.append(FeatureTable(feat_name, data))
    return tables

def create_postgres_tables(tables, dataset_name:str, level:str, index_label:str, engine) -> None:
    """Creates document and author level tables for all high level features"""
    for table in tables:
        table.data.to_sql(f"{dataset_name}_{level}_{table.feature}", 
                          engine, 
                          if_exists="replace",
                          index=True, 
                          index_label=index_label)
    

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n",
                        "--dataset_name",
                        required=True,
                        help="Name of dataset")
    parser.add_argument("-d",
                        "--document_vectors_path",
                        required=True,
                        help="Path to a dataset's generated document vectors")
    
    args = parser.parse_args()
    
    document_vectors = load_document_vectors(args.document_vectors_path).round(6)
    author_vectors = create_author_vector_df(document_vectors).round(6)
    
    document_tables = create_feature_tables(document_vectors, "documents")
    author_tables = create_feature_tables(author_vectors, "authors")
    
    import ipdb;ipdb.set_trace()
        
    create_postgres_tables(document_tables, 
                           args.dataset_name, 
                           "documents", 
                           "document_id",
                           postgres_connection)
    
    create_postgres_tables(author_tables, 
                           args.dataset_name, 
                           "authors",
                           "author_id",
                           postgres_connection)
    
if __name__ == "__main__":
    main()