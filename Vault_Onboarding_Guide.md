---
type: guide
tags: [guide, onboarding, start-here]
---

# Start Here — Your Obsidian Vault Onboarding Guide

A note before anything else: I designed the structure this vault was built from, but I haven't seen the actual files Gemini generated inside Antigravity. Everything below should match closely if the migration ran cleanly, but if a specific note or folder name doesn't match exactly what you see, don't get stuck on it — press `Ctrl/Cmd+O` (the Quick Switcher), start typing what you're looking for, and Obsidian will find it. The workflow and mental model below hold regardless of small naming differences.

Read this once, top to bottom, before Day 1. After that, treat it as a reference — keep it open in a side pane for your first week, then you won't need it anymore.

---

## Part 1 — Obsidian in Ten Minutes

You've never used this tool, so here's everything you actually need to know, in plain terms.

**Vault** is the whole folder. When you open Obsidian and point it at your repository, that folder becomes your vault — every subfolder and every `.md` file inside it is part of it.

**Note** is a single `.md` file. Every problem, every concept, every day of the plan is one note.

**Wikilink** is the `[[Double Bracket]]` syntax connecting two notes. When you see `[[HashMap Internals]]` written inside a note, it's clickable — click it and you jump straight there. Hover over it without clicking and Obsidian shows a preview popup, so you can peek without leaving where you are.

**Backlinks** work in reverse. Open `HashMap Internals.md` and look at the bottom of the note (or the right sidebar) — you'll see every note that links *to* this one, automatically. This is the entire trick behind this system: a single concept note shows you every day it was studied and every LeetCode problem that used it, with zero manual upkeep on your part.

**Properties** are the structured fields at the top of every note — status, difficulty, dates. Obsidian renders these as a clean little table, not raw text, and you edit them by clicking directly into a field. This is what powers every dashboard — a plugin reads these properties across hundreds of notes and assembles them into live tables.

**The Quick Switcher** (`Ctrl/Cmd+O`) is your most-used shortcut. Press it, type a note's name, hit Enter. Faster than browsing folders for almost everything you'll do.

**Search** (`Ctrl/Cmd+Shift+F`) is full-text search across every note, not just titles — use it when you remember a phrase but not which note it lives in.

**The Outline panel**, usually in the right sidebar, auto-generates a clickable table of contents for whatever note you have open, built from its headers. This guide has headers specifically so the Outline panel makes it navigable.

**Reading view vs. Edit view** — a toggle, usually top-right, switches between a clean rendered view and raw editable markdown. You'll live mostly in edit view since you're actively annotating notes.

**The three plugins**, one line each: Dataview turns your notes' properties into live tables — every dashboard and index depends on it. Templater spawns a new note pre-filled with the right structure and today's date instead of you typing frontmatter from scratch. Tasks gives you a vault-wide view of every unchecked `- [ ]` box across all 120 daily notes at once.

That's genuinely the whole primer. Everything else you pick up by using it.

---

## Part 2 — Day 0: Before You Study Anything

1. Install Obsidian from obsidian.md if it isn't already on your machine.
2. Open Obsidian → **Open folder as vault** → select your repository folder.
3. Obsidian will likely ask whether to trust this vault and enable the plugins found inside it. Say yes — the plugin configuration was committed specifically so this works on a fresh machine.
4. Go to **Settings** (gear icon, bottom left) → **Community Plugins**. If you see a button that says "Turn on community plugins," click it. Confirm Dataview, Templater, and Tasks all show as installed and enabled. If any are missing, use **Browse** to find and install them.
5. Open `Dashboard/Home.md` through the Quick Switcher. This is your single most important check: if the Dataview sections render as actual tables, your setup is working. If you see raw text that looks like code instead of a table, Dataview isn't enabled yet — go back to step 4.
6. Open `Daily Journal/Day 000.md`. This note documents your environment setup — Java, Maven, IntelliJ, your six GitHub repositories, your LeetCode and GitHub accounts. Work through its checklist literally, checking off each box as you confirm it.
7. Once Day 000 is fully checked off, Day 0 is done.

---

## Part 3 — Day 1: Your First Real Day

Open `Daily Journal/Day 001.md` through the Quick Switcher.

At the top, the properties panel shows `day_number: 1`, `week_number: 1`, `status: planned`, plus `dsa_problems` and `theory_topics` as lists of links. Below that, the note is organized into the same four blocks the original plan used — DSA Block, Theory Block, Project Block, Career Block — followed by a Daily Deliverable checklist.

Walk through one full link to see the pattern: in the DSA Block you'll see something like "Problem 1: `[[0001 Two Sum]]`." Click it. You land on the Two Sum note — its own properties (difficulty, pattern, companies, status), a problem statement, a hint, and a Revisit Log table that's currently empty. This note is where you *track* the problem; the actual code goes in your `dsa-java` repository in IntelliJ, not here. A short pasted snippet or your final approach in a code block is fine for memory's sake, but this note isn't your IDE.

After you solve it in IntelliJ and commit it, come back to this note: change `status` from `not-started` to `solved`, set `first_solved_date`, and add a row to the Revisit Log.

Same pattern for Theory Block links — click into the Knowledge note, actually study there (Part 6 covers how), and flip `status` to `studied` once you genuinely understand it, not just once you've read it.

At the end of the day, return to `Day 001.md`, check off the Daily Deliverable boxes, and flip the note's own `status` to `complete`. Then update the "Today" line on `Dashboard/Home.md` to point at `[[Day 002]]` before you close up — the one manual housekeeping step that keeps the dashboard honest.

That's the entire loop. Every day from here repeats this exact pattern.

---

## Part 4 — The Vault Map: What's Where, and When You'll Open It

The most important thing to internalize about this vault: **the Daily Note is the hub. Almost everything else is a spoke you reach by clicking a link from today's note, not by browsing to it directly.** If you ever find yourself manually digging through `Knowledge/Java/` folder by folder trying to find something, stop — go back to the relevant Daily Note, or use the Quick Switcher.

**Dashboard/** — open every morning, first thing. Mostly read-only; the one exception is the "Today" line you update once a day.

**Daily Journal/** — your actual home base, where you'll spend most of your direct typing and checking-off time, all day, every day.

**Knowledge/** — you'll almost never browse this folder directly. You arrive here by clicking theory links from a Daily Note. The one deliberate exception is your evening reading slot, covered in Part 12.

**Practice/LeetCode/** — same pattern, reached via DSA Block links or the Revision Due dashboard, not browsed.

**Practice/Mocks/** and **Practice/Projects/** — opened more directly, since they're tied to specific scheduled events rather than daily content.

**Career/** — mostly reached via links early on (today's LinkedIn post, a company dossier). You'll browse this folder more directly starting around Week 9, when applications begin.

**Templates/** — you almost never open these to read them. You consume them indirectly, through the "create new note from template" command, whenever a new Mock, Application, or Interview Debrief needs to exist.

**_Source-Archive/** — the original flat files, frozen for reference. You should essentially never need to open this.

---

## Part 5 — How the Roadmap and the Books Work Together Now

The original problem was simple: the day-by-day plan and the books were two disconnected documents. That's resolved structurally now, not by citation text — every Theory Block topic in every Daily Note is a literal, clickable link directly into the relevant content.

When Day 1's Theory Block names JVM Architecture, you don't go looking for a book and a chapter number. You click `[[JVM Architecture]]` (or whatever the linked note is actually called) straight from the Daily Note, and you land inside the atomized version of what used to be a chapter — broken into one note per concept, not a forty-page dump.

One shift worth internalizing clearly: the 10 books, as standalone documents, no longer exist as something you'd open and read front-to-back. Their content has been fully broken apart into `Knowledge/`. This was deliberate — a monolithic chapter is hard to link to precisely and hard to revisit later; forty separate single-concept notes are each individually linkable, individually trackable through their own `status` field, and individually revisable. So where the original schedule said "read Effective Java, 20 minutes," that slot now means something slightly different — covered concretely in Part 12.

---

## Part 6 — Taking Notes While You Study

The Knowledge note you land on from a Theory Block link is not a frozen reference. It's yours now — edit it directly.

When the migration atomized the books, it captured what the source material said. Your job during actual study isn't to copy that out somewhere else — it's to read what's there, then directly rewrite or extend parts of it in your own words, in that same note. Add your own code example if the original one doesn't click for you. Add a one-line "why I kept forgetting this" note if something didn't stick the first time.

A note that starts the program at `status: to-study` with a thin two-sentence definition might grow into a note at `status: mastered` with a worked example and links to two related concepts you discovered while studying, by Week 10. That's the system working as intended — these notes are meant to thicken over the 120 days, not stay static.

One distinction worth keeping clear: anything true regardless of which day it is — a concept explanation, a working code example, why a pattern holds — belongs in the Knowledge note. Anything specific to today only — how the session felt, what's confusing right now, what tomorrow should focus on — belongs in the Daily Note's reflection section instead (Part 12).

---

## Part 7 — Tracking Daily Progress

Four mechanisms, layered:

The **Daily Deliverable checklist** at the bottom of each Daily Note — check items off as you finish them, exactly as the original plan intended.

Each Daily Note's own **status field** — `planned` → `in-progress` → `complete`.

The **Weekly Review notes** in `Daily Journal/Weekly Reviews/` — fill these in every Sunday, the same ritual as the original Weekly Scorecard, now living as a proper note with a query at the top that auto-pulls that week's seven days for cross-reference instead of you tallying everything by hand.

`Dashboard/Progress Overview.md` rolls all of this up automatically — total days complete out of 120, problems solved by status, concepts still sitting at `to-study` or `stub`. You don't maintain this directly; it just reflects whatever you've already checked off elsewhere.

---

## Part 8 — How to Revise

Every LeetCode note carries three fields for this: `last_reviewed`, `review_count`, `next_review_due`. The interval logic behind them: after the 1st revisit, due again in 3 days; 2nd revisit, 7 days; 3rd, 14 days; 4th, 30 days; 5th onward, 60 days.

`Dashboard/Revision Due.md` surfaces everything due today by querying these fields across the whole problem set — you don't track this list yourself, you just work through whatever it shows you.

This is a manual update, not automatic magic: when you revisit a problem, you click into its properties and update those three fields yourself. Budget about a minute per problem for this bookkeeping. Part 12 shows exactly where in your day this fits.

---

## Part 9 — LeetCode Practice Workflow

The split to hold in your head: **IntelliJ and the `dsa-java` repository are where you write and run code. The Obsidian note is where you think and track** — the pattern, the hint, the complexity, your history with this exact problem.

**First attempt:** open the note linked from today's Daily Note, read the problem statement and hint there if needed, switch to IntelliJ, solve it, commit to `dsa-java`. Back in Obsidian: update `status`, set `first_solved_date` and `avg_time_min`, add the first row to the Revisit Log.

**Revisit** (when a problem resurfaces later in the plan, or surfaces via Revision Due): open the *same* note — this is the entire point of having deduplicated every problem to one canonical note. Check your own past notes and complexity analysis before re-solving from scratch. Re-solve, add a new Revisit Log row, update the three review fields from Part 8.

If you want to drill an entire pattern at once — useful before a company-specific sprint — open the relevant note in `Practice/LeetCode/_Patterns/`. You'll see every problem using that pattern in one table, sorted by difficulty and status.

---

## Part 10 — Projects and Career Workflow

**Projects:** open the relevant note in `Practice/Projects/` when starting work on a repository. The code lives in the repo itself, opened separately in IntelliJ; the hub note tracks status and links out to it. For `order-management-api` and `scalable-ecommerce-platform` specifically, the moment you make a real architectural decision — why Kafka over a direct HTTP call, why this database — write it as a new ADR note in that project's `ADRs/` subfolder using the ADR Template. Do this while the reasoning is still fresh, not retroactively.

**LinkedIn posts:** all 34 are pre-written, sitting in `Career/LinkedIn Content/Posts/`. On a posting day, open the relevant note, copy the body, publish it, then flip that note's status from `drafted` to `published`.

**Company dossiers and 72-hour protocols:** mostly dormant until you're actually applying, around Week 9 onward. The moment a real interview gets scheduled, open that company's 72-Hour Protocol note and work through it hour-block by hour-block.

**Applications and Interview Debriefs:** create a new note from the relevant template the moment each real event happens — you apply, you get an interview, you finish a round. Don't batch these. Write the debrief the same day, while details are still sharp.

---

## Part 11 — Quick Reference

| Section | What it's for | When you open it | Do you edit it? |
|---|---|---|---|
| Dashboard/ | Command center, live status | Every morning | Mostly read; one "Today" line updated daily |
| Daily Journal/ | Your daily driver | All day, every day | Constantly |
| Knowledge/ | Atomized book content | Via links during Theory Block | Yes — actively, as you study |
| Practice/LeetCode/ | Problem tracking and history | Via links during DSA Block, or Revision Due | Yes — status and revisit log |
| Practice/Mocks/ | Mock interview logs | When a mock is scheduled, then right after | Created and filled per session |
| Practice/Projects/ | Repository hubs and ADRs | When starting project work | Status, plus ADRs as decisions happen |
| Career/ | Companies, applications, content, behavioral | Mostly Week 9 onward | As real events happen |
| Templates/ | Blueprints for new notes | Rarely opened to read | Consumed via "new note from template" |
| _Source-Archive/ | Original flat files, frozen | Almost never | Never — historical record only |

---

## Part 12 — Your Full Daily Workflow, Start to Finish

This maps your existing 06:00–22:00 schedule onto exactly when the vault comes into play, and — just as importantly — when it doesn't.

| Time | Block | What you actually do in the vault |
|---|---|---|
| 06:00 | Wake up, walk | Nothing. Screen-free, by design. |
| 06:20 | Review yesterday + today's plan | Open `Dashboard/Home.md`, skim "This Week," open today's Daily Note, read all four blocks once before starting any of them. |
| 06:35 | DSA Block | Click each linked LeetCode note, solve in IntelliJ/`dsa-java`, update status and Revisit Log back in the note as each problem finishes. |
| 09:15 | Theory Block | Click each linked Knowledge note, study and actively extend it (Part 6), flip status to `studied` once genuinely understood. |
| 12:45 | Project Block | Open today's linked Project hub note, work in the actual repo, write an ADR note if a real decision was made. |
| 15:15 | Career Block | Open today's linked LinkedIn post, networking template, or company dossier as relevant; publish posts, log outreach. |
| 16:05 | Revision | Open `Dashboard/Revision Due.md`, work through what's surfaced, update the three review fields on each problem touched. |
| 17:30 | Mock or weak-area work | On scheduled mock days: open `Practice/Mocks/`, run the session, fill the Mock Debrief Template after. Otherwise: revisit anything flagged `needs-review`. |
| 18:30 | Primary study ends | — |
| 19:00 | "Book reading" | This slot now means something different than it used to: open a Knowledge subject MOC you haven't browsed in a while, or follow the graph view out from today's notes, picking up anything still marked `stub` or `to-study`. |
| 19:20 | Study Journal | Back in today's Daily Note — add a short Reflection section if one doesn't already exist (what you learned, what's still unclear, tomorrow's focus), check off the Daily Deliverable list, flip the note's status to `complete`. |
| 20:00+ | Wind down, sleep | Update the "Today" line on `Dashboard/Home.md` to point at tomorrow's note before closing the laptop — the only Dashboard edit of the day. |

---

## Part 13 — Habits That Keep This System Alive

If Obsidian Git is running, you don't need to think about commits daily — but glance at the git history weekly so it isn't entirely invisible to you.

Don't let `status: stub` notes silently accumulate. `Dashboard/Progress Overview.md` surfaces these on purpose; a growing stub count is a signal to slow down and actually study those specific gaps, not a thing to scroll past.

The Sunday Weekly Review is the one ritual that catches drift early. An honest week rating below 7 is the system telling you something needs to change — exactly as the original plan intended, just now with the data already assembled for you instead of hand-tallied.

And one last thing, said plainly: resist the urge to keep restructuring the vault itself once you're actually using it. The system is built. Day 1 onward is about studying inside it — not continuing to engineer it.
