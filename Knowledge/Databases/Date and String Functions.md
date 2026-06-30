---
type: concept
title: Date and String Functions
tags: [sql, database, oa, concepts]
---
# Date and String Functions

String and Date manipulation are among the most common requirements for generating business reports and debugging.

## Common String Functions
- **`SUBSTRING(string FROM pattern)`**: Extracts a substring based on a regular expression or index.
- **`CONCAT(str1, str2, ...)`**: Joins multiple strings.
- **`LENGTH(string)`**: Returns the number of characters.
- **`LOWER()` / `UPPER()`**: Case conversion.

## Common Date Functions
- **`CURRENT_DATE` / `NOW()`**: Gets the current date/time.
- **`EXTRACT(field FROM source)`**: Pulls out a specific part of a date (e.g., `EXTRACT(MONTH FROM date_col)`).
- **`DATE_TRUNC('precision', source)`**: Truncates a timestamp to a specific precision (e.g., beginning of the month).
- **Interval Math**: `date_col >= CURRENT_DATE - INTERVAL '30 days'`

## Example Usage
```postgresql
SELECT id, 
       SUBSTRING(email FROM '@(.*)$') as domain,
       EXTRACT(YEAR FROM created_at) as signup_year
FROM users
WHERE created_at >= CURRENT_DATE - INTERVAL '6 months';
```

## Why it's tested in OAs
Most real-world application data involves timestamps and raw text. Candidates must demonstrate they can clean, group, and filter by these native data types natively in SQL without needing a backend processing script.
