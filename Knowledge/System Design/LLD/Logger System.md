---
type: concept
title: Logger System LLD
tags: [lld, design, concurrency]
---
# Logger System LLD

## Requirements
- Support multiple log levels (INFO, DEBUG, ERROR).
- Support multiple appenders (Console, File, Database).
- Thread-safe and asynchronous logging to prevent blocking the main thread.

## Core Components
1. **Logger**: The main interface used by the application.
2. **LogManager**: Singleton managing logger instances.
3. **LogMessage**: Data class holding the message, level, and timestamp.
4. **Appender**: Interface for different output destinations.
5. **LogFormatter**: Strategy for formatting the message.

## Design Patterns Used
- **Singleton**: For the `LogManager`.
- **Observer/Pub-Sub**: The Logger publishes `LogMessage`s to subscribed `Appender`s.
- **Factory**: For creating Appenders or Loggers.
- **Chain of Responsibility**: For filtering log levels (e.g., only ERROR goes to DB, DEBUG goes to File).

## Asynchronous Handling
To ensure high performance, the Logger places `LogMessage`s into a `BlockingQueue`. A separate background worker thread polls this queue and writes to the Appenders, effectively decoupling the caller from the slow I/O operations of logging.
