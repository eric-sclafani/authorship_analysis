from scipy.stats import zscore

# project imports
from .processing import author_vectors, authors_df


def get_threshold_zscores_idxs(zscores, threshold:float):
    """Gets indices for |zscores| that meet a threshold"""
    selected = []
    for i, zscore in enumerate(zscores):
        if abs(zscore) > threshold:
            selected.append(i)
    return selected

def get_author_identifying_features(author_id:str, threshold=2.0):
    """
    Given an author, calculates their zscores for all features and selects the ones that deviate the most from the 
    mean. These features are what separate this author from the average author
    """
    zscores = zscore(author_vectors)
    author_idx = authors_df.loc[authors_df["author_id"] == author_id].index[0]
    author_zscores = zscores.iloc[author_idx]
    selected_zscores = get_threshold_zscores_idxs(author_zscores, threshold)
    return author_zscores.iloc[selected_zscores]




