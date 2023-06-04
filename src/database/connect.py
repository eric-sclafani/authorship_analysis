import psycopg2
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    """Parses the postgres database.ini"""
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        return {param[0]:param[1] for param in params}
    else:
        raise Exception(f"Section {section} not found in the {filename} file")
    
def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute("""SELECT version()""")

        db_version = cur.fetchone()
        print(db_version)
       
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect()
    
    
