---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 9 — Trie"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, trie, fundamentals]
---

# Trie (Prefix Tree) Fundamentals

## Intuition
A Trie is a tree where each node represents one character, and a path from the root represents a **prefix** shared by every word that passes through it. Words that share a prefix literally share the same nodes.

This turns "search across every word in a list" ($O(n \cdot m)$) into "walk down a fixed number of nodes" ($O(m)$), where $m$ is the word length. The search time is completely independent of $n$ (the number of words stored).

## Node Structure
```java
class TrieNode {
    TrieNode[] children = new TrieNode[26]; // One slot per possible next letter
    boolean isEndOfWord = false; // TRUE only at nodes where a full word ends
}
```

## Basic Operations
- **Insert:** Walk down character by character. If a child doesn't exist, create it. After the last character, mark `isEndOfWord = true`.
- **Search (Exact Match):** Walk down. If a child is missing, return false. At the end, return `node.isEndOfWord`.
- **StartsWith (Prefix Match):** Identical to Search, but return `true` immediately if the traversal finishes without hitting a null (don't check `isEndOfWord`).

```java
class Trie {
    private TrieNode root = new TrieNode();

    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            if (curr.children[c - 'a'] == null) curr.children[c - 'a'] = new TrieNode();
            curr = curr.children[c - 'a'];
        }
        curr.isEndOfWord = true;
    }

    public boolean search(String word) {
        TrieNode node = traverse(word);
        return node != null && node.isEndOfWord; // Must be a complete word
    }

    public boolean startsWith(String prefix) {
        return traverse(prefix) != null; // Path just needs to exist
    }

    private TrieNode traverse(String s) {
        TrieNode curr = root;
        for (char c : s.toCharArray()) {
            if (curr.children[c - 'a'] == null) return null;
            curr = curr.children[c - 'a'];
        }
        return curr;
    }
}
```
