from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random
from typing import List, Dict
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

# project
from processing import text_docs_df


#~~~Helpers~~~

def _get_author_documents(author_id:str) -> List[str]:
    """returns an author's list of documents"""
    return text_docs_df.loc[text_docs_df["authorIDs"] == author_id]["fullText"]

def _fit_vectorizer(documents:List[str]) -> TfidfVectorizer:
    """Fits a TFIDF vectorizer to a list of documents"""
    tfidf = TfidfVectorizer(max_features=100, max_df=.2)
    tfidf.fit(documents)
    return tfidf

def _get_author_tfidf_words(tfidf:TfidfVectorizer) -> str:
    """Retrieves the fit TFIDF vocab words as a space delimited string for wordcloud generation"""
    author_tfidf_words = tfidf.get_feature_names_out().tolist()
    random.shuffle(author_tfidf_words) # prevent alphabetic sorting by np array
    author_tfidf_words = " ".join(author_tfidf_words)
    return author_tfidf_words

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
        words = _get_author_tfidf_words(tfidf)
        wc = WordCloud(background_color="white", max_font_size=50, max_words=150, width=800, height=600, colormap="tab10").generate(words)
        author_wordcloud_map[author_id] = wc
        
    return author_wordcloud_map
        
        
    
def retrieve_wc_given_author_id(author_id:str):
    """Retrieves the word cloud of an author"""
    
    
    
    
    
def main():
    
    if not Path("data/wordclouds/").exists:
        wordclouds = generate_all_wordclouds()
        save_wordclouds_to_disk(wordclouds)
        
    

if __name__ == "__main__":
    main()