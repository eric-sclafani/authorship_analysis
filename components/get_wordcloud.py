from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random
from PIL import Image
from typing import List, Dict
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

# project
from .processing import text_docs_df, authors_df


#~~~Helpers~~~


def _get_author_id(author_index:int) -> str:
    """Gets the author id given a DataFrame index"""
    
    return authors_df.iloc[author_index].author_id if author_index is not None else "None"

def _get_author_documents(author_id:str) -> List[str]:
    """returns an author's list of documents"""
    return text_docs_df.loc[text_docs_df["authorIDs"] == author_id]["fullText"]

def _fit_vectorizer(documents:List[str]) -> TfidfVectorizer:
    """Fits a TFIDF vectorizer to a list of documents"""
    tfidf = TfidfVectorizer(max_features=100, max_df=.2)
    tfidf.fit(documents)
    return tfidf

def _get_tfidf_words(tfidf:TfidfVectorizer) -> str:
    """Retrieves the fit TFIDF vocab words as a space delimited string for wordcloud generation"""
    author_tfidf_words = tfidf.get_feature_names_out().tolist()
    random.shuffle(author_tfidf_words) # prevent alphabetic sorting by np array
    author_tfidf_words = " ".join(author_tfidf_words)
    return author_tfidf_words

def make_wc() -> WordCloud:
    """Instantiates a WordCloud object"""
    return WordCloud(background_color="white", max_font_size=50, max_words=150, width=800, height=600, colormap="tab10")

def save_wordclouds_to_disk(author_wc_maps:Dict[str, WordCloud]) -> None:
    """Saves all generated wordclouds to disk"""

    plt.figure(figsize=(16,9), facecolor='k')
    for author_id, wordcloud in author_wc_maps.items():
        path = f"data/wordclouds/{author_id}_wc.png"
        plt.imshow(wordcloud)
        plt.axis("off")  
        plt.savefig(path, facecolor='k', bbox_inches='tight') 

    
def generate_all_wordclouds() -> Dict[str, WordCloud]:
    """Creates wordclouds for all authors"""
    
    all_authors = text_docs_df.authorIDs.unique()
    author_wordcloud_map = {}
    for author_id in all_authors:
        author_docs = _get_author_documents(author_id)
        tfidf = _fit_vectorizer(author_docs)
        words = _get_tfidf_words(tfidf)
        wc = make_wc().generate(words)
        author_wordcloud_map[author_id] = wc
        
    return author_wordcloud_map

def generate_overall_tfidf_wc() -> WordCloud:
    """Generates the default TFIDF wordcloud which is aggregated from all documents"""
    all_docs = text_docs_df["fullText"]
    tfidf = _fit_vectorizer(all_docs)
    words = _get_tfidf_words(tfidf)
    return make_wc().generate(words)
        
    
def retrieve_wc_given_author(author_index:str) -> Image:
    """Retrieves the word cloud of an author"""
    
    author_id = _get_author_id(author_index)
    filenames = [str(file) for file in Path("data/wordclouds/").glob("*")]
    author_file = list(filter(lambda x: author_id in x, filenames))[0]

    return Image.open(author_file)
        
    
    
    
    
def main():
    
    if not Path("data/wordclouds/").exists:
        wordclouds = generate_all_wordclouds()
        save_wordclouds_to_disk(wordclouds)
    
    wordcloud = generate_overall_tfidf_wc()
    plt.figure(figsize=(16,9), facecolor='k')
    path = f"data/wordclouds/default_tfidf_wc.png"
    plt.imshow(wordcloud)
    plt.axis("off")  
    plt.savefig(path, facecolor='k', bbox_inches='tight') 

    

if __name__ == "__main__":
    main()