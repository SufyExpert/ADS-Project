# Question 2 — Movie Streaming Platform Backend

## Problem Definition
Design and implement the backend of a **Movie Streaming Platform** that stores, manages, and retrieves movie data, user activity, and reviews.  
The system must also support intelligent search and ranking mechanisms using both **semantic** and **keyword-based** matching.

---

## Objective
The goal is to build a **Flask-based REST API** connected with **MongoDB** that can:
- Manage movie information, user histories, and reviews.  
- Support both **basic** and **hybrid** search methods.  
- Rank movies dynamically based on similarity, rating, and popularity.  
- Provide structured, ready-to-use API endpoints for integration.

---

## System Description

### 1. Movie Management
Stores essential details for each movie:
- Title  
- Release Year  
- Genres  
- Cast and Director  
- Rating  

All movie fields are indexed for efficient search.

---

### 2. User Watch History
Tracks each user’s watched movies.  
Also supports analytics queries like:
> **Top 5 most-watched movies in the last 30 days**

---

### 3. Movie Reviews
Fetches reviews for any movie using its unique ID.  
This allows displaying audience feedback alongside each movie.

---

### 4. Search Functionalities

#### a. Basic Search
Uses MongoDB’s **full-text search** to find results by exact keywords.

#### b. Hybrid Search
Uses both **semantic similarity** and **word overlap** for more intelligent results.  
Weighted formula:
