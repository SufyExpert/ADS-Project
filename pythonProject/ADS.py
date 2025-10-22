from datetime import timedelta, datetime
from flask import Flask, request, jsonify, render_template_string
from pymongo import MongoClient, TEXT
from bson.objectid import ObjectId
from sentence_transformers import SentenceTransformer
import numpy as np

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')

client = MongoClient("mongodb+srv://sufyexpert:Fvj.7A5y%23Fc3-Fi@ads.ht4thba.mongodb.net/movie_platform")
db = client.movie_platform

db.movies.create_index([("title", TEXT), ("director", TEXT), ("cast.actor", TEXT)])

def fix_id(movies):
    return [{**m, "_id": str(m["_id"])} for m in movies]

def convert_objectid(doc):
    if isinstance(doc, list): return [convert_objectid(d) for d in doc]
    if isinstance(doc, dict): return {k: convert_objectid(v) for k, v in doc.items()}
    if isinstance(doc, ObjectId): return str(doc)
    return doc

@app.route('/')
def home():
    return render_template_string("Hello, Sufyan here!")

@app.route('/users/<id>/history')
def get_user_history(id):
    try:
        history = list(db.watch_history.find({"user_id": ObjectId(id)}))
        return jsonify(convert_objectid(history))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/movies/<id>/reviews')
def get_movie_reviews(id):
    try:
        reviews = list(db.reviews.find({"movie_id": ObjectId(id)}))
        return jsonify(convert_objectid(reviews))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/movies/top-watched")
def top_watched_movies():
    last_30 = datetime.utcnow() - timedelta(days=30)
    pipeline = [
        {"$match": {"timestamp": {"$gte": last_30}}},
        {"$group": {"_id": "$movie_id", "watch_count": {"$sum": 1}}},
        {"$sort": {"watch_count": -1}}, {"$limit": 5},
        {"$lookup": {"from": "movies", "localField": "_id", "foreignField": "_id", "as": "movie"}},
        {"$unwind": "$movie"},
        {"$project": {"movie_id": "$_id", "title": "$movie.title", "release_year": "$movie.release_year", "watch_count": 1, "_id": 0}}
    ]
    return jsonify(convert_objectid(list(db.watch_history.aggregate(pipeline))))

@app.route('/movies/search/basic')
def search_movies_basic():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "query missing"}), 400
    results = list(db.movies.find({"$text": {"$search": query}}, {"score": {"$meta": "textScore"}})
                   .sort([("score", {"$meta": "textScore"})]))
    return jsonify(convert_objectid(results))

@app.route('/movies/search/hybrid')
def search_movies_hybrid():
    q = request.args.get('query')
    if not q:
        return jsonify({"error": "query missing"}), 400

    movies = list(db.movies.find({}))
    qv = model.encode(q)
    res = []

    for m in movies:
        title = m.get("title", "")
        tv = model.encode(title)
        sem = np.dot(qv, tv) / (np.linalg.norm(qv) * np.linalg.norm(tv))
        key = len(set(q.lower().split()) & set(title.lower().split())) / max(len(q.split()), 1)
        score = 0.8 * sem + 0.2 * key
        res.append((score, m))

    res.sort(reverse=True, key=lambda x: x[0])
    return jsonify(fix_id([m for _, m in res[:10]]))

@app.route('/movies/search')
def search_movies_ranked():
    q = request.args.get('query')
    if not q:
        return jsonify({"error": "query missing"}), 400

    movies = list(db.movies.find({}))
    qv = model.encode(q)
    scores = []

    for m in movies:
        title = m.get("title", "")
        tv = model.encode(title)
        sim = np.dot(qv, tv) / (np.linalg.norm(qv) * np.linalg.norm(tv))
        rate = m.get("rating", 0) / 10
        pop = db.watch_history.count_documents({
            "movie_id": m["_id"],
            "timestamp": {"$gte": datetime.utcnow() - timedelta(days=30)}
        })
        pop = min(pop / 10, 1)
        score = 0.5 * sim + 0.3 * rate + 0.2 * pop
        scores.append((score, m))

    scores.sort(reverse=True, key=lambda x: x[0])
    return jsonify(fix_id([m for _, m in scores[:10]]))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
