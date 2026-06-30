# Resume That Gets Past ATS

### ATS reality: most resumes are never seen by human eyes

Every Tier 1 company runs applications through an Applicant Tracking System before a recruiter sees them. The ATS parses your resume into fields (name, company, title, dates, skills, education) and either ranks or filters candidates based on keyword match against the job description. A resume that confuses the parser — even one that looks great to a human — can get silently dropped or mis-ranked. You are not writing a resume for a person first. You are writing for a parser first, a recruiter second (60–90 seconds of attention), and a hiring manager third.

### ATS optimization rules

- **No tables.** Tables break parsing order — the ATS may read across columns instead of down them, scrambling your work history.
- **No columns.** Two-column "modern" templates are the single most common reason strong resumes get mis-parsed. Use a single-column, linear layout.
- **No graphics, icons, or skill bars.** They add nothing the parser can read and often get rendered as garbage characters.
- **No headers/footers for critical info.** Some parsers skip header/footer text entirely — never put your contact info or a skills summary there.
- **Standard section headings.** Use "Experience," "Education," "Skills," "Projects" — not "My Journey" or "What I Bring." The parser is matching against a dictionary of expected headings.
- **.docx or simple .pdf, never an image-based or design-tool export.** Canva and Figma exports often render as one giant image block — completely unparseable.
- **Standard fonts.** Calibri, Arial, or Georgia at 10.5–11pt. No script fonts, no fonts the parser's font dictionary doesn't recognize.

### The impact formula for every bullet

```
[Strong verb] + [what you built/fixed/owned] + [technology/method used] + [quantified result]
```

Every bullet on your resume should be testable against this formula. If you can't fill in all four parts honestly, the bullet is too vague to survive a recruiter's 60-second scan.

### Before/after: weak bullets transformed

**Weak:** "Worked on backend APIs for the payments team."
**Strong:** "Built 6 REST APIs in Java/Spring Boot for the payments reconciliation service, reducing manual reconciliation time from 4 hours to 20 minutes daily."

**Weak:** "Responsible for fixing bugs in the codebase."
**Strong:** "Diagnosed and fixed a race condition in the order-processing service causing 2% of orders to double-charge customers, eliminating the issue in production within one sprint."

**Weak:** "Helped improve system performance."
**Strong:** "Reduced p99 API latency from 800ms to 220ms by introducing Redis caching for the product-catalog read path, cutting database load by 40%."

**Weak:** "Worked with cross-functional teams on a new feature."
**Strong:** "Led backend design for a new refunds workflow across 3 teams (Payments, Support, Finance), shipping on schedule and processing ₹2Cr+ in refunds in the first month."

**Weak:** "Wrote unit tests for the application."
**Strong:** "Increased test coverage from 35% to 78% for the checkout module using JUnit and Mockito, cutting regression bugs reported post-release by roughly half."

**Weak:** "Migrated services to microservices architecture."
**Strong:** "Decomposed a monolithic billing service into 4 microservices using Spring Boot and Kafka, reducing deployment time from 45 minutes to 6 minutes and enabling independent team releases."

**Weak:** "Mentored junior developers."
**Strong:** "Mentored 2 SDE-1s through onboarding and their first production releases, both promoted within 12 months; built the team's onboarding checklist still in use today."

**Weak:** "Improved CI/CD pipeline."
**Strong:** "Rebuilt the CI/CD pipeline with GitHub Actions and Docker layer caching, cutting average build time from 14 minutes to 4 minutes across 30+ engineers' daily workflow."

**Weak:** "Handled production incidents."
**Strong:** "Served as primary on-call for a service handling 5M+ daily requests; led incident response for a P1 outage, restoring service in 18 minutes and writing the postmortem that became the team's incident-response template."

**Weak:** "Worked on database optimization."
**Strong:** "Optimized 3 high-traffic PostgreSQL queries by rewriting joins and adding composite indexes, reducing average query time from 1.2s to 90ms on a table with 40M+ rows."

### Complete resume structure

1. **Header:** Name, phone, email, LinkedIn URL (customized), city. No photo, no "objective" line.
2. **Summary (optional, 2 lines max):** Only include if it adds signal — e.g., "Backend engineer, 3 years, specializing in distributed payment systems (Java, Spring Boot, Kafka)." Skip generic summaries entirely.
3. **Skills:** Grouped by category (Languages / Frameworks / Infrastructure / Databases). Specific technologies only.
4. **Experience:** Reverse chronological. Company, title, dates, location. 3–5 bullets per role using the impact formula, most recent/relevant role gets the most space.
5. **Projects:** 2–3 projects max, only if they add signal beyond your work experience (open source, side projects with real usage, or work projects you can speak about in more depth than the bullet allows).
6. **Education:** Degree, institution, graduation year. GPA only if above 8.5/10 or equivalent and you're within 3 years of graduating.

### The one-page rule

At 3 years of experience, you have one page — no exceptions. A two-page resume at this level signals either an inability to prioritize or an attempt to pad thin experience with noise. Recruiters spend under a minute on first pass; a second page is, on average, never read. Cut ruthlessly.

### ATS keyword extraction

1. Paste the job description into a text editor and highlight every noun that's a technology, methodology, or domain term (e.g., "distributed systems," "payment gateway," "idempotency," "Kafka," "on-call").
2. Cross-reference against your actual experience — only use keywords you can honestly speak to in an interview.
3. Weave matched keywords naturally into your bullets and skills section.
4. Tailor per application for your top 5–10 target companies. Generic resumes sent everywhere consistently underperform 3–4 tailored versions sent to fewer, better-targeted roles.
