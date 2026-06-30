# Chapter 9: Trie (Prefix Tree)

*A small chapter with an outsized payoff: once you see that words sharing a prefix can share the same nodes, "search across every word in the list" quietly turns into "walk down a fixed number of nodes" — independent of how many words there are.*

## 9.1 What a Trie Is

A Trie (prefix tree) is a tree where each node represents one character, and a path from the root to any node represents a **prefix** shared by every word that passes through it. Words that share a prefix literally share the same nodes for that prefix — the sharing is the entire point.

```
Words stored: cat, car, card, dog

root
├── c
│   └── a
│       ├── t  (end: "cat")
│       └── r  (end: "car")
│           └── d  (end: "card")
└── d
    └── o
        └── g  (end: "dog")
```

Notice `car` and `card` share the `c → a → r` path entirely — `card` just continues one node further. That shared structure is what makes prefix queries fast.

## 9.2 Node Structure

```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];   // one slot per possible next letter
    boolean isEndOfWord = false;                // true only at nodes where a full word ends
}
```

(A `HashMap<Character, TrieNode>` works too, and is more flexible for an unknown or large character set — but a fixed-size array is faster and simpler when the alphabet is small and known, like lowercase English.)

## 9.3 Why a Trie: O(m) vs. O(n·m)

Store n words in a plain `HashSet<String>` and ask "does any word start with this prefix?" — you'd have to check the prefix against every one of the n words individually, each comparison costing up to O(m): **O(n·m)** total. A Trie answers the identical question by walking down exactly m nodes — one per character of the prefix — **O(m)** total, completely independent of how many words n are stored. That's the entire value proposition: turning "search across everything" into "walk down a fixed number of nodes."

## 9.4 Insert

Walk down character by character. If a child for the current character doesn't exist yet, create it. After the last character, mark that node as the end of a word.

```java
public void insert(String word) {
    TrieNode curr = root;
    for (char c : word.toCharArray()) {
        int idx = c - 'a';
        if (curr.children[idx] == null) {
            curr.children[idx] = new TrieNode();
        }
        curr = curr.children[idx];
    }
    curr.isEndOfWord = true;
}
```

## 9.5 Search

Walk down character by character. If any required child is missing, the word was never inserted — return false. If the walk completes, the word is present **only if** that final node is explicitly marked `isEndOfWord` — the path might exist purely as a *prefix* of some longer word, without ever having been inserted as a complete word itself.

```java
public boolean search(String word) {
    TrieNode node = traverse(word);
    return node != null && node.isEndOfWord;
}

private TrieNode traverse(String s) {
    TrieNode curr = root;
    for (char c : s.toCharArray()) {
        int idx = c - 'a';
        if (curr.children[idx] == null) {
            return null;
        }
        curr = curr.children[idx];
    }
    return curr;
}
```

## 9.6 StartsWith

The identical traversal as search — but **without** checking `isEndOfWord`. Only the path's existence matters.

```java
public boolean startsWith(String prefix) {
    return traverse(prefix) != null;
}
```

---

## Problem — Implement Trie (LeetCode 208)

**Full Implementation**, assembling everything above:

```java
class Trie {
    class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEndOfWord = false;
    }

    private TrieNode root;

    public Trie() {
        root = new TrieNode();
    }

    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) {
                curr.children[idx] = new TrieNode();
            }
            curr = curr.children[idx];
        }
        curr.isEndOfWord = true;
    }

    public boolean search(String word) {
        TrieNode node = traverse(word);
        return node != null && node.isEndOfWord;
    }

    public boolean startsWith(String prefix) {
        return traverse(prefix) != null;
    }

    private TrieNode traverse(String s) {
        TrieNode curr = root;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) return null;
            curr = curr.children[idx];
        }
        return curr;
    }
}
```

**Trace**, demonstrating exactly why `isEndOfWord` and "the path exists" are two different questions:

```
insert("apple"): builds root→a→p→p→l→e, marking isEndOfWord=true ONLY at the final 'e' node.

search("apple"):    reaches the 'e' node, isEndOfWord=true  → true    ✓
search("app"):      reaches the second 'p' node (root→a→p→p). isEndOfWord is FALSE
                     there — only the final 'e' node was ever marked  → false
startsWith("app"):  reaches that same 'p' node successfully (the path exists,
                     regardless of isEndOfWord)  → true

insert("app"):      walks the SAME existing path root→a→p→p (no new nodes needed —
                     they already exist from "apple"), and marks isEndOfWord=true
                     at that second 'p' node.

search("app"):      NOW returns true — the flag was just set.  → true   ✓
```

**Complexity:** insert/search/startsWith are all O(m), where m is the word/prefix length. Space is O(total characters across all inserted words) in the worst case with no shared prefixes — but shared prefixes (like "app" living inside "apple") are stored exactly **once**, which is the actual space payoff of using a Trie at all.

---

## Problem — Design Add and Search Words Data Structure (LeetCode 211)

**Statement.** Support `addWord(word)` and `search(word)`, where `search` may contain `.` as a wildcard matching *any single character*.

**Approach.** `addWord` is identical to `Trie.insert`. `search` needs a fundamentally different traversal: encountering `.` means trying **all 26** possible children at that position, not following one fixed path — which requires recursion/backtracking instead of a simple loop, since a single `.` branches the search into up to 26 parallel possibilities, any one of which might lead to a match.

```java
class WordDictionary {
    class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEndOfWord = false;
    }

    private TrieNode root;

    public WordDictionary() {
        root = new TrieNode();
    }

    public void addWord(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) {
                curr.children[idx] = new TrieNode();
            }
            curr = curr.children[idx];
        }
        curr.isEndOfWord = true;
    }

    public boolean search(String word) {
        return searchHelper(word, 0, root);
    }

    private boolean searchHelper(String word, int index, TrieNode node) {
        if (node == null) return false;
        if (index == word.length()) return node.isEndOfWord;

        char c = word.charAt(index);
        if (c == '.') {
            for (TrieNode child : node.children) {   // wildcard: try EVERY child
                if (searchHelper(word, index + 1, child)) {
                    return true;
                }
            }
            return false;
        } else {
            return searchHelper(word, index + 1, node.children[c - 'a']);
        }
    }
}
```

**Trace**, after `addWord("bad")`, `addWord("dad")`, `addWord("mad")` (three separate paths from root: `b→a→d`, `d→a→d`, `m→a→d`, each ending in `isEndOfWord=true`):

```
search("pad"): index0, char='p'. root has no 'p' child (no word starts with p)
               → fails immediately.   Result: false   ✓

search("b.."): 'b' → follow to b-node.  '.': wildcard — only child 'a' exists → recurse.
               '.': wildcard again — only child 'd' exists → recurse.  End of word,
               isEndOfWord at this d-node = true.   Result: true   ✓

search(".ad"): '.': wildcard — try ALL of root's children: b, d, m exist.
               Try 'b' first: 'a' exists under b, 'd' exists under that —
               end of word, isEndOfWord=true → SUCCESS, return immediately
               (no need to even try 'd' or 'm' as the wildcard match).
               Result: true   ✓
```

**Complexity:** `addWord` is O(m). `search` is O(m) when there are no wildcards, but O(26^d) worst case, where **d is the number of wildcards** in the query — exponential in wildcard *count*, not in word length overall. That distinction matters: typical inputs keep the number of `.` characters small even when words themselves are long.

---

## Problem — Word Search II (LeetCode 212) — Trie + Backtracking, the Hardest Trie Problem

**Statement.** Given an m×n board of letters and a list of words, find every word constructible from a path of sequentially adjacent cells (horizontally or vertically), never reusing a cell within one word.

**Why this needs both Trie and backtracking.** Searching independently for each word — a separate DFS over the whole board, once per word — costs roughly O(words × board cells × 4^word length), and re-explores every shared prefix from scratch, once per word that has it. The fix: insert **every** word into a single Trie first, then run **one** combined DFS over the board, walking the board path and the Trie path *simultaneously*. At each board cell, only continue exploring if the letters collected so far correspond to an existing Trie path — any path that doesn't match the start of *any* word in the list dies immediately, pruned for free. The moment the Trie path lands on a node marking a complete word, record it. Shared prefixes across multiple words get explored together exactly once, not once per word.

```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    String word = null;   // non-null exactly at the node completing a word — lets us
                            // grab the word directly, no need to rebuild it from the path
}

public List<String> findWords(char[][] board, String[] words) {
    TrieNode root = buildTrie(words);
    List<String> result = new ArrayList<>();
    int rows = board.length, cols = board[0].length;

    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            dfs(board, r, c, root, result);
        }
    }
    return result;
}

private TrieNode buildTrie(String[] words) {
    TrieNode root = new TrieNode();
    for (String word : words) {
        TrieNode curr = root;
        for (char ch : word.toCharArray()) {
            int idx = ch - 'a';
            if (curr.children[idx] == null) {
                curr.children[idx] = new TrieNode();
            }
            curr = curr.children[idx];
        }
        curr.word = word;
    }
    return root;
}

private void dfs(char[][] board, int r, int c, TrieNode node, List<String> result) {
    if (r < 0 || r >= board.length || c < 0 || c >= board[0].length) return;
    char ch = board[r][c];
    if (ch == '#' || node.children[ch - 'a'] == null) return;   // visited, or no matching Trie path

    TrieNode next = node.children[ch - 'a'];
    if (next.word != null) {
        result.add(next.word);
        next.word = null;   // prevent adding the same word twice via a different path
    }

    board[r][c] = '#';   // mark visited for THIS path only
    dfs(board, r + 1, c, next, result);
    dfs(board, r - 1, c, next, result);
    dfs(board, r, c + 1, next, result);
    dfs(board, r, c - 1, next, result);
    board[r][c] = ch;   // BACKTRACK — restore, so a different search path can reuse this cell
}
```

**Why backtracking (restoring `board[r][c]`) is essential here, unlike Number of Islands.** In Number of Islands, a sunk land cell is correctly gone forever — it belongs to exactly one island, permanently. Here, the *same* cell might be the second letter of one candidate word starting from one neighbor, and simultaneously the third letter of an entirely different candidate word starting from a different neighbor. Marking it visited only for the *duration of the current path*, then restoring it before returning, is exactly what backtracking means: try a choice, explore everything it leads to, then undo it before the next alternative gets its turn.

**Trace** on a tiny board with two overlapping words sharing a prefix:

```
Board:        o a
              e t

words = ["oa", "oet"]

buildTrie: root→o→a (word="oa")
                  →e→t (word="oet")
           (both words share the initial 'o' node — explored only once on the board)

dfs(0,0) [cell 'o']: matches root's 'o' child. mark board[0][0]='#'.
  dfs(1,0) [cell 'e']: o-node has child 'e' → matches. mark board[1][0]='#'.
    dfs(1,1) [cell 't']: oe-node has child 't' → matches. oet-node.word="oet" → ADD "oet".
      mark board[1][1]='#'.  no further matching neighbors. restore board[1][1]='t'.
    restore board[1][0]='e'.
  dfs(0,1) [cell 'a']: o-node has child 'a' → matches. oa-node.word="oa" → ADD "oa".
    mark board[0][1]='#'.  no further matching neighbors (oa-node is a leaf). restore board[0][1]='a'.
  restore board[0][0]='o'.

dfs(1,0), dfs(1,1) as FRESH starting cells: root has no 'e' or 't' child → fail immediately.

Final result: ["oet", "oa"]   ✓   Both words found, with the shared 'o' explored exactly
                                   once rather than twice — the entire point of merging
                                   the Trie walk with the board walk.
```

**Complexity:** Bounded by O(rows × cols × 4^L), where L is the longest word's length — but the Trie's pruning means most branches die almost immediately rather than actually reaching that worst case. Space O(total characters across all words) for the Trie, plus O(L) for the recursion stack.

**Common mistakes:**
- **Forgetting `next.word = null` after recording a match.** Without it, a word reachable via more than one path on the board gets added to the results multiple times.
- **Skipping the backtracking restore.** Unlike grid flood-fill problems, cells here legitimately participate in more than one candidate word — failing to restore them breaks every search that should have been able to reuse them.
- **Building a separate Trie or running an independent DFS per word**, instead of one combined Trie and one combined board pass — this throws away the entire reason a Trie was introduced in the first place.

---

## Common Mistakes — Chapter-Wide

- **Confusing "a path exists" with "a complete word was inserted."** `startsWith` returning true only means the prefix path exists; only `isEndOfWord`, checked specifically at the end of traversal, confirms an actual inserted word.
- **Trying to handle wildcard search with a plain iterative loop.** A `.` genuinely branches into up to 26 possibilities — that requires recursion/backtracking, not a single linear walk.
- **Forgetting to mark-and-restore visited cells correctly in Word Search II** — the same cell can legitimately belong to multiple different candidate words, unlike simple flood-fill problems.
- **Re-running independent per-word searches instead of building one shared Trie** — defeats the entire asymptotic benefit a Trie provides whenever multiple words are involved.

## Pattern Recognition Guide

- "Many words, need fast prefix queries" (search, startsWith, autocomplete) → Trie.
- "Search with a wildcard matching any character" → Trie + recursive branching at each wildcard position.
- "Search a grid/board for any of several target words at once" → build one Trie from every target word, then a single combined DFS/backtracking pass walking the Trie and the grid together — never search for each word independently once a Trie is on the table.
- The general signal: a "given list of words" large enough that comparing against each one individually feels wasteful, where the actual operation is fundamentally about *prefixes* — that's a Trie.

## Chapter Summary

- A Trie turns "does any word match or start with this prefix" from an O(n·m) search-through-everything into an O(m) walk down a fixed number of nodes — independent of how many words n are stored, because words sharing a prefix share the same nodes for it.
- Insert, search, and startsWith are the *identical* traversal; they differ only in what gets checked at the very end — search requires `isEndOfWord`, startsWith only requires the path to exist.
- Wildcard search breaks the simple linear-walk traversal entirely — a `.` must branch into every possible child, which needs recursion, not a loop.
- Word Search II is the payoff for combining two ideas from two different chapters: a Trie's prefix-sharing efficiency, and backtracking's "mark, explore, restore" discipline — the same discipline behind Number of Islands' visited-marking, except here it must be *undone* afterward, because the same board cell can legitimately be part of more than one candidate word.
