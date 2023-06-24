from sqlalchemy import create_engine
from typing import Dict
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
        
params = config()
postgres_connection = create_engine(
"{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}".format(
    dialect="postgresql",
    driver="psycopg2",
    username=params["user"],
    password=params["password"],
    host=params["host"],
    port=params["port"],
    database=params["database"]
    )
)