# Career Hub Dashboard

## Behavioral and Leadership
- [[_STAR Stories MOC|STAR Stories]]
- [[Amazon LP Mapping]]

### Target Companies
```dataview
TABLE tier as Tier, base_salary_range as "Base Salary Range"
FROM "Career/Companies"
WHERE type = "company-dossier"
SORT tier ASC
```

### LinkedIn Content Pipeline
```dataview
TABLE scheduled_week as Week, scheduled_day as Day, status
FROM "Career/LinkedIn Content/Posts"
WHERE type = "linkedin-post"
SORT post_number ASC
```

### Networking Contacts
```dataview
TABLE company, role, connection_date as "Connected", follow_up_date as "Follow Up"
FROM "Career/Networking/Contacts"
WHERE type = "contact"
SORT follow_up_date ASC
```

### Active Negotiations
```dataview
TABLE company, base, bonus, esop, deadline, status
FROM "Career/Negotiation/Offers"
WHERE type = "offer-tracker"
SORT deadline ASC
```
