import psycopg2
from typing import Dict
from contextlib import contextmanager
from configparser import ConfigParser


def config(filename='database/database.ini', section='postgresql') -> Dict[str,str]:
    """Parses the postgres database.ini"""
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        return {param[0]:param[1] for param in params}
    else:
        raise Exception(f"Section {section} not found in the {filename} file")
    
@contextmanager
def postgres_connection():
    """Establishes a connection to a postgres database"""
    params = config()
    connection = psycopg2.connect(**params)
    try:
        yield connection
    finally:
        connection.close()
        
def select(query:str):
    """Executes a given SELECT query"""
    with postgres_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()