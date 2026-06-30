# SDE-2 Interview Preparation Vault

This repository contains the Obsidian Vault used for tracking and structuring my SDE-2 interview preparation. It follows a multi-phase structure and heavily utilizes metadata to track progress via Dataview dashboards.

## Folder Structure Overview

```text
.
├── Career
│   ├── Applications
│   ├── Behavioral
│   ├── Companies
│   ├── Interview Debriefs
│   ├── LinkedIn Content
│   └── Networking
├── Daily Journal
├── Dashboard
├── Knowledge
│   ├── Career Strategy
│   ├── Datastore Systems
│   ├── Design Patterns
│   ├── Java
│   ├── Kubernetes
│   ├── Messaging Systems
│   ├── Networking and Protocols
│   ├── Operating Systems
│   ├── Spring Boot and Backend Engineering
│   └── System Design
├── Practice
│   ├── LeetCode
│   ├── Mocks
│   ├── Projects
│   └── Revision
├── Templates
├── _Source-Archive
└── _Vault Conventions.md
```

## Required Plugins

To fully utilize this vault, the following Obsidian community plugins are required:
1. **Dataview**: Essential. Powers every dashboard and MOC query in this system. It queries YAML frontmatter metadata to build tables of practice problems, applications, and revision queues.
2. **Templater**: Essential. Enables dynamic fields (such as today's date or file title) inside templates, automating the creation of daily notes and standardizing tracking.
3. **Tasks** (Optional but recommended): For tracking open action items directly in markdown files.
4. **Obsidian Git** (Optional): Auto-commits and pushes to maintain a contribution record for this repository.

## How to Resume this Vault on a New Machine

To resume using this vault on a new machine:
1. `git clone` this repository to your local machine.
2. Open the Obsidian application, click "Open folder as vault", and select the cloned repository folder.
3. Once opened, turn off "Safe Mode" if prompted to enable community plugins.
4. Go to Settings > Community Plugins, and ensure **Dataview** and **Templater** are installed and enabled. That's it! The vault is fully functional.
