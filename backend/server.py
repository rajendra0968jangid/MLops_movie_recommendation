import os
import re
import joblib
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)
RAW_KEY = os.getenv("OMDB_API_KEY", "").strip()

# 🛠️ FOOLPROOF PARSING: Extract just the 8-character key if a user accidentally pasted a full URL
OMDB_API_KEY = RAW_KEY
if "apikey=" in RAW_KEY:
    # Use regular expressions to extract whatever characters follow 'apikey='
    match_key = re.search(r'apikey=([a-zA-Z0-9]+)', RAW_KEY)
    if match_key:
        OMDB_API_KEY = match_key.group(1)

app = Flask(__name__)
CORS(app)

MOVIES_PATH = os.path.join(BASE_DIR, "model", "movies_list.pkl")
SIMILARITY_PATH = os.path.join(BASE_DIR, "model", "similarity_matrix.pkl")

if not os.path.exists(MOVIES_PATH) or not os.path.exists(SIMILARITY_PATH):
    print("⚠️ Recommendation weights missing! Running train_model.py...")
    import train_model

movies_df = joblib.load(MOVIES_PATH)
similarity = joblib.load(SIMILARITY_PATH)

def normalize_string(text):
    return re.sub(r'[^a-zA-Z0-9]', '', str(text)).lower()

def fetch_omdb_data(movie_tuple):
    movie_id, title = movie_tuple
    poster_url = 'https://via.placeholder.com/300x450?text=No+Poster+Found'
    imdb_rating = 'N/A'
    release_year = 'N/A'
    
    if OMDB_API_KEY:
        try:
            omdb_url = f"https://www.omdbapi.com/?t={requests.utils.quote(title)}&apikey={OMDB_API_KEY}"
            omdb_response = requests.get(omdb_url, timeout=3).json()
            
            if omdb_response.get("Response") == "True":
                if omdb_response.get("Poster") and omdb_response.get("Poster") != "N/A":
                    poster_url = omdb_response.get("Poster")
                imdb_rating = omdb_response.get("imdbRating", "N/A")
                release_year = omdb_response.get("Year", "N/A")
            else:
                search_url = f"https://www.omdbapi.com/?s={requests.utils.quote(title)}&apikey={OMDB_API_KEY}"
                search_response = requests.get(search_url, timeout=3).json()
                if search_response.get("Response") == "True" and search_response.get("Search"):
                    first_match = search_response["Search"][0]
                    if first_match.get("Poster") and first_match.get("Poster") != "N/A":
                        poster_url = first_match.get("Poster")
                    release_year = first_match.get("Year", "N/A")
                    
                    id_url = f"https://www.omdbapi.com/?i={first_match['imdbID']}&apikey={OMDB_API_KEY}"
                    id_response = requests.get(id_url, timeout=2).json()
                    imdb_rating = id_response.get("imdbRating", "N/A")
        except Exception as e:
            print(f"OMDb fetch error for {title}: {e}")
    else:
        poster_url = f"https://via.placeholder.com/300x450?text={requests.utils.quote(title)}"

    return {
        "id": movie_id,
        "title": title,
        "poster": poster_url,
        "rating": imdb_rating,
        "year": release_year
    }

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    try:
        data = request.json
        user_movie = data.get('movie_title', '').strip()
        
        if not user_movie:
            return jsonify({"error": "Please enter a movie title!"}), 400
            
        normalized_user_input = normalize_string(user_movie)
        match = movies_df[movies_df['title'].apply(normalize_string) == normalized_user_input]
        
        if match.empty:
            match = movies_df[movies_df['title'].apply(normalize_string).str.contains(normalized_user_input)]
            
        if match.empty:
            return jsonify({"error": "Movie not found in database. Try another title!"}), 404
            
        movie_idx = match.index[0]
        distances = similarity[movie_idx]
        movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        
        movie_targets = [
            (int(movies_df.iloc[i[0]].movie_id), str(movies_df.iloc[i[0]].title)) 
            for i in movie_list
        ]
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            recommendations = list(executor.map(fetch_omdb_data, movie_targets))
            
        response_data = {"recommendations": recommendations}
        if not OMDB_API_KEY:
            response_data["warning"] = "OMDb API Key is missing in backend/.env. Running in offline mode without images."
            
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)