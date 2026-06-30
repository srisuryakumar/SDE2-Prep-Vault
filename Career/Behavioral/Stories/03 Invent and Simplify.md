---
type: star-story
story_id: 3
title: "Invent and Simplify — Content Localization"
amazon_lps: ["Invent and Simplify"]
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
Our content team was manually copying and pasting localized text strings into a giant JSON file, frequently making JSON syntax errors that broke the production build.

### Task
I needed to simplify this error-prone localization process so non-technical users couldn't break the build.

### Action
Instead of enforcing JSON linters, I invented a simpler workflow. I wrote a script that pulled data directly from a shared Google Sheet via API. The content team could just edit the spreadsheet (which they were comfortable with). During the CI/CD pipeline, my script would fetch the sheet, convert it to valid JSON, and inject it into the build.

### Result
Build failures due to syntax errors went to zero immediately. The content team's workflow time was cut in half, proving that the best technical solutions often remove the user from the code entirely.
