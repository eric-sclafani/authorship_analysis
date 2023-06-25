#!/usr/bin/env python3

# this script contains functions for converting corpora of different formats into a standard jsonlines format

import pandas as pd
import numpy as np
import uuid
import os

def load_csv(path:str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_txt(path:str) -> pd.DataFrame:
    pass

def get_unique_author_ids(df:pd.DataFrame, identifier:str):
    return df[identifier].unique()

def main():
    
    blogs_raw = load_csv("../../data/blogs/blogtext.csv")
    ids = get_unique_author_ids(blogs_raw, "id")




if __name__ == "__main__":
    main()