---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 5 — NoSQL Fundamentals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [database, nosql, mongodb]
---

# MongoDB (Document Store)

## Intuition
MongoDB stores BSON (Binary JSON) documents. There is no fixed schema—each document in a collection can have a different shape. Related data is often *embedded* inside a document instead of normalized into separate tables, which avoids expensive JOINs.

## When to choose MongoDB
- Product catalogs (different attributes per category, e.g. Electronics has RAM, Furniture has dimensions).
- Content Management Systems (articles with variable structures).
- Event logs (each event type carries different fields).
- User-generated content where the schema evolves rapidly.

## Indexing
Just like PostgreSQL, MongoDB uses B-trees for indexing, and composite indexes follow the left-prefix rule.
```javascript
// Single field index
db.products.createIndex({ price: -1 });

// Compound index
db.orders.createIndex({ user_id: 1, created_at: -1 });

// Text index for full-text search
db.products.createIndex({ name: "text", description: "text" });
```

## Aggregation Pipeline
MongoDB's equivalent of `GROUP BY` and `JOIN`.
```javascript
db.orders.aggregate([
  { $match:  { status: "DELIVERED" } },                           // WHERE
  { $group:  { _id: "$user_id", total: { $sum: "$total_amount" } }}, // GROUP BY
  { $sort:   { total: -1 } },                                     // ORDER BY
  { $limit:  10 }                                                 // LIMIT
]);

// $lookup is the MongoDB equivalent of a JOIN
db.orders.aggregate([
  { $lookup: {
      from: "users", localField: "user_id", foreignField: "_id", as: "user"
  }}
]);
```
