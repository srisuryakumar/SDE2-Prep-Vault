---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 6 — Developer Environment, Git, and Tooling"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, tooling, maven]
---

# Maven Build System and pom.xml

Maven is a build tool and dependency manager. It enforces a strict project structure (code in `src/main/java`, tests in `src/test/java`).

## The `pom.xml`
The Project Object Model (POM) defines the build.
- **Coordinates:** `groupId` (reverse domain), `artifactId` (project name), and `version`.
- **Dependencies:** Libraries downloaded from Maven Central into your local cache (`~/.m2/repository`).
- **Scopes:** 
  - `compile` (default)
  - `runtime` (JDBC drivers)
  - `test` (JUnit, Mockito; not in final JAR)
  - `provided` (Servlet API)

## The Build Lifecycle
Maven executes phases in a specific order. Running a phase runs all preceding phases.
- `clean`: Delete `target/`
- `compile`: Compile code to `target/classes/`
- `test`: Run unit tests
- `package`: Package compiled code into a JAR/WAR
- `verify`: Run integration tests and coverage checks
- `install`: Install JAR to local `~/.m2` repo
- `deploy`: Upload JAR to a remote repository

Common commands: `mvn clean package -DskipTests`, `mvn spring-boot:run`.
