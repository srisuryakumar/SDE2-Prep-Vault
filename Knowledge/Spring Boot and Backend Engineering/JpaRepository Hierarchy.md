---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 4 — Entities and JPA"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [spring, jpa, repository]
---

# JpaRepository Hierarchy

## Intuition
Spring Data JPA provides a hierarchy of interfaces that give you a full CRUD implementation without writing any concrete classes or SQL.

## The Hierarchy
```
Repository<T, ID>               (marker interface only)
 └─ CrudRepository<T, ID>       (save, findById, findAll, delete, count, existsById)
     └─ PagingAndSortingRepository<T, ID>  (findAll(Sort), findAll(Pageable))
         └─ JpaRepository<T, ID>           (flush, saveAndFlush, deleteAllInBatch, getById)
```

By extending `JpaRepository<T, ID>` and annotating with `@Repository`, Spring Data generates a concrete proxy implementation at startup wired to your `DataSource`.
