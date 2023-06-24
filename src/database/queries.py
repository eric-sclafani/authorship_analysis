import pandas as pd
from typing import List, Tuple

from .connect import postgres_connection


def retrieve_all_entries(dataset_name:str, 
                         level:str, 
                         feature:str) -> pd.DataFrame:
    """Given the name, level, and feature of a table, retrieve all columns from that table"""
    query = f"SELECT * FROM {dataset_name}_{level}_{feature};"
    with postgres_connection.connect() as connection:
        index = "document_id" if level == "documents" else "author_id"
        return pd.read_sql_query(query, connection, index_col=index)
    
def remove_dupe_cols(df:pd.DataFrame) -> pd.DataFrame:
    return df.loc[:,~df.columns.duplicated(keep="first")].copy()

def combine_dfs(dfs:List[pd.DataFrame]) -> pd.DataFrame:
    df = pd.concat(dfs, axis=1)
    return remove_dupe_cols(df)
    
def select_features(features:List[str], 
                    dataset_name:str
                    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
    doc_dfs = []
    author_dfs = []
    for feature in features:
        doc_dfs.append(retrieve_all_entries(dataset_name, "documents", feature))
        author_dfs.append(retrieve_all_entries(dataset_name, "authors", feature))
    
    doc_df = combine_dfs(doc_dfs)
    author_df = combine_dfs(author_dfs)
    return doc_df, author_df