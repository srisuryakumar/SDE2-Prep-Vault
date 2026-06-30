---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 6 — Developer Environment, Git, and Tooling"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, tooling, git]
---

# Git Internals and Workflow

## Git Objects
Git stores data as content-addressed objects:
- **BLOB:** File content (just bytes, no filename).
- **TREE:** A directory mapping filenames to blob/tree SHAs.
- **COMMIT:** A snapshot pointing to a root tree, parent commit, author, and message.
- **TAG:** A named pointer to a commit.
A **branch** is just a file containing the SHA of the latest commit on that branch.

## The Three States
1. **Working Directory:** Files on disk.
2. **Staging Area (Index):** Changes ready to be committed. `git add` moves changes here. (Use `git add -p` for interactive patch staging).
3. **Repository:** Committed history. `git commit` takes what is staged and creates a commit.

## Merge vs Rebase
- **Merge:** Creates a merge commit that joins two histories together. Preserves parallel development history.
- **Rebase:** Rewrites your branch's commits on top of another branch (like `main`), creating a linear history. Use interactive rebase (`git rebase -i`) to squash and clean up commits before opening a Pull Request.
