---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 6 — Developer Environment, Git, and Tooling"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, tooling, git]
---

# Git Branch Protection and Force-With-Lease

## Branch Protection Rules
In professional teams, the `main` branch is protected. Branch protection rules enforce:
- **Require PRs:** Code must be reviewed; no direct pushes.
- **Require status checks:** CI pipelines (tests/builds) must pass before merging.
- **Dismiss stale approvals:** If new commits are pushed after approval, re-approval is required.
- **No force pushes:** History on shared branches cannot be rewritten.

## Force-With-Lease
When you rewrite history on a personal feature branch (e.g., via interactive rebase), you must force push to the remote. 
- **`git push --force`** is dangerous: it blindly overwrites the remote, silently destroying any commits teammates may have pushed.
- **`git push --force-with-lease`** is safe: it checks if the remote branch has changed since your last fetch. If someone else pushed to it, the push is rejected, preventing data loss. Never use `--force`; always use `--force-with-lease`.
