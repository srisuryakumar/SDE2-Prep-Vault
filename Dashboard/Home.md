# SDE-2 Prep — Home

## Today
[Update this line manually each morning — do not rely on auto-date-detection, since slipped days make calendar-based "today" unreliable]
## Today: [[Day 001]]

## This Week
```dataview
TABLE status, planned_date
FROM "Daily Journal"
WHERE week_number = 1
SORT day_number ASC
```
*(Note: replace `1` with the actual current week number manually if Dataview's this context doesn't resolve correctly outside a templated note — verify and adjust.)*

## Problems Solved
```dataview
TABLE length(rows) as "Count"
FROM "Practice/LeetCode"
WHERE type = "leetcode-problem"
GROUP BY status
```

## Revision Due Today
```dataview
TABLE next_review_due, review_count
FROM "Practice/LeetCode"
WHERE next_review_due <= date(today) AND status != "mastered"
SORT next_review_due ASC
```

## Upcoming Mocks
```dataview
TABLE mock_type, date
FROM "Practice/Mocks"
WHERE date >= date(today) OR date = null
SORT date ASC
LIMIT 5
```

## Application Pipeline
```dataview
TABLE company, role, status, interview_date
FROM "Career/Applications"
SORT date_applied DESC
```

## Quick Links
- **Dashboards:** [[Progress Overview]], [[Application Tracker]], [[Revision Due]]
- **Hubs:** [[_Knowledge MOC]], [[_LeetCode MOC]], [[_Practice MOC]], [[_Career MOC]], [[_Templates MOC]]
- **Current:** [[Day 000]], [[Day 001]], [[Week 01 Review]]
