---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 6 — Testing"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [testing, spring, mockito]
---

# @MockitoBean vs @MockBean

## Intuition
In Spring Boot 3.4, `@MockBean` and `@SpyBean` were deprecated in favor of `@MockitoBean` and `@MockitoSpyBean`.

## What they do
They behave identically: they create a Mockito mock (or spy) and register it as the Spring bean for that type in the test application context, replacing any real bean of that type.
The rename was purely to align with Spring Framework 6.2's direct Mockito integration and decouple the feature from the Spring Boot testing layer.
