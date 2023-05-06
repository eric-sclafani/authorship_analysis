import pandas as pd
import numpy as np
from typing import List

# project imports
from .processing import get_author_entries, get_author_id
from .processing import text_docs_df


def get_token_counts(documents:List[str]) -> List[int]:
    """Returns a list of token counts given a list of documents"""
    return [len(document.split()) for document in documents]

def data_table(clicked_author):
    
    author_id = get_author_id(clicked_author)
    author_entries = get_author_entries(author_id, type="docs")
    author_docs = author_entries["fullText"].to_list()
    token_counts = get_token_counts(author_docs)
    
    df = pd.DataFrame(
        {"Document count":[len(author_docs)], 
         "Total token count":[sum(token_counts)],
         "Mean token count":[round(np.mean(token_counts, axis=0),2)], 
         "Std token count":[round(np.std(token_counts, axis=0),2)]
        })
    return df.to_dict("records")    

def default_table():
    """Returns statistics across the whole corpus"""
    all_docs = text_docs_df["fullText"].to_list()
    token_counts = get_token_counts(all_docs)

    df = pd.DataFrame(
        {"Document count":[len(all_docs)], 
         "Total token count":[sum(token_counts)],
         "Mean token count":[round(np.mean(token_counts, axis=0),2)], 
         "Std token count":[round(np.std(token_counts, axis=0),2)]
        })

    
    return df.to_dict("records")    