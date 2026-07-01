---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 10 — Dynamic Programming"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, dp, state-machine, stocks]
---

# State Machine DP Pattern

## Intuition
Problems like "Best Time to Buy and Sell Stock" series can be modeled as a state machine. On any given day, you are either:
- **`cash[i]`**: Max profit not holding stock.
- **`hold[i]`**: Max profit holding 1 stock (often negative, as you spent money on an unsold share).

## Buy/Sell Stock I (1 Transaction)
You can only buy once. Buying starts fresh from `-prices[i]`.
- `cash = max(cash, hold + prices[i])` (sell)
- `hold = max(hold, -prices[i])` (buy fresh)

## Buy/Sell Stock II (Unlimited Transactions)
You can buy and sell infinitely. Buying can *reinvest* cash from a previous sale.
- `prevCash = cash`
- `cash = max(cash, hold + prices[i])` (sell)
- `hold = max(hold, prevCash - prices[i])` (buy, reinvesting)

## Buy/Sell Stock III (At Most 2 Transactions)
Unroll the machine into 2 `(hold, cash)` pairs.
**CRITICAL:** To avoid transactions overlapping on the same day, update `cash2` $\rightarrow$ `hold2` $\rightarrow$ `cash1` $\rightarrow$ `hold1`. `hold2` needs the `cash1` from *yesterday*.

```java
public int maxProfit(int[] prices) {
    int hold1 = -prices[0], cash1 = 0;
    int hold2 = -prices[0], cash2 = 0;

    for (int i = 1; i < prices.length; i++) {
        cash2 = Math.max(cash2, hold2 + prices[i]); // Sell 2nd
        hold2 = Math.max(hold2, cash1 - prices[i]); // Buy 2nd (reinvest cash1)
        cash1 = Math.max(cash1, hold1 + prices[i]); // Sell 1st
        hold1 = Math.max(hold1, -prices[i]);        // Buy 1st (fresh)
    }
    return cash2;
}
```

## Buy/Sell Stock IV (At Most K Transactions)
Generalize Stock III into arrays of size $k+1$.
Loop over transaction number `t` from $k$ down to $1$ (for the same reason as Stock III's ordering).

```java
public int maxProfit(int k, int[] prices) {
    if (prices.length == 0) return 0;
    int[] hold = new int[k + 1];
    int[] cash = new int[k + 1];
    Arrays.fill(hold, -prices[0]);

    for (int i = 1; i < prices.length; i++) {
        for (int t = k; t >= 1; t--) { 
            cash[t] = Math.max(cash[t], hold[t] + prices[i]);
            hold[t] = Math.max(hold[t], cash[t - 1] - prices[i]);
        }
    }
    return cash[k];
}
```
