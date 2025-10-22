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

```json
[
  {
    "movie_id": "635f10000000000000000003",
    "release_year": 2008,
    "title": "The Dark Knight",
    "watch_count": 4
  },
  {
    "movie_id": "635f10000000000000000006",
    "release_year": 2010,
    "title": "Inception",
    "watch_count": 3
  },
  {
    "movie_id": "635f10000000000000000007",
    "release_year": 1999,
    "title": "The Matrix",
    "watch_count": 3
  },
  {
    "movie_id": "635f10000000000000000004",
    "release_year": 1994,
    "title": "Pulp Fiction",
    "watch_count": 2
  },
  {
    "movie_id": "635f10000000000000000009",
    "release_year": 1980,
    "title": "Star Wars: Episode V - The Empire Strikes Back",
    "watch_count": 2
  }
]
```

Shows the most watched movies in the last 30 days.

### 🔹 Movie Reviews
`GET /movies/635f10000000000000000001/reviews`

```json
[
  {
    "_id": "68f881622d0a10988763dd63",
    "movie_id": "635f10000000000000000001",
    "rating": 10,
    "text_review": "An offer you can't refuse. One of the greatest films ever made.",
    "timestamp": "Wed, 15 Oct 2025 01:00:00 GMT",
    "user_id": "635f00000000000000000011"
  }
]
```

### 🔹 User Watch History
`GET /users/635f00000000000000000001/history`

```json
[
  {
    "_id": "68f881042d0a10988763dd46",
    "movie_id": "635f10000000000000000003",
    "timestamp": "Wed, 01 Oct 2025 20:00:00 GMT",
    "user_id": "635f00000000000000000001",
    "watch_duration_minutes": 152
  },
  {
    "_id": "68f881042d0a10988763dd4a",
    "movie_id": "635f10000000000000000006",
    "timestamp": "Sun, 05 Oct 2025 20:15:00 GMT",
    "user_id": "635f00000000000000000001",
    "watch_duration_minutes": 148
  },
  {
    "_id": "68f881042d0a10988763dd59",
    "movie_id": "635f10000000000000000002",
    "timestamp": "Mon, 20 Oct 2025 20:00:00 GMT",
    "user_id": "635f00000000000000000001",
    "watch_duration_minutes": 142
  }
]
```

## Example Queries
- `http://127.0.0.1:5000/movies/search/hybrid?query=thriller`
- `http://127.0.0.1:5000/movies/search?query=sci-fi`
- `http://127.0.0.1:5000/movies/top-watched`

## Expected Output
Each endpoint returns JSON containing matched movie info, scores, or user/review details depending on the route.
