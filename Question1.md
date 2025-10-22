# Question 1 (Design Scenario --- 45 marks)

## Scenario:

You are tasked to build a movie streaming platform backend. The platform
must store:

-   **Movies** (title, release year, genres, cast, director, rating)
-   **Users** (name, email, subscription type)
-   **Watch history** (user, movie, timestamp, watch duration)
-   **Reviews** (user, movie, rating, text review)
-   **Search functionality:**
    -   Keyword search (by title, director, cast)
    -   Similarity search (typos like "Godfathe" → "The Godfather")
    -   Hybrid search that ranks results using:
        -   Title similarity
        -   Average rating
        -   Popularity (watch count)

------------------------------------------------------------------------

## 1) MongoDB Schema Design

### **Movies Collection**

``` json
{
  _id: ObjectId,
  title: String,
  release_year: Number,
  director: String,
  rating: Number,
  genres: [ String ],
  cast: [
    {
      actor: String,
      role: String
    }
  ]
}
```

**Nesting Detail:** - `genres`: Array of strings for multiple genres. -
`cast`: Nested array of `{ actor, role }` objects.

------------------------------------------------------------------------

### **Users Collection**

``` json
{
  _id: ObjectId,
  name: String,
  email: String,
  subscription_type: String
}
```

------------------------------------------------------------------------

### **Watch History Collection**

``` json
{
  _id: ObjectId,
  user_id: ObjectId,
  movie_id: ObjectId,
  timestamp: ISODate,
  watch_duration_minutes: Number
}
```

**Relationships:** - `user_id`: References `users._id` - `movie_id`:
References `movies._id`

------------------------------------------------------------------------

### **Reviews Collection**

``` json
{
  _id: ObjectId,
  user_id: ObjectId,
  movie_id: ObjectId,
  rating: Number,
  text_review: String,
  timestamp: ISODate
}
```

**Relationships:** - `user_id`: References `users._id` - `movie_id`:
References `movies._id`

------------------------------------------------------------------------

## 2) Proposed Indexes for Multi-Field Search

### **Keyword and Similarity Search**

``` js
db.movies.createIndex({
  "title": "text", 
  "director": "text", 
  "cast.actor": "text" 
})
```

### **Hybrid Search Ranking**

``` js
db.movies.createIndex({
  "rating": -1,
  "release_year": -1
})
```

### **User History Retrieval**

``` js
db.watch_history.createIndex({ "user_id": 1 })
```

### **Movie Reviews Retrieval**

``` js
db.reviews.createIndex({ "movie_id": 1 })
```

------------------------------------------------------------------------

## 3) API Sketches

### **a. /movies/search?query=...**

**GET /movies/search?query=...&limit=10&offset=0**

``` json
{
  "items": [
    {
      "id": "ObjectId",
      "title": "String",
      "releaseYear": "Number",
      "director": "String",
      "genres": ["String"],
      "overallRating": "Number",
      "popularity": { "watchCount": "Number" },
      "score": "Number"
    }
  ],
  "nextOffset": "Number"
}
```

------------------------------------------------------------------------

### **b. /users/`<id>`{=html}/history**

**GET /users/`<id>`{=html}/history**

``` json
{
  "items": [
    {
      "movieId": "ObjectId",
      "movieTitle": "String",
      "watchedOn": "ISODate",
      "watchDurationMinutes": "Number"
    }
  ],
  "nextOffset": "Number"
}
```

------------------------------------------------------------------------

### **c. /movies/`<id>`{=html}/reviews**

**GET /movies/`<id>`{=html}/reviews**

``` json
{
  "items": [
    {
      "reviewId": "ObjectId",
      "userId": "ObjectId",
      "userName": "String",
      "rating": "Number",
      "reviewText": "String",
      "submittedOn": "ISODate"
    }
  ],
  "nextOffset": "Number"
}
```

------------------------------------------------------------------------

## 4) Aggregation Query --- "Top 5 Most-Watched Movies in the Last Month"

``` js
db.watch_history.aggregate([
  {
    $match: {
      timestamp: {
        $gte: new Date(new Date().setDate(new Date().getDate() - 30))
      }
    }
  },
  {
    $group: {
      _id: "$movie_id",
      watchCount: { $sum: 1 }
    }
  },
  {
    $sort: { watchCount: -1 }
  },
  {
    $limit: 5
  },
  {
    $lookup: {
      from: "movies",
      localField: "_id",
      foreignField: "_id",
      as: "movieDetails"
    }
  }
])
```
