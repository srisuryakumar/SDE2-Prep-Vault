---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, applications, mobile]
---

# Mobile Applications

Backend engineers must understand mobile apps, as they are primary consumers of APIs.

## Native Mobile Apps
- **iOS (Swift):** Compiled to ARM64 machine code, runs directly on iOS.
- **Android (Kotlin/Java):** Compiled to bytecode, then AOT-compiled by the Android RunTime (ART) to native ARM code.

## Cross-Platform Mobile Apps
- **React Native:** Uses JavaScript to drive native iOS/Android UI components via a "bridge". Slower than native due to bridge overhead.
- **Flutter:** Uses Dart (compiled to ARM). Paints its own UI using a graphics engine (Skia) rather than using native components.

## API Considerations for Mobile
- **Bandwidth:** Minimize payload size to handle slow cellular networks.
- **Offline Support:** Apps cache data locally (SQLite/Room). Backend must support cache validation headers (`ETag`, `Last-Modified`).
- **Push Notifications:** You cannot use HTTP polling. Backends publish events to Kafka, and a notification service pushes them to Apple (APNs) or Google (FCM).
