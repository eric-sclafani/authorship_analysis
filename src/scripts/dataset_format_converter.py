#!/usr/bin/env python3

# this script contains functions for converting datasets into the desried jsonlines format
import pandas as pd
import os


def load_csv(path:str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_txt(path:str) -> pd.DataFrame:
    pass

def main():
    
    blogs_raw = load_csv("../data/blogs/blogtext.csv")
    



if __name__ == "__main__":
    main()