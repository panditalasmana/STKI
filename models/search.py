import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("dataset/laptop_dataset.csv")

# =========================
# PREPROCESSING FUNCTION
# =========================

def preprocessing(text):

    # CASE FOLDING
    text = text.lower()

    # REMOVE SYMBOL / PUNCTUATION
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # REMOVE EXTRA SPACE
    text = re.sub(r'\s+', ' ', text).strip()

    return text

# =========================
# APPLY PREPROCESSING
# =========================

df['combined'] = (
    df['nama_laptop'] + " " +
    df['deskripsi']
)

df['processed'] = df['combined'].apply(preprocessing)

# =========================
# TF-IDF
# =========================

vectorizer = TfidfVectorizer(
    stop_words='english'
)

tfidf_matrix = vectorizer.fit_transform(
    df['processed']
)

# =========================
# SEARCH FUNCTION
# =========================

def search_laptop(query):

    # PREPROCESS QUERY
    query = preprocessing(query)

    # TF-IDF QUERY
    query_vector = vectorizer.transform([query])

    # COSINE SIMILARITY
    similarity = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    # URUTKAN SIMILARITY
    top_indices = similarity.argsort()[::-1]

   # FILTER YANG SCORE > 0
    top_indices = [
         i for i in top_indices
       if similarity[i] > 0
      ][:10]

    results = []

    for rank, idx in enumerate(top_indices, start=1):

        results.append({

            "id": df.iloc[idx]["id"],

            "rank": rank,

            "nama": df.iloc[idx]["nama_laptop"],

            "harga": f"Rp {df.iloc[idx]['harga']:,}".replace(",", "."),

            "deskripsi": df.iloc[idx]["deskripsi"],

            "score": round(similarity[idx], 3),

            "image": df.iloc[idx]["image"]

        })

    return results