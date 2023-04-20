
from wordcloud import WordCloud
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

# project
from .processing import text_docs_df


# create an img through matplotlib and load using ploty in Dash

def make_wc(author_id:str) -> None:
    """
    Generates a wordcloud from an authors documents and saves it to disk in a temp directory
    
    NOTE: everytime a new author is hovered over, I need to delete the old image
    """
    
    author_docs = text_docs_df