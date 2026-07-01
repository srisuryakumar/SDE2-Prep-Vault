import os

companies_data = {
    "Razorpay": {
        "rounds": "1 DSA, 1 LLD/HLD, 1 Hiring Manager",
        "dsa_patterns": ["[[0146 LRU Cache]]", "subarray-HashMap", "linked list"],
        "dsa_hints": ["Design", "Prefix Sum + HashMap", "Linked List"],
        "sys_design": "Payment Gateway with idempotency",
        "domain": "Payment Gateway, Webhooks, Exactly-once processing",
        "values": "Transparency, Ownership, Customer First",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[Generic Cache System Design LLD]]",
        "salary_min": "40",
        "salary_ask": "45"
    },
    "PhonePe": {
        "rounds": "1 Machine Coding, 1 DSA, 1 System Design, 1 HM",
        "dsa_patterns": ["graphs", "DP", "concurrency"],
        "dsa_hints": ["Graph", "DP", "Concurrency"],
        "sys_design": "UPI payment system at 500M transactions/day",
        "domain": "High throughput systems, Redis, HBase",
        "values": "Do the right thing, Take ownership, Build for scale",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[Generic Cache System Design LLD]]",
        "salary_min": "45",
        "salary_ask": "52"
    },
    "Meesho": {
        "rounds": "1 DSA, 1 HLD, 1 HM",
        "dsa_patterns": ["arrays", "strings", "trees"],
        "dsa_hints": ["Array", "String", "Tree DFS"],
        "sys_design": "Product recommendation or flash sale",
        "domain": "E-commerce scale, Flash sales",
        "values": "Speed over perfection, User First",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[Generic Cache System Design LLD]]",
        "salary_min": "38",
        "salary_ask": "42"
    },
    "Atlassian": {
        "rounds": "1 DSA, 1 LLD (Machine Coding), 1 HLD, 1 Values",
        "dsa_patterns": ["trees", "DFS/BFS", "topological sort"],
        "dsa_hints": ["Tree DFS", "Graph BFS", "Topological Sort"],
        "sys_design": "Jira workflow engine",
        "domain": "SaaS scale, Collaboration tools",
        "values": "Open company, Play as a team",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[Generic Cache System Design LLD]]",
        "salary_min": "45",
        "salary_ask": "50"
    },
    "Amazon": {
        "rounds": "2 DSA, 1 LLD, 1 System Design, 1 Bar Raiser",
        "dsa_patterns": ["trees", "arrays", "HashMaps"],
        "dsa_hints": ["Tree DFS", "Array", "HashMap"],
        "sys_design": "Shopping Cart, Locker system",
        "domain": "AWS architecture, DynamoDB",
        "values": "16 Leadership Principles",
        "story": "[[Amazon Leadership Principles Deep Dive]]",
        "lld": "[[Generic Cache System Design LLD]]",
        "salary_min": "45",
        "salary_ask": "52"
    },
    "Uber": {
        "rounds": "1 DSA (Hard), 1 Machine Coding, 1 HLD, 1 HM",
        "dsa_patterns": ["Hard graphs", "Dijkstra", "Trie"],
        "dsa_hints": ["Graph", "Shortest Path", "Trie"],
        "sys_design": "Location tracking, Surge pricing",
        "domain": "Geospatial queries, Quadtrees",
        "values": "Go get it, See the forest and the trees",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[Generic Cache System Design LLD]]",
        "salary_min": "50",
        "salary_ask": "58"
    },
    "Rippling": {
        "rounds": "1 DSA, 1 API/LLD, 1 System Design, 1 HM",
        "dsa_patterns": ["API design", "data modeling"],
        "dsa_hints": ["Design", "HashMap"],
        "sys_design": "RBAC, workflow engine",
        "domain": "HRIS, complex data models",
        "values": "Push the limits, Hard work",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[Logger System LLD]]",
        "salary_min": "55",
        "salary_ask": "65"
    },
    "Swiggy": {
        "rounds": "1 DSA, 1 Machine Coding, 1 System Design, 1 HM",
        "dsa_patterns": ["Maps", "arrays", "standard mediums"],
        "dsa_hints": ["HashMap", "Array", "Two Pointers"],
        "sys_design": "Food delivery tracking",
        "domain": "Hyperlocal delivery, Geolocation",
        "values": "Customer first, Stand up and disagree",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[Generic Cache System Design LLD]]",
        "salary_min": "38",
        "salary_ask": "45"
    },
    "Groww": {
        "rounds": "1 DSA, 1 LLD, 1 HLD, 1 HM",
        "dsa_patterns": ["Array processing", "sorting"],
        "dsa_hints": ["Array", "Sorting", "Math"],
        "sys_design": "Stock trading engine, Portfolio tracker",
        "domain": "Fintech, Trading engines",
        "values": "Customer obsession, Simplicity",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[In-Process Pub-Sub Event Bus LLD]]",
        "salary_min": "35",
        "salary_ask": "40"
    },
    "CRED": {
        "rounds": "1 Machine Coding, 1 LLD/DSA, 1 System Design, 1 HM",
        "dsa_patterns": ["Strings", "DP", "trees"],
        "dsa_hints": ["String", "DP", "Tree DFS"],
        "sys_design": "Rewards allocation, Leaderboard",
        "domain": "High trust systems, Gamification",
        "values": "High trust, high performance",
        "story": "[[Project Deep Dive Rehearsal]]",
        "lld": "[[Generic Cache System Design LLD]]",
        "salary_min": "40",
        "salary_ask": "48"
    }
}

# Find valid LeetCode problems
lc_files = []
for root, _, files in os.walk('Practice/LeetCode'):
    for f in files:
        if f.endswith('.md'):
            lc_files.append(f[:-3])

def get_dsa_problems(company, hints):
    problems = []
    # If Razorpay, use specific problems first
    if company == "Razorpay":
        problems.append("[[0146 LRU Cache]]")
        # try to find subarray-HashMap
        for lc in lc_files:
            if "Subarray" in lc or "Sum" in lc:
                if f"[[{lc}]]" not in problems:
                    problems.append(f"[[{lc}]]")
                    break
        for lc in lc_files:
            if "Linked List" in lc or "List" in lc:
                if f"[[{lc}]]" not in problems:
                    problems.append(f"[[{lc}]]")
                    break
    
    # Fill remaining to 5
    idx = 0
    while len(problems) < 5 and idx < len(lc_files):
        prob = f"[[{lc_files[idx]}]]"
        if prob not in problems:
            problems.append(prob)
        idx += 1
    return problems

template = """---
type: company-protocol
company: {company}
tags: [protocol, {company_lower}]
---

# {company} — 72-Hour Interview Activation Protocol

**Round types expected:** {rounds}

---

## Hour 0-4: Intelligence Refresh

- [ ] Re-read [[{company}]] dossier — focus specifically on: {domain}
- [ ] Search LeetCode Discuss: "{company} SDE2 2026" — note any new reported patterns
- [ ] Search r/developersIndia: "{company} interview experience" — posts from last 3 months only
- [ ] Check Blind: "{company} interview" — filter by most recent
- [ ] Log any new findings in the [[Application Tracker]] note

---

## Hours 4-24: DSA Sprint

Solve these problems, drawn from this company's known patterns:

1. {dsa_1} — {hint_1} — target 20 min
2. {dsa_2} — {hint_2} — target 20 min
3. {dsa_3} — {hint_3} — target 25 min
4. {dsa_4} — {hint_4} — target 25 min
5. {dsa_5} — {hint_5} — target 30 min

Time cap per Medium: 25 minutes before reading hints.

---

## Hours 24-48: Domain and Behavioral Sprint

**Domain knowledge to review:**
- {domain}

**Engineering blog reading:**
- Search for "{company} engineering blog" — read the most recent technical post

**Behavioral preparation:**
- Company values: {values}
- STAR stories to rehearse: {story}
- "Why {company}?" — write a 3-sentence answer referencing: one specific engineering challenge they face, one technology choice they've made, one career alignment reason

---

## Hours 48-72: Simulation Sprint

- [ ] 1 timed DSA mock — 45 min, 2 Mediums from this company's LeetCode tag
- [ ] Re-solve {lld} in 45 min without looking at your implementation
- [ ] Verbally walk through [[{sys_design}]] using the 5-step framework — time at 45 min exactly
- [ ] Salary anchor confirmed: Levels.fyi "{company} SDE-2 India 2026" — write minimum and opening ask below

Minimum I will accept: ₹{salary_min}L
Opening ask: ₹{salary_ask}L

---

## Hour 72: Final 30-Minute Checklist

- [ ] Interview link / address / room confirmed
- [ ] Water and notepad ready for system design
- [ ] IntelliJ open with a blank Java file — test it compiles `Hello World`
- [ ] VS Code with Java Extension Pack as backup — test it
- [ ] Read through the SDE-2 Differentiator table in [[02_Interview_Intelligence_and_Behavioral]] or its vault equivalent
- [ ] Review top 3 STAR stories one final time — say "I" not "we"
"""

for company, data in companies_data.items():
    probs = get_dsa_problems(company, data["dsa_hints"])
    hints = data["dsa_hints"]
    while len(hints) < 5:
        hints.append(hints[-1]) # pad
        
    content = template.format(
        company=company,
        company_lower=company.lower(),
        rounds=data["rounds"],
        domain=data["domain"],
        dsa_1=probs[0], hint_1=hints[0],
        dsa_2=probs[1], hint_2=hints[1],
        dsa_3=probs[2], hint_3=hints[2],
        dsa_4=probs[3], hint_4=hints[3],
        dsa_5=probs[4], hint_5=hints[4],
        values=data["values"],
        story=data["story"],
        lld=data["lld"],
        sys_design=data["sys_design"],
        salary_min=data["salary_min"],
        salary_ask=data["salary_ask"]
    )
    
    path = f"Career/Companies/72-Hour Protocols/{company}.md"
    with open(path, 'w') as f:
        f.write(content)

print("Generated 10 protocols.")
