# Weak Topics & Spaced Repetition

## Spaced Repetition Logic

When you revisit a LeetCode problem, you must manually update the frontmatter properties. Follow these steps:

1. Update `last_reviewed` to today's date (e.g., `YYYY-MM-DD`).
2. Increment the `review_count` by 1.
3. Set `next_review_due` using the following interval table based on the new `review_count`:
   - **1st review:** +3 days
   - **2nd review:** +7 days
   - **3rd review:** +14 days
   - **4th review:** +30 days
   - **5th review and beyond:** +60 days

*Note: This is a manual frontmatter edit each time. You may choose to extend this later with a Templater button if desired.*
