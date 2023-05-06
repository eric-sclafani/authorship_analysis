import pandas as pd
from dash import dash_table
import spacy

# project imports
from .processing import get_author_entries, get_author_id

nlp = spacy.load("en_core_web_md")

def data_table(clicked_author):
    

    author_id = get_author_id(clicked_author)
    author_entries = get_author_entries(author_id)
        
    

def default_table():
    pass