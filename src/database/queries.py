import pandas as pd
from typing import List

from connect import postgres_connection


def retrieve_all_columns(dataset_name:str, 
                         level:str, 
                         feature:str) -> pd.DataFrame:
    """Given the name, level, and feature of a table, retrieve all columns from that table"""
    query = f"SELECT * FROM {dataset_name}_{level}_{feature};"
    with postgres_connection.connect() as connection:
        index = "document_id" if level == "documents" else "author_id"
        return pd.read_sql_query(query, connection, index_col=index)
    
def select_features_from_checklist(features:List[str], dataset_name:str
                                   ):
    docs_df = pd.DataFrame()
    author_df = pd.DataFrame()
    
    for feature in features:
        docs = retrieve_all_columns(dataset_name, "documents", feature)
        authors = retrieve_all_columns(dataset_name, "authors", feature)
        
        import ipdb;ipdb.set_trace()
                
    
    
    
    
   
   
select_features_from_checklist(["pos_unigrams", "pos_bigrams"], "pan2022")