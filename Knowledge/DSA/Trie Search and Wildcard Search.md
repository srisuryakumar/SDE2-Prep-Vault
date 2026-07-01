---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 9 — Trie"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [dsa, pattern, trie, wildcard-search]
---

# Trie Search and Wildcard Search

## Intuition
When searching a Trie with a wildcard character `.` that can match *any single character*, the simple linear-walk traversal breaks. A `.` genuinely branches into up to 26 possibilities. This requires **recursion/backtracking**, not a simple loop.

## Template
```java
public boolean search(String word) {
    return searchHelper(word, 0, root);
}

private boolean searchHelper(String word, int index, TrieNode node) {
    if (node == null) return false;
    if (index == word.length()) return node.isEndOfWord;

    char c = word.charAt(index);
    if (c == '.') {
        // Wildcard: Try EVERY child
        for (TrieNode child : node.children) {
            if (searchHelper(word, index + 1, child)) {
                return true;
            }
        }
        return false;
    } else {
        // Normal character
        return searchHelper(word, index + 1, node.children[c - 'a']);
    }
}
```
**Complexity:** $O(m)$ without wildcards, but $O(26^d)$ worst case, where $d$ is the number of wildcards in the query. It is exponential in the wildcard *count*, not the word length overall.
