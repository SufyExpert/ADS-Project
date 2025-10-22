# README

## How to Run
1. Install dependencies:
   ```bash
   pip install flask pymongo sentence-transformers numpy
   ```
2. Run the app:
   ```bash
   python main.py
   ```
3. Open in browser or test with curl:
   ```bash
   http://127.0.0.1:5000
   ```

## API Usage

### 🔹 Basic Search
`GET /movies/search/basic?query=inception`

Searches movies by keyword (title, director, cast).

### 🔹 Hybrid Search (80% semantic + 20% keyword)
`GET /movies/search/hybrid?query=inception`

Ranks results using both:
- **Semantic similarity** (meaning)
- **Keyword overlap**

Example result (top 10):
```json
[
  {"title": "Inception", "rating": 9, "_id": "..."},
  {"title": "Interstellar", "rating": 8.8, "_id": "..."}
]
```

### 🔹 Ranked Search (Weighted Formula)
`GET /movies/search?query=action`

Ranks results by:
```
score = 0.5 * semantic + 0.3 * rating + 0.2 * popularity
```

### 🔹 Top 5 Watched
`GET /movies/top-watched`

Shows the most watched movies in the last 30 days.

### 🔹 Movie Reviews
`GET /movies/<movie_id>/reviews`

### 🔹 User Watch History
`GET /users/<user_id>/history`

## Example Queries
- `http://127.0.0.1:5000/movies/search/hybrid?query=thriller`
- `http://127.0.0.1:5000/movies/search?query=sci-fi`
- `http://127.0.0.1:5000/movies/top-watched`

## Expected Output
Each endpoint returns JSON containing matched movie info, scores, or user/review details depending on the route.
