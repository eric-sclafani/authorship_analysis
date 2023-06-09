#!/usr/bin/env python3
"""
This script is for making postgres tables for a dataset on the document and author levels
"""
import pandas as pd
import argparse
from sqlalchemy import create_engine

from typing import Dict

# project imports
from connect import config, postgres_connection
from create_author_vectors import make_author_vector_df


def load_document_vectors(path:str) -> pd.DataFrame:
    return pd.read_csv(path)


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
    
    # document_vectors = load_document_vectors(args.document_vectors_path)
    # author_vectors = make_author_vector_df(document_vectors)
    
    
    cfg = config()
    engine = create_engine(f'postgresql://{cfg["user"]}:{cfg["password"]}@{cfg["host"]}:{cfg["port"]}/{cfg["database"]}')
    df = pd.DataFrame({
        "col1":[1,2,3],
        "col2":[4,5,6],
        "col3":[7,8,9]
    })
    df.to_sql("test_table", engine, index=False, if_exists="replace")
    
    
    with postgres_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM test_table;")
        result = cursor.fetchall()
        print(result)

if __name__ == "__main__":
    main()