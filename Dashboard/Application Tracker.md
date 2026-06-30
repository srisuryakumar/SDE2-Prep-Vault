# Application Tracker

## Pipeline by Tier
```dataview
TABLE company, company.tier as Tier, role, status, interview_date, date_applied
FROM "Career/Applications"
WHERE type = "application"
SORT company.tier ASC, date_applied DESC
```
