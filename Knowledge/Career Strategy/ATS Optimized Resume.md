---
type: concept
subject: Career Strategy
source_book: "Book 9 — Interview Mastery and Career Strategy"
source_chapter: "Chapter 2 — Resume That Gets Past ATS"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [career, resume, ats]
---

# ATS Optimized Resume

## ATS Reality
Most resumes are filtered by an Applicant Tracking System (ATS) before human eyes see them. You write for the parser first, the recruiter second (60-90 seconds), and the hiring manager third.

## ATS Optimization Rules
- **No tables or columns:** They break parsing order. Use a single-column linear layout.
- **No graphics, icons, or skill bars:** Render as garbage characters.
- **Standard section headings:** Use "Experience," "Education," "Skills," "Projects."
- **Format:** `.docx` or simple `.pdf`. No Canva/Figma image-based exports.
- **Length:** One page only for 3 YOE.

## The Impact Formula for Every Bullet
`[Strong verb] + [what you built/fixed/owned] + [technology/method used] + [quantified result]`
*Example:* "Reduced p99 API latency from 800ms to 220ms by introducing Redis caching for the product-catalog read path, cutting database load by 40%."

## Quantification
Never invent numbers, but estimate honestly.
- Measure a latency drop once? Say "~30% reduction".
- Know your team's request volume? Say "service processing 5M+ requests daily".

## Skills Section
- **Include:** Specific languages, frameworks, DBs, Infra (Java, Spring Boot, Kafka, Kubernetes).
- **Exclude:** Soft skills ("Leadership," "Team Player").

## Projects Section (Signaling SDE-2)
An SDE-2 project shows system thinking, scale, and architectural decisions, not just "I built a CRUD app." Talk about rate limiting, custom encoding, deployment via Terraform, etc.

## ATS Keyword Extraction
Tailor your resume for top targets. Highlight domain terms (e.g. "event-driven architecture") from the JD and weave them naturally into your bullets. ATS matching is often literal.
