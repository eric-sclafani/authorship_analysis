from sklearn.manifold import MDS, TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)


#~~~Data~~~

authors_df = pd.read_csv("data/features/author_vectors.csv")
author_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("MDS", MDS())
    ])
author_vectors = authors_df.loc[:, ~authors_df.columns.isin(['author_id'])]
processed_author_vectors = author_pipeline.fit_transform(author_vectors)
author_kmeans = KMeans(n_clusters=6, random_state=42)
author_kmeans.fit(processed_author_vectors) 

docs_df = pd.read_csv("data/features/document_vectors.csv")
doc_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("PCA", PCA(n_components=50)),
    ("TSNE", TSNE())
    ])
doc_vectors = docs_df.loc[:, ~docs_df.columns.isin(['doc_id', 'author_id'])]
processed_doc_vectors = doc_pipeline.fit_transform(doc_vectors)
doc_kmeans = KMeans(n_clusters=6, random_state=42)
doc_kmeans.fit(processed_doc_vectors)

# averaged author vector; compare author vectors to this vector
avg_author_vector = author_vectors.mean()