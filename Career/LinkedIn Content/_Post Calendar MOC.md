# LinkedIn Post Calendar

```dataview
TABLE scheduled_week as Week, scheduled_day as Day, status
FROM "Career/LinkedIn Content/Posts"
WHERE type = "linkedin-post"
SORT post_number ASC
```
