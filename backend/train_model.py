import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# 🛠️ AUTOMATED .ENV CREATOR (Moved here to prevent server restarts!)
if not os.path.exists(ENV_PATH):
    print("🔑 Local .env file missing! Creating secure configuration blueprint...")
    with open(ENV_PATH, "w") as env_file:
        env_file.write("OMDB_API_KEY=\n")
    print("✅ Local .env file initialized! You can now paste your OMDb API key inside it.")

try:
    import kagglehub
except ImportError:
    print("📦 Installing kagglehub companion package...")
    os.system("pip install kagglehub")
    import kagglehub

MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

print("📥 Fetching the raw TMDB Dataset archive via kagglehub...")
try:
    download_folder = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")
    csv_path = os.path.join(download_folder, "tmdb_5000_movies.csv")
    print(f"📂 Dataset successfully located in cache: {csv_path}")
except Exception as e:
    raise RuntimeError(f"Kagglehub download failed. Error: {e}")

print("📦 Loading and processing dataset content columns...")
df = pd.read_csv(csv_path, encoding="utf-8")

if 'id' in df.columns and 'movie_id' not in df.columns:
    df.rename(columns={'id': 'movie_id'}, inplace=True)

df['genres'] = df['genres'].fillna('')
df['overview'] = df['overview'].fillna('')
df['tags'] = df['overview'] + " " + df['genres']

movies_cleaned = df[['movie_id', 'title', 'tags']].copy()

print("🧮 Vectorizing text metadata via TF-IDF...")
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_cleaned['tags'])

print("📐 Calculating Cosine Similarity Matrix...")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

print("💾 Saving compressed joblib binary assets...")
joblib.dump(movies_cleaned, os.path.join(MODEL_DIR, "movies_list.pkl"), compress=3)
joblib.dump(cosine_sim, os.path.join(MODEL_DIR, "similarity_matrix.pkl"), compress=3)

print("✅ Movie Recommendation engine compiled successfully!")