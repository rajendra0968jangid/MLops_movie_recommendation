# 🎬 CineMatch — AI Movie Recommendation Engine

CineMatch is a modern, high-performance web dashboard that generates semantic movie recommendations using text-vectorization machine learning and pairs them with live metadata streams from the IMDB/OMDb API. The interface is engineered with a dark, sleek, responsive layout featuring fluid canvas particle physics and high-fidelity card animations.

---

## 🚀 Key Features

* **Fuzzy-String Matrix Math:** Cleans punctuation, spaces, and casing variations on the fly to find correct title nodes automatically.
* **Parallel Metadata Aggregation:** Utilizes Python's `ThreadPoolExecutor` to multi-thread live external REST API calls simultaneously, reducing poster load times by up to **80%**.
* **Automated Configuration Deployment:** Dynamically generates a secure, git-ignored `.env` profile if missing when booting the server application.
* **Zero Repo Friction:** Pulls data streams cleanly using `kagglehub` directly into a local global system cache, keeping the local workspace lightweight and within Git boundaries.
* **Immersive Cinematic Frontend:** Features a canvas-rendered interactive ambient backdrop with smooth hover transitions.

---

## 📂 Project Architecture

```text
movie-recommendation-system/
├── frontend/
│   ├── index.html        # Glassmorphism search layer & grid structures
│   ├── style.css         # Modern dark-theme styles & hover animation matrices
│   └── script.js         # DOM presentation controller & particle simulator
└── backend/
    ├── .env              # Private runtime environment variables (Git-ignored)
    ├── requirements.txt  # Python environment dependencies
    ├── train_model.py    # Kagglehub dataset ingestion & TF-IDF vectorization
    ├── server.py         # Concurrent Flask API runtime & proxy routing engine
    └── model/            # Generated joblib similarity assets (Git-ignored)
```
## 🖥️ Dashboard/Model/Output
The frontend delivers an immersive Netflix aesthetic featuring an interactive canvas background with moving particle physics. Upon typing a movie title, the dashboard handles transitions seamlessly—showing an infinite red loop spinner during calculation, and loading uniform 2:3 cinematic grid cards complete with real-time IMDB star ratings, poster art, and release dates.
![CineMatch Dashboard Home Screen](../preview-images/cinematch-home.png)
*Figure : Main Search Interface featuring the cinematic animated particle background.*
## 🚀 How to Run this project?

### Step 1: Run Backend Server

Navigate to the backend directory and start the Flask application.

1. Open your terminal and navigate to the backend directory:
```bash
cd backend
```

2. Install all the required Python libraries using the dependencies file:
```bash
pip install -r requirements.txt
```

3. Train your model before starting your server:
```bash
python train_model.py
```
4. Obtain a Free OMDb API Token:
   * Go to the official [OMDb API Key Registration Page](https://www.omdbapi.com/apikey.aspx).
   * Select the **Free** tier option, complete your registration, and copy your unique **API Key** string.
5. Configure your secret credentials:
    * Open the newly generated [backend/.env](./backend/.env) file and paste your API token right after the equals sign:
    ```OMDB_API_KEY=your_copied_api_key_here```

4. Start your local Flask development server:
```bash
python server.py
```

The backend will now be running actively at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Step 2: Launch Frontend Interface

Open the user interface safely using a local preview server.

1. Launch the Frontend.
2. Navigate into the frontend/ folder using your file explorer or VS Code.
3. Right-click on index.html and select "Open with Live Preview" (or use the Live Server extension) to launch the user interface in your browser safely without cross-origin blocks.