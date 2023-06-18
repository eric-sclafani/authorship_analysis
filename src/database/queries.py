import pandas as pd
from typing import List

from connect import postgres_connection


def select(query:str):
    """Executes a given SELECT query"""
    with postgres_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
def select_checklist_features(dataset_name:str,
                              level:str, 
                              features:List[str]
                              ):
    pass