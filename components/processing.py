from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)


#~~~Author level data~~~
authors_df = pd.read_csv("data/features/author_vectors.csv")
author_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("MDS", MDS())
    ])
author_vectors = authors_df.loc[:, ~authors_df.columns.isin(['author_id'])]
processed_author_vectors = author_pipeline.fit_transform(author_vectors)
author_kmeans = KMeans(n_clusters=6, random_state=42)
author_kmeans.fit(processed_author_vectors) 

# averaged author vector; compare author vectors to this vector
avg_author_vector = author_vectors.mean()

#~~~Document level data~~~
docs_df = pd.read_csv("data/features/document_vectors.csv")
doc_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("PCA", PCA(n_components=50)),
    ("TSNE", TSNE())
    ])
doc_vectors = docs_df.loc[:, ~docs_df.columns.isin(['doc_id', 'author_id'])]
processed_doc_vectors = doc_pipeline.fit_transform(doc_vectors)

# unvectorized text documents (data is not publicly available, so I cannot version control it)
text_docs_df = pd.read_json("data/documents/pan22_preprocessed.jsonl", lines=True)

