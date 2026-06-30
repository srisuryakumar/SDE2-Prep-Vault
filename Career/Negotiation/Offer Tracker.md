---
type: offer-tracker
---
# Offer Tracker

```dataview
TABLE company, base, bonus, esop, deadline, status
FROM "Career/Negotiation/Offers"
WHERE type = "offer"
SORT deadline ASC
```
