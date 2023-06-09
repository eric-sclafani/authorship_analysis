import pandas as pd
from connect import postgres_connection


def load_csv(path:str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)

def load_jsonl(path:str) -> pd.DataFrame:
    return pd.read_json(path, lines=True)





def main():
    pass

if __name__ == "__main__":
    main()