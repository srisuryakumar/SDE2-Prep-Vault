---
type: index
title: Mocks MOC
tags: [mock, index]
---
# Mocks Index

This table aggregates all mock interviews scheduled or completed, helping you track your score trend over time.

```dataview
TABLE 
  date as Date,
  mock_type as "Mock Type",
  score as Score,
  related_day as "Day Scheduled"
FROM "Practice/Mocks"
WHERE type = "mock-interview"
SORT date ASC, file.name ASC
```
