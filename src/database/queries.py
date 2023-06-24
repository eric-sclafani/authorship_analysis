import pandas as pd
from typing import List

from connect import postgres_connection


def select(query:str):
    """Executes a given SELECT query"""
    with postgres_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
def select_checklist_features(features:List[str],
                              dataset_name:str
                              ):
    levels = ["authors", "documents"]
    return select(f"""--sql
                  SELECT * FROM {dataset_name}_documents_dep_labels
                  LIMIT 5;""")
    
    
   
   
print(select_checklist_features(["pos_unigrams", "pos_bigrams"], "pan2022")) 