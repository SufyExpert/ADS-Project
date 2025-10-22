Question 1 (Design Scenario — 45 marks)
Scenario:
You are tasked to build a movie streaming platform backend. The platform must store:
•	Movies (title, release year, genres, cast, director, rating)
•	Users (name, email, subscription type)
•	Watch history (user, movie, timestamp, watch duration)
•	Reviews (user, movie, rating, text review)
•	Search functionality:
o	Keyword search (by title, director, cast)
o	Similarity search (typos like "Godfathe" → "The Godfather")
o	Hybrid search that ranks results using:
	Title similarity
	Average rating
	Popularity (watch count)
Tasks:
1)	Design MongoDB schema (with relationships, nested docs for cast/genres).


1.	Movies Collection:

Purpose: Stores all information about a single movie. It utilizes nested documents for rich, self-contained data.
```json
{
  "_id": "ObjectId",
  "title": "String",
  "release_year": "Number",
  "director": "String",
  "rating": "Number",
  "genres": [ "String" ],
  "cast": [
    {
      "actor": "String",
      "role": "String"
    }
  ]
}```

Nesting Detail:
•	genres: An array of strings to allow for multiple genres per movie.
•	cast: An array of nested documents, where each document contains the actor and their specific role in the movie.

2.	Users Collection:
Purpose: Stores information for each unique user account.
```json
{
  "_id": "ObjectId",
  "name": "String",
  "email": "String",
  "subscription_type": "String"
}
Watch History Collection:
Purpose: Establishes a relationship between a user and a movie they have watched. This collection is designed to record each watch event.
code
JSON
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "movie_id": "ObjectId",
  "timestamp": "ISODate",
  "watch_duration_minutes": "Number"
}
Relationship Detail:
• user_id: A reference to the _id of a document in the users’ collection.
• movie_id: A reference to the _id of a document in the movies collection.
Reviews Collection:
Purpose: Establishes a relationship between a user, a movie, and the review content they submitted.
code
JSON
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "movie_id": "ObjectId",
  "rating": "Number",
  "text_review": "String",
  "timestamp": "ISODate"
}
Relationship Detail:
• user_id: A reference to the _id of a document in the users collection.
• movie_id: A reference to the _id of a document in the movies collection.
Visual Representation:
Propose indexes for multi-field search.
The databases use indexes to find documents faster, so it doesn't have to look through every single document in the collection. In our scenario we will use following indexes:
• Index for Keyword and Similarity Search: A single Text Index on the movies collection that includes all fields relevant to keyword searching. It allows users to type a search term and find matches in the movie's title, director's name, or cast members.
code
JavaScript
db.movies.createIndex({
  "title": "text",
  "director": "text",
  "cast.actor": "text"
})
• Index for Hybrid Search Ranking & Filtering: A Compound Index on the movies collection that includes fields used for ranking and sorting search results. The hybrid search must not only find movies but also rank them by rating and popularity. While the Text Index finds the initial set of movies, this compound index makes the process of sorting that set by rating or release_year extremely fast.
code
JavaScript
db.movies.createIndex({
  "rating": -1,
  "release_year": -1
})
-1 is to represent the descending order of data!
• Index for User History Retrieval: A Single Field Index on the user_id field in the watch_history collection. This index is critical for the /users/<id>/history API.
code
JavaScript
db.watch_history.createIndex({
  "user_id": 1
})
1 is to represent the descending order of data!
• Index for Movie Reviews Retrieval: A Single Field Index on the movie_id field in the reviews collection. Similar to the history index, this directly supports the /movies/<id>/reviews API.
code
JavaScript
db.reviews.createIndex({
  "movie_id": 1
})
Sketch APIs for:
a. /movies/search?query=...
Performs a weighted search for movies based on a query string, with support for pagination. The response is an aggregation of data from the movies, reviews, and watch_history collections.
• Endpoint:
GET /movies/search?query=...&limit=10&offset=0
• URL Structure Breakdown:
• /movies/search: The static path that identifies the search resource.
• ?: Separates the path from the query parameters.
• query=...: A key-value pair for the search term.
• &: Separates multiple query parameters.
• Query Parameters:
• query (string, required): The search term.
• limit (integer, optional, default: 10): Max items per page.
• offset (integer, optional, default: 0): Items to skip for pagination.
• Success Response:
code
JSON
{
  "items": [
    {
      "id": "ObjectId",
      "title": "String",
      "releaseYear": "Number",
      "director": "String",
      "genres": [ "String" ],
      "overallRating": "Number",
      "popularity": {
        "watchCount": "Number"
      },
      "score": "Number"
    }
  ],
  "nextOffset": "Number"
}
b. /users/<id>/history
Retrieves the paginated watch history for a specific user. The response joins data from watch_history and movies to be more user-friendly.
• Endpoint:
GET /users/<id>/history
• URL Structure Breakdown:
• <id>: A path parameter placeholder for the user's unique ObjectId.
• Path Parameters:
• id (string, required): The unique ObjectId of the user.
• Query Parameters:
• limit (integer, optional, default: 20): Max items per page.
• offset (integer, optional, default: 0): Items to skip for pagination.
• Success Response:
code
JSON
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
c. /movies/<id>/reviews
Retrieves all reviews for a specific movie, with support for pagination. The response joins data from reviews and users.
• Endpoint:
GET /movies/<id>/reviews
• URL Structure Breakdown:
• <id>: A path parameter placeholder for the movie’s unique ObjectId.
• Path Parameters:
• id (string, required): The unique ObjectId of the movie.
• Query Parameters:
• limit (integer, optional, default: 10): Max items per page.
• offset (integer, optional, default: 0): Items to skip for pagination.
• Success Response:
code
JSON
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
Write one aggregation query: “Top 5 most-watched movies in the last month.”
The logic is the same regardless of the programming language you use to run it.
code
JavaScript
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
    $sort: {
      watchCount: -1
    }
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
