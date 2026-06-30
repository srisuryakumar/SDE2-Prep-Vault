# Java Mastery: From Zero to Production-Grade Engineering

**For Surya — A JavaScript/TypeScript Engineer Who Is Done Guessing About Java**

---

> **How to read this book:** Every concept is explained from scratch, then its internals are exposed. Read the code examples. Run them. Break them. The "What Interviewers Ask" sections are not optional — they encode the precise depth SDE-2 interviews expect.

## Table of Contents

1. **How Java Works** — bytecode, the JVM, JDK vs JRE vs JVM, classloading, your first program
2. **JVM Memory Architecture** — Heap, Stack, Metaspace, Garbage Collection, G1GC
3. **Java Syntax from Scratch** — primitives, String internals, operators, control flow, methods, arrays
4. **Object-Oriented Programming** — the four pillars, records, sealed classes, enums, SOLID
5. **The Collections Framework** — ArrayList, LinkedList, HashMap internals, TreeMap, PriorityQueue, ArrayDeque
6. **Generics and Functional Programming** — wildcards, type erasure, lambdas, Streams, Optional
7. **Java Concurrency** — threads, synchronized, volatile, atomics, locks, ExecutorService, CompletableFuture, virtual threads
8. **Testing Java Applications** — JUnit 5, AssertJ, Mockito, TDD, code coverage
9. **Modern Java Features** — records, sealed classes, pattern matching, switch expressions, text blocks, var

---

# CHAPTER 1: How Java Works

## 1.1 What Is a Computer Program at the Lowest Level?

Before we write a single line of Java, we need to understand what a program actually *is* at the metal level — because Java's entire design is a reaction to the problems that exist at that level.

A CPU is a machine that executes **instructions**. These instructions are just numbers stored in memory — patterns of bits that the CPU recognizes as "add these two registers," "jump to this memory address," "read from this location." The CPU doesn't understand C, Python, JavaScript, or Java. It understands one thing: its own **instruction set architecture (ISA)**.

An x86-64 CPU (your laptop) has a completely different ISA from an ARM CPU (your phone). This means a program compiled for x86-64 will not run on ARM. They speak different machine languages.

Here's what native machine code looks like for "add two numbers":
```
48 01 d8       ; x86-64: add rax, rbx
```

This is a 3-byte instruction. The CPU reads these bytes, decodes them, and routes electricity through transistors to execute the addition. This is the bottom of the stack — pure hardware.

**The Problem:** When you write code in C, a compiler translates your source into machine code for one specific CPU/OS combination. That compiled binary is called a **native binary** or **native executable**. It runs fast — there's nothing between your code and the CPU.

But here's the catch: that binary is completely tied to the platform it was compiled for. A Windows x86-64 binary will not run on macOS ARM. A Linux binary won't run on Windows. You'd need to compile your code separately for every combination of CPU architecture and operating system you want to support.

In the 1990s, this was a genuine crisis for enterprise software.

---

## 1.2 The Problem Java Solved: Write Once, Run Anywhere

Sun Microsystems launched Java in 1995 with a radical idea: what if we introduced an **intermediate layer** between your code and the hardware?

Instead of compiling directly to machine code, Java compiles to an intermediate format called **bytecode** — a set of instructions for an *imaginary* CPU called the Java Virtual Machine (JVM). The JVM is then implemented natively for each platform: Windows, macOS, Linux, Solaris. Each JVM knows how to translate bytecode into the real machine code for its platform.

This means:
1. You write Java code once.
2. You compile it to bytecode once.
3. Any machine with a JVM can run it — no recompilation needed.

**"Write Once, Run Anywhere"** — Java's original marketing slogan — was technically accurate, which was unprecedented.

The analogy: think of bytecode as a **universal recipe** written in a neutral language. Every chef (JVM) in every country knows how to read this recipe and cook it using their local ingredients (hardware). You never rewrite the recipe — you just need a chef who knows the neutral language.

---

## 1.3 The Compilation Pipeline: .java → bytecode → native code

Let's trace exactly what happens to your code step by step.

```
Your Brain
    |
    v
HelloWorld.java          ← Source file: human-readable text
    |
    | javac (Java Compiler)
    v
HelloWorld.class         ← Bytecode: platform-neutral binary
    |
    | JVM loads the .class file
    v
JVM Execution Engine
    |
    | Interpreter (first pass — slow but immediate)
    | JIT Compiler (hot paths — compiles bytecode → native machine code)
    v
Native Machine Code      ← x86-64, ARM64, etc. — runs on CPU
    |
    v
CPU Executes             ← Transistors do arithmetic
```

Let's explain each stage:

### Stage 1: Compilation with `javac`
The Java compiler (`javac`) reads your `.java` source file, performs type-checking, and produces a `.class` file. This `.class` file contains **bytecode** — a compact binary instruction set designed for the JVM.

Bytecode is NOT machine code. It's an intermediate representation. If you look inside a `.class` file, you'll see instructions like `IADD` (integer add), `INVOKEVIRTUAL` (call a method), `ALOAD_0` (load a reference from local variable slot 0). These are JVM instructions, not CPU instructions.

### Stage 2: Class Loading
When you run your program, the JVM's **ClassLoader** finds the `.class` file and loads the bytecode into memory. It also verifies that the bytecode is valid and doesn't violate Java's safety rules (the **Bytecode Verifier** — this is what prevents malicious bytecode from doing things like forging pointers).

### Stage 3: Interpretation (first execution)
The JVM first **interprets** bytecode — it reads each instruction and executes it immediately, translating on the fly. This is slow (roughly 100x slower than native code) but instant to start.

### Stage 4: JIT Compilation (hot paths)
The JVM monitors which code paths are executed frequently ("hot paths"). When a method is called enough times (default: 10,000 times in HotSpot JVM), the **Just-In-Time (JIT) compiler** kicks in and compiles that method's bytecode into actual native machine code for your CPU.

After JIT compilation, subsequent calls to that method run at near-native speed — the JVM doesn't interpret it anymore. The JIT compiler also performs sophisticated optimizations: inlining small methods, removing dead code, loop unrolling, escape analysis (deciding if an object can live on the stack instead of the heap).

**This is why Java "warms up":** a Java application is slow for the first few seconds while the JIT compiles hot paths. After warmup, Java applications often match or exceed C++ performance for long-running workloads.

---

## 1.4 JDK vs JRE vs JVM: Exact Definitions

These three acronyms confuse every Java beginner. Here they are, precisely:

```
┌─────────────────────────────────────────────────┐
│                     JDK                         │
│  (Java Development Kit)                         │
│                                                 │
│  ┌───────────────────────────────────────────┐  │
│  │                JRE                        │  │
│  │  (Java Runtime Environment)               │  │
│  │                                           │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │              JVM                   │  │  │
│  │  │  (Java Virtual Machine)            │  │  │
│  │  │                                   │  │  │
│  │  │  - ClassLoader                    │  │  │
│  │  │  - Bytecode Verifier             │  │  │
│  │  │  - Execution Engine (JIT)        │  │  │
│  │  │  - GC                            │  │  │
│  │  │  - Memory Manager                │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  │                                           │  │
│  │  + Java Standard Library (java.lang,      │  │
│  │    java.util, java.io, java.net, etc.)    │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  + javac (compiler)                             │
│  + javadoc (documentation generator)           │
│  + jdb (debugger)                              │
│  + jar (archive tool)                          │
│  + jconsole, jstack, jmap (monitoring tools)   │
│  + jshell (REPL, Java 9+)                      │
└─────────────────────────────────────────────────┘
```

**JVM (Java Virtual Machine):** The runtime engine. Contains the ClassLoader, Bytecode Verifier, JIT compiler, Garbage Collector, and Memory Manager. It is an abstract specification — HotSpot (Oracle/OpenJDK) and GraalVM are two implementations of it. The JVM is platform-specific: there's a different JVM binary for Windows, macOS, and Linux.

**JRE (Java Runtime Environment):** JVM + the Java standard library (all the `java.*` packages you import). Everything needed to **run** a compiled Java program. End users who just want to run a Java application need only the JRE.

**JDK (Java Development Kit):** JRE + development tools (compiler `javac`, debugger `jdb`, documentation generator `javadoc`, archive tool `jar`, profiling tools). Developers need the JDK. Since Java 11, Oracle no longer ships a standalone JRE — the JDK itself is used for both development and deployment.

**When you need what:**
- Writing and compiling Java code → JDK
- Running a compiled Java program → JDK (since Java 11; previously JRE was sufficient)
- Shipping to production → JDK, or a custom JRE you build with `jlink`

---

## 1.5 Installing Java 21 and Running Your First Program

### Why Java 21?
Java 21 is a **Long-Term Support (LTS)** release, meaning Oracle and OpenJDK will provide security patches and bug fixes until 2028+. Key features introduced by Java 21 that we use in this book:
- **Virtual Threads** (Project Loom, finalized) — millions of lightweight threads
- **Records** (finalized in Java 16) — compact immutable data classes
- **Sealed Classes** (finalized in Java 17) — exhaustive type hierarchies
- **Pattern Matching** (finalized in Java 16-21 progressively)
- **Switch Expressions** (finalized in Java 14)

Non-LTS releases come every 6 months and are supported for only 6 months — not appropriate for production without careful management. Java 8 is still used in legacy systems, but its concurrency model predates virtual threads and its syntax is verbose. Java 21 is the correct target.

### Installation

**Option 1: SDKMAN (recommended for developers on Linux/macOS)**
```bash
# Install SDKMAN
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install Java 21 (Temurin = open-source, production-grade)
sdk install java 21.0.3-tem

# Verify
java -version
# Output: openjdk version "21.0.3" 2024-04-16
javac -version
# Output: javac 21.0.3
```

**Option 2: Direct download**
Go to https://adoptium.net and download the Temurin 21 installer for your OS.

**Option 3: Homebrew (macOS)**
```bash
brew install openjdk@21
```

### Your First Java Program

Create a file called `HelloWorld.java`:

```java
// File: HelloWorld.java
// IMPORTANT: The class name MUST match the filename exactly (case-sensitive)

public class HelloWorld {
    // main is the entry point. The JVM looks for this exact signature.
    // String[] args holds command-line arguments passed to the program.
    public static void main(String[] args) {
        System.out.println("Hello, Surya! Welcome to Java.");
        System.out.println("Your JavaScript days are not wasted.");
        System.out.println("They're about to get a powerful companion.");
    }
}
```

**Compile and run:**
```bash
# Compile: produces HelloWorld.class in the same directory
javac HelloWorld.java

# Run: JVM loads HelloWorld.class and calls main()
java HelloWorld
```

**Output:**
```
Hello, Surya! Welcome to Java.
Your JavaScript days are not wasted.
They're about to get a powerful companion.
```

**Java 11+ shortcut — single-source file execution:**
```bash
# Skip the compile step for single-file programs
java HelloWorld.java
```

This compiles and runs in one step, keeping the `.class` file in memory. Useful for quick scripts, not for projects.

---

## 1.6 What Happens When You Type `java HelloWorld`

This is the most important question for understanding Java from the inside. When you run `java HelloWorld`, a cascade of events occurs:

```
java HelloWorld
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  1. JVM STARTUP                                     │
│     - OS creates a new process                      │
│     - JVM binary (libjvm.so / jvm.dll) is loaded   │
│     - JVM initializes Heap, Stack, Metaspace        │
│     - Bootstrap ClassLoader is created              │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  2. CLASS LOADING (Three-phase process)             │
│                                                     │
│  Phase A: LOADING                                   │
│     - Bootstrap ClassLoader loads core Java classes │
│       (java.lang.Object, java.lang.String, etc.)   │
│     - Extension ClassLoader loads ext libraries     │
│     - Application ClassLoader finds HelloWorld.class│
│       in the classpath                              │
│     - The .class file's binary data is read from   │
│       disk into the Method Area (Metaspace)         │
│                                                     │
│  Phase B: LINKING                                   │
│     - Verification: bytecode checked for validity  │
│       (no stack overflows, type safety, etc.)       │
│     - Preparation: static fields allocated and set  │
│       to default values (0, null, false)            │
│     - Resolution: symbolic references (class names, │
│       method names as strings) are resolved to      │
│       actual memory addresses in the JVM            │
│                                                     │
│  Phase C: INITIALIZATION                            │
│     - Static initializer blocks run                 │
│     - Static fields assigned their programmed values│
│     - If HelloWorld has "static int X = 5;",       │
│       this is where X gets 5 (Preparation gave it 0)│
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  3. MAIN METHOD INVOCATION                          │
│     - JVM locates: public static void main(String[])│
│     - Creates a new Thread (the "main" thread)      │
│     - Creates a stack frame for main() on the stack │
│     - String[] args array created on Heap           │
│     - Execution begins                              │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  4. EXECUTION ENGINE                                │
│     - Interpreter reads bytecode instructions       │
│     - System.out.println("Hello...") triggers:      │
│       → JVM resolves System class → out field →    │
│          PrintStream object → println() method      │
│       → JVM calls native OS write() syscall        │
│       → OS writes to stdout file descriptor         │
│       → Terminal displays the text                  │
│     - After ~10,000 calls, JIT compiler compiles   │
│       hot methods to native machine code            │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  5. SHUTDOWN                                        │
│     - main() returns                                │
│     - JVM runs shutdown hooks                       │
│     - Finalizers run (if any — avoid them)          │
│     - JVM process exits with code 0 (success)      │
└─────────────────────────────────────────────────────┘
```

### The Three ClassLoaders in Detail

Java uses a **parent-delegation model** for class loading. When the Application ClassLoader is asked to load `HelloWorld`, it first asks its parent (Extension ClassLoader), which asks *its* parent (Bootstrap ClassLoader). Only if the parent can't find the class does the child try itself. This prevents user code from replacing core Java classes like `java.lang.String`.

```
Bootstrap ClassLoader          ← Loads rt.jar / java.base module
        │ parent of
        ▼
Extension ClassLoader           ← Loads ext/*.jar (jre/lib/ext)
        │ parent of
        ▼
Application ClassLoader         ← Loads your -classpath
        │ parent of
        ▼
Custom ClassLoader (optional)   ← Frameworks (Spring, OSGi) use this
```

**From JavaScript, you can think of:** ClassLoader ≈ Node.js `require()` / module system, except Java's is hierarchical and can run multiple isolated sets of classes in the same JVM (used by application servers like Tomcat to run multiple web apps).

---

## 1.7 The `public static void main(String[] args)` Signature — Explained

Every word in `public static void main(String[] args)` is required for specific reasons:

- **`public`** — The JVM must be able to call this method from outside your class. If it were `private`, the JVM couldn't access it.
- **`static`** — The JVM calls `main()` before creating any objects. If `main` were an instance method, the JVM would need to create a `HelloWorld` object first — but how would it know which constructor to use? Static means the method belongs to the class itself, not an instance.
- **`void`** — The JVM doesn't use a return value from `main`. To return an exit code, you call `System.exit(0)`.
- **`main`** — This is the exact name the JVM's startup code looks for. Not `Main`, not `start`, not `run`. Exactly `main`.
- **`String[] args`** — The command-line arguments passed to the program, as an array of Strings. `java HelloWorld foo bar` → `args = ["foo", "bar"]`.

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "What happens when you run a Java program? Walk me through the complete sequence."**

**SDE-2 Answer:** When you type `java HelloWorld`, the JVM process starts and allocates memory regions — Heap, Stack, Metaspace. The Bootstrap ClassLoader loads core Java classes. Then the Application ClassLoader finds HelloWorld.class on the classpath and loads it through three phases: Loading (binary data read into Metaspace), Linking (bytecode verification, static field preparation with default values, symbolic reference resolution), and Initialization (static initializers and static field assignments run). The JVM then locates the `public static void main(String[])` method, creates the main Thread, pushes a stack frame for main(), and begins execution via the Interpreter. As code paths are executed repeatedly, the JIT compiler kicks in after threshold hits (typically 10,000 invocations) and compiles bytecode to native machine code for that platform. System.out.println ultimately makes a native OS syscall to write to stdout.

**Q2: "What is the difference between JDK, JRE, and JVM?"**

**SDE-2 Answer:** JVM is the execution engine — ClassLoader, bytecode verifier, JIT compiler, GC, and memory manager. It's an abstract specification implemented by HotSpot, GraalVM, etc. JRE is JVM plus the Java standard library (java.lang, java.util, etc.) — everything needed to run a compiled Java program. JDK is JRE plus development tools: javac compiler, javadoc, jdb debugger, jstack, jmap, jconsole, jar tool. Since Java 11, Oracle no longer ships a standalone JRE; the JDK serves both purposes. In production, you'd typically ship the JDK or build a minimal custom runtime using jlink.

**Q3: "Why is Java platform-independent if the JVM is platform-specific?"**

**SDE-2 Answer:** Java source compiles to bytecode — a platform-neutral instruction set for the abstract JVM machine. The bytecode itself is identical regardless of OS or CPU. The JVM implementation, however, is platform-specific: HotSpot on Linux x86-64 translates bytecode to x86 machine instructions, while HotSpot on macOS ARM64 translates the same bytecode to ARM instructions. The platform-specific work is encapsulated inside the JVM, so your bytecode never needs to change. The analogy is a universal recipe (bytecode) that local chefs (JVMs) cook using local techniques (native code generation). The independence lives at the bytecode level; the specificity lives inside the JVM.

---

# CHAPTER 2: JVM Memory Architecture

Understanding JVM memory is not optional for Java engineers. Every production issue — from OutOfMemoryErrors to GC pauses to thread dumps — requires knowing exactly what lives where.

```
┌──────────────────────────────────────────────────────────────────┐
│  JAVASCRIPT VS JAVA: Memory and the Runtime                       │
│                                                                    │
│  JavaScript (V8 engine) also has a heap and call stack:           │
│  • JS Call Stack: one stack, one thread — overflow = RangeError   │
│  • JS Heap: V8 manages it; you cannot set -Xmx                   │
│  • JS GC: you have zero control; it runs when V8 decides          │
│                                                                    │
│  Key difference — Java gives you CONTROL:                         │
│  • -Xmx4g: limit heap to 4GB                                      │
│  • -XX:+HeapDumpOnOutOfMemoryError: capture heap on OOM           │
│  • -XX:+UseG1GC: choose which GC algorithm to use                 │
│  • jcmd <pid> VM.native_memory: inspect memory live               │
│                                                                    │
│  In Node.js backend, if you need more memory: NODE_OPTIONS=       │
│  '--max-old-space-size=4096'. In Java: -Xmx4g at startup.        │
│  Java's control is more granular and the tooling is richer.       │
└──────────────────────────────────────────────────────────────────┘
```

## 2.1 The Complete JVM Memory Layout

```
┌──────────────────────────────────────────────────────────────────┐
│                         JVM PROCESS MEMORY                       │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                        HEAP                                │  │
│  │  (Shared across ALL threads — objects live here)           │  │
│  │                                                            │  │
│  │  ┌──────────────────────────┐  ┌───────────────────────┐  │  │
│  │  │    YOUNG GENERATION      │  │   OLD GENERATION      │  │  │
│  │  │  (New objects born here) │  │  (Long-lived objects) │  │  │
│  │  │                          │  │                       │  │  │
│  │  │  ┌───────┐ ┌───┐ ┌───┐  │  │  ┌─────────────────┐  │  │  │
│  │  │  │ Eden  │ │S0 │ │S1 │  │  │  │  Tenured Space  │  │  │  │
│  │  │  │       │ │   │ │   │  │  │  │                 │  │  │  │
│  │  │  └───────┘ └───┘ └───┘  │  │  └─────────────────┘  │  │  │
│  │  └──────────────────────────┘  └───────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────┐  ┌─────────────────────────────────────┐  │
│  │    METASPACE     │  │        THREAD-PRIVATE AREAS          │  │
│  │  (Class metadata)│  │                                     │  │
│  │                  │  │  Thread 1:  Thread 2:  Thread 3:    │  │
│  │  Class definitions│  │  ┌───────┐ ┌───────┐ ┌───────┐    │  │
│  │  Method bytecode │  │  │ Stack │ │ Stack │ │ Stack │    │  │
│  │  Runtime constant│  │  │frames │ │frames │ │frames │    │  │
│  │  pool            │  │  └───┬───┘ └───┬───┘ └───┬───┘    │  │
│  │  Field/method    │  │      │          │          │        │  │
│  │  descriptors     │  │  ┌───▼───┐ ┌───▼───┐ ┌───▼───┐    │  │
│  │                  │  │  │PC Reg │ │PC Reg │ │PC Reg │    │  │
│  │  Lives in NATIVE │  │  │(instr │ │(instr │ │(instr │    │  │
│  │  memory (not heap│  │  │addr)  │ │addr)  │ │addr)  │    │  │
│  └──────────────────┘  │  └───────┘ └───────┘ └───────┘    │  │
│                         │                                    │  │
│                         │  ┌──────────────────────────────┐ │  │
│                         │  │    NATIVE METHOD STACKS      │ │  │
│                         │  │  (C/C++ native code frames)  │ │  │
│                         │  └──────────────────────────────┘ │  │
│                         └────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

Let's go deep on each region.

---

## 2.2 The Heap: Where Objects Live

The Heap is the largest and most important memory region. Every object created with `new` lives here. The Heap is **shared across all threads** — any thread can read or write any object on the heap (which is why concurrency is hard — more in Chapter 7).

The Heap is divided into **generations** based on the insight that "most objects die young" — this is the **weak generational hypothesis**, empirically validated across almost all programs. A `HashMap.Entry` used in a single request and immediately discarded shouldn't be mixed with a database connection pool that lives for the entire application lifetime.

### Young Generation

The Young Generation is where all new objects are born. It has three sub-regions:

**Eden Space:** Every new object is first allocated in Eden. `new Order()` → object appears in Eden. Eden is typically 80% of the Young Generation's space.

**Survivor Spaces (S0 and S1):** Two equal-sized spaces, always one active and one empty. Objects that survive a Minor GC graduate from Eden into the active Survivor space.

```
Object Lifecycle in Young Generation:

new MyObject() ──→ Eden (empty slot found via pointer bump)
                      │
                      │ Eden fills up
                      ▼
               ╔═══════════════╗
               ║  MINOR GC     ║  (Stop-the-world but very fast: ~1-5ms)
               ╚═══════════════╝
                      │
           ┌──────────┴───────────┐
           ▼                      ▼
      Not reachable?         Still reachable?
      Collected (dead)       Copied to S0 (age=1)
                                   │
                                   │ Next Minor GC
                                   ▼
                              Still reachable?
                              Copied to S1 (age=2)
                                   │
                                   │ age >= threshold (default 15)
                                   ▼
                         Promoted to OLD GENERATION
```

**Key insight:** Minor GC only scans the Young Generation. Because most objects die in Eden, the live set is tiny, making Minor GC fast. The JVM uses a technique called **pointer bumping** to allocate in Eden — just increment a pointer, no searching for free space.

### Old Generation (Tenured Space)

Objects that survive enough Minor GC cycles get **promoted** to the Old Generation. Old Gen objects are assumed to be long-lived: caches, thread pools, service beans, static collections.

Old Gen is collected by **Major GC (Full GC)**, which is slower and more disruptive because it must scan the entire heap (or at least the entire Old Gen). This is why keeping short-lived objects short-lived matters — objects that accidentally get promoted to Old Gen put pressure on Full GC.

---

## 2.3 The Stack: Where Method Calls Live

Each **Thread** gets its own **Stack** — completely private, not shared with other threads. This is why local variables are inherently thread-safe: other threads can't see your stack.

When a method is called, a **Stack Frame** is pushed onto the thread's stack. When the method returns (or throws an exception), the frame is popped.

```
Thread's Call Stack (top = currently executing):

┌──────────────────────────────────┐
│    Frame: calculateTotal()       │ ← Currently executing
│    local vars: sum=0, i=0       │
│    operand stack: [3, 7]        │
│    return address: line 42 of   │
│    processOrder()                │
├──────────────────────────────────┤
│    Frame: processOrder()         │
│    local vars: order=<ref>, tax  │
│    operand stack: []             │
│    return address: line 18 of   │
│    handleRequest()               │
├──────────────────────────────────┤
│    Frame: handleRequest()        │
│    local vars: req=<ref>         │
│    operand stack: []             │
│    return address: main()        │
├──────────────────────────────────┤
│    Frame: main()                 │
│    local vars: args=<ref>        │
│    operand stack: []             │
│    return address: (JVM start)   │
└──────────────────────────────────┘
        Stack Bottom
```

### What's Inside a Stack Frame

Each frame contains:

1. **Local Variables Array:** All local variables declared in the method, including method parameters. Primitives store their actual value here. Object references store the memory address (pointer) to the object on the Heap.

2. **Operand Stack:** A temporary working area for ongoing computations. When you write `int sum = a + b`, the bytecode pushes `a` and `b` onto the operand stack, pops them, adds them, and pushes the result.

3. **Frame Data:** Return address (where to return after this method), reference to the runtime constant pool.

**Stack size is fixed per thread.** Default is usually 512KB–1MB. Infinite recursion fills the stack → `StackOverflowError`.

---

## 2.4 Metaspace: Class Metadata

Metaspace holds **class-level information** — not objects, but the descriptions of classes:

- Class structure (class name, superclass, interfaces implemented)
- Method bytecode (the actual bytecode instructions for every method)
- Field names and types
- Method signatures
- Runtime Constant Pool (string literals, class references, method references — as symbolic names)
- Annotations
- JIT-compiled native code (HotSpot stores compiled methods here)

**Metaspace is not on the Heap.** It lives in native memory (outside the Java Heap), managed directly by the JVM. This is important: OutOfMemoryError in Metaspace means you're loading too many classes (common in applications that generate classes dynamically, like Hibernate with many entities, or systems that create new ClassLoaders frequently).

### Why Metaspace Replaced PermGen (Java 7 and earlier)

Before Java 8, this area was called **PermGen (Permanent Generation)** and was part of the Heap with a fixed maximum size (`-XX:MaxPermSize`). Developers frequently hit `OutOfMemoryError: PermGen space` in applications that loaded many classes (JSPs, Hibernate entities, Spring beans). PermGen was hard to tune — too small and you OOM, too large and you waste Heap.

Java 8 replaced PermGen with **Metaspace** in native memory. Metaspace grows automatically up to available system memory (`-XX:MaxMetaspaceSize` to cap it). Class unloading (when a ClassLoader is GC'd) frees Metaspace. This eliminated most PermGen OOM issues.

---

## 2.5 PC Register and Native Method Stack

**PC (Program Counter) Register:** One per thread. A tiny register that holds the address of the bytecode instruction currently being executed by that thread. When a thread is switched out by the OS, the PC register is saved so execution can resume exactly where it left off. For native methods (code written in C/C++), the PC register is undefined.

**Native Method Stack:** When Java code calls a native method (a C/C++ function via JNI — Java Native Interface), the native code runs on a separate native stack. This is used by the standard library itself (e.g., `System.arraycopy`, file I/O operations) and by libraries that wrap native C code (cryptography, GPU computing, etc.).

---

## 2.6 Stack vs Heap: What Lives Where

This is one of the most commonly tested concepts. Let's be precise:

```java
public void analyzeOrder() {
    int quantity = 5;              // STACK: primitive, stored directly in frame
    double price = 19.99;          // STACK: primitive, stored directly in frame
    
    String productName = "Widget"; // STACK: reference variable
                                   // HEAP: the "Widget" String object
    
    Order order = new Order();     // STACK: 'order' reference variable
                                   // HEAP: the Order object itself
    
    order.setQuantity(quantity);   // quantity value (5) passed by value on stack
}
// method returns → entire frame popped from stack
// quantity, price, productName variable gone (but "Widget" may survive on Heap)
// order variable gone (but Order object survives if referenced elsewhere)
```

```
STACK (thread-private)           HEAP (shared)
─────────────────────            ─────────────────────────────────────
quantity: 5                      
price: 19.99                     ┌─────────────────────┐
productName: ──────────────────→ │  "Widget" (String)  │
order: ────────────────────────→ ├─────────────────────┤
                                 │  Order object        │
                                 │    quantity: 0       │
                                 │    price: 0.0        │
                                 └─────────────────────┘
```

**The rules:**
- Primitive local variables → Stack (value directly)
- Object local variables → Stack stores the reference; the object is on the Heap
- Instance fields (fields of an object) → Heap (inside the object)
- Static fields → Metaspace (not in the heap in strict terms, though accessible via Heap references in practice; technically stored with class metadata)

**From JavaScript perspective:** In JavaScript, you never think about this distinction because the engine manages everything. In Java, the distinction matters for understanding GC behavior, thread safety, and performance.

---

## 2.7 Object References vs Primitive Values in Memory

```java
int a = 42;        // a IS 42, stored directly
int b = a;         // b gets a COPY of 42; changing b doesn't affect a

String s1 = "Hello";    // s1 holds a REFERENCE (memory address) to the String object
String s2 = s1;         // s2 holds a COPY of the REFERENCE (same address)
                        // Both s1 and s2 point to the same String object
                        // But since String is immutable, this doesn't matter in practice

Order o1 = new Order(); // o1 holds a REFERENCE to the Order object
Order o2 = o1;          // o2 holds a COPY of the REFERENCE
o2.setQuantity(5);      // Modifies the SAME Order object that o1 points to!
System.out.println(o1.getQuantity()); // Prints 5 — this is aliasing
```

**Java passes everything by value — always.** But for objects, the "value" is the reference (address). This is a common source of confusion:

```java
// This does NOT swap the caller's variables
void swap(Order a, Order b) {
    Order temp = a;
    a = b;
    b = temp;
    // Only the LOCAL copies of a and b (references) are swapped
    // The caller's variables are unchanged
}

// This DOES modify the object (because you're mutating through the reference)
void modifyQuantity(Order order) {
    order.setQuantity(999);
    // This mutates the actual object on the Heap
    // Caller sees the change when they access order.getQuantity()
}
```

---

## 2.8 Garbage Collection: Why It Exists and How It Works

In C and C++, you manually allocate memory (`malloc`) and free it (`free`). Forgetting to free causes **memory leaks**. Freeing memory that's still in use causes **use-after-free bugs** and crashes.

Java's GC automatically reclaims memory for objects that are no longer reachable — your code cannot access them anymore. No `free()`, no `delete`, no memory leaks from forgetting to release.

### GC Roots: The Starting Point of Reachability

The GC starts from a set of **GC Roots** — objects that are always considered reachable:

1. **Local variables in active stack frames** — any object referenced by a variable in any thread's current stack frames
2. **Static fields** — any object referenced by a class's static fields
3. **JNI references** — objects referenced by native C/C++ code
4. **Interned strings** — the String pool

The GC does a **reachability traversal** starting from these roots:

```
GC Roots (always reachable)
    │
    ├─→ MyService (static field in Application)
    │       │
    │       ├─→ UserRepository (field of MyService)
    │       │       └─→ DataSource (field of UserRepository)
    │       │
    │       └─→ OrderCache (field of MyService)
    │               └─→ Map<Long, Order> (internal map)
    │                       └─→ Order objects (values in map)
    │
    └─→ HttpRequest (local variable in handleRequest() stack frame)
            └─→ RequestBody (field of HttpRequest)

  NOT reachable → GARBAGE:
    - Order object created earlier, reference went out of scope
    - Temporary StringBuilder created in a completed method
    - Any object with no path from any root
```

Any object with NO path from any GC root to it is **garbage** — the GC collects it.

### Mark-and-Compact / Mark-and-Copy

The JVM uses different GC algorithms for different generations:

**Young Gen (Minor GC) uses Mark-and-Copy:**
1. Mark all reachable objects starting from GC roots
2. Copy all live objects from Eden + active Survivor to the empty Survivor space (compacting them together)
3. Bump the age counter of survived objects
4. Clear Eden and old Survivor space entirely (fast — just reset a pointer)

**Why copying works in Young Gen:** Most objects are dead (weak generational hypothesis). Copying only the survivors (small set) is faster than scanning and compacting the entire space.

---

## 2.9 G1GC: How Modern Java Does Garbage Collection

Java 21 uses **G1GC (Garbage-First Garbage Collector)** by default. G1 was designed to achieve predictable pause times for large heaps.

### G1GC's Key Idea: Heap Regions

Instead of having one contiguous Young Gen and one contiguous Old Gen, G1 divides the entire heap into ~2000 equal-sized **regions** (typically 1MB–32MB each):

```
G1 Heap (example: 4GB total, ~2000 regions of 2MB each):

┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ E │ E │ E │ S │ O │ O │ F │ E │ O │ H │ F │ E │  ...2000 regions
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
 E = Eden    S = Survivor    O = Old    F = Free    H = Humongous
```

**Region types:**
- **Eden:** New object allocation
- **Survivor:** Young Gen survivors
- **Old:** Promoted objects
- **Free:** Available for any purpose
- **Humongous:** Objects larger than 50% of a region size (allocated in consecutive regions)

### G1 Collection Cycle

**1. Minor GC (Young-Only Collection):**
- Scans only Eden and Survivor regions
- Live objects copied to new Survivor or Old regions
- Eden regions become Free
- Fast, stop-the-world, ~1-10ms

**2. Concurrent Marking (background):**
- G1 identifies which Old regions have the most garbage (concurrent with your application — no pause)
- Builds a **remembered set** of cross-region references

**3. Mixed GC:**
- Collects ALL Eden/Survivor regions + the most garbage-dense Old regions
- "Garbage First" = collect regions with the most garbage first
- Allows meeting pause time goals by only collecting as many Old regions as can fit in the pause budget

**4. Full GC (fallback):**
- If G1 can't keep up, it falls back to a stop-the-world Full GC (single-threaded — very slow)
- Indicates the heap is too small or objects are being promoted too fast

### JVM GC Flags

```bash
# Run with G1GC (default in Java 9+)
java -XX:+UseG1GC MyApp

# Pause target: aim for 200ms max pauses
java -XX:MaxGCPauseMillis=200 MyApp

# Use ZGC for ultra-low latency (<1ms pauses, Java 15+)
java -XX:+UseZGC MyApp

# Log GC events to a file for analysis
java -Xlog:gc*:file=gc.log:time,uptime MyApp
```

---

## 2.10 Common Memory Errors

```java
// 1. OutOfMemoryError: Java heap space
//    You've filled the heap with objects the GC can't collect
List<byte[]> leak = new ArrayList<>();
while (true) {
    leak.add(new byte[1024 * 1024]); // 1MB per iteration
    // GC can't collect these — 'leak' holds strong references to all of them
}
// java.lang.OutOfMemoryError: Java heap space

// 2. OutOfMemoryError: Metaspace
//    You've loaded too many classes (usually a class generation/reflection issue)
// Happens with ORMs with thousands of entities, or frameworks that generate proxies

// 3. StackOverflowError
//    Infinite recursion fills the thread's stack
public void infinite() {
    infinite(); // Each call pushes a new frame; stack fills up
}
// java.lang.StackOverflowError
```

### Essential JVM Flags

```bash
# Minimum heap size (JVM starts with at least this)
-Xms512m

# Maximum heap size (JVM never exceeds this)
-Xmx2g

# Dump heap contents to a file when OOM occurs (for analysis with tools like Eclipse MAT)
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/tmp/heap-dump.hprof

# Cap Metaspace (default: unlimited up to OS limits)
-XX:MaxMetaspaceSize=256m

# Thread stack size (default ~512KB on most platforms)
-Xss512k

# Production recommended settings:
java -Xms2g -Xmx2g \                        # Fixed heap (avoids resizing pauses)
     -XX:+UseG1GC \                          # G1 GC
     -XX:MaxGCPauseMillis=200 \             # Target pause
     -XX:+HeapDumpOnOutOfMemoryError \       # Dump on OOM
     -XX:HeapDumpPath=/logs/heap.hprof \    # Where to dump
     -Xlog:gc*:file=/logs/gc.log:time \     # GC logging
     -jar myapp.jar
```

**Why set `-Xms` equal to `-Xmx`?** In production, you want the JVM to commit all the memory it will ever use upfront. If the heap starts small and grows, each resize triggers a Full GC. Fixed heap = no resize GCs.

---

## 2.11 Complete Memory Example with Code

```java
public class MemoryDemo {
    // Static field → stored in Metaspace (class-level)
    private static final String APP_NAME = "MyApp";
    
    // Instance field → stored in Heap (inside each MemoryDemo object)
    private int instanceCount;
    
    public static void main(String[] args) {
        // 'main' stack frame pushed onto main-thread's stack
        // args: reference on stack, String[] object on heap
        
        int localPrimitive = 42;          // Stack: value directly
        String localRef = "Hello";         // Stack: reference; "Hello" in String pool (Heap)
        
        MemoryDemo demo = new MemoryDemo(); // Stack: 'demo' reference
                                           // Heap: MemoryDemo object
        
        demo.processData();                // New stack frame pushed
        
        // demo.processData() returns → frame popped
        // After main() returns: localPrimitive, localRef gone from stack
        // demo reference gone from stack
        // MemoryDemo object on Heap: eligible for GC (no more references)
    }
    
    public void processData() {
        // New stack frame for processData
        int[] numbers = new int[]{1, 2, 3}; // Stack: 'numbers' reference
                                             // Heap: int[] array object
        
        StringBuilder sb = new StringBuilder(); // Stack: 'sb' reference
                                                // Heap: StringBuilder object
        
        for (int n : numbers) {              // n: local var on stack
            sb.append(n);
        }
        
        String result = sb.toString();      // Stack: 'result' reference
                                           // Heap: new String object
        
        System.out.println(result);         // JVM calls println
        
        // Method ends: numbers, sb, result, n all gone from stack
        // The int[] array and StringBuilder are now eligible for GC
        // The result String may survive if it gets referenced elsewhere
    }
}
```

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "Explain the difference between Heap, Stack, and Metaspace."**

**SDE-2 Answer:** The Heap is shared across all threads and is where objects live — anything created with `new`. It's divided into Young Generation (Eden + two Survivor spaces) and Old Generation (Tenured). All GC activity targets the Heap. The Stack is thread-private — every thread gets its own stack. Method calls push frames; each frame holds local variables (primitives store actual values, object variables store references/addresses) and the operand stack for in-progress computations. When a method returns, its frame is popped and all its local variables are gone. Metaspace is also per-JVM but not on the Heap — it's native memory holding class definitions, method bytecode, field descriptors, and the runtime constant pool. It replaced PermGen in Java 8, growing dynamically up to available system memory rather than having a fixed cap.

**Q2: "What causes an OutOfMemoryError? What would you do to diagnose it in production?"**

**SDE-2 Answer:** There are three flavors: heap OOM (objects accumulate faster than GC can collect them — usually a memory leak where strong references prevent collection), Metaspace OOM (too many classes loaded, common with frameworks that generate bytecode at runtime like Hibernate), and native memory OOM (off-heap allocations exceed OS limits, seen with DirectByteBuffers in NIO). To diagnose: first, ensure `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/heap.hprof` is set in production. Capture the heap dump when OOM occurs, then analyze with Eclipse Memory Analyzer (MAT) or IntelliJ's heap analyzer. Look for the "Leak Suspects" report — it usually identifies which class is accumulating objects and which root reference is holding them alive. Also review GC logs for Full GC frequency and efficiency (if GC is running constantly but recovering almost no memory, you have a leak).

**Q3: "How does Garbage Collection know what to collect? What is a GC Root?"**

**SDE-2 Answer:** GC uses reachability analysis, not reference counting. It starts from a fixed set of GC roots — local variables in active thread stacks, static fields, JNI references, and interned strings — and traverses the object reference graph. Any object reachable from a root through any chain of references is considered live. Everything else is garbage. This correctly handles circular references, which would trip up reference counting (if A references B and B references A but nothing else references either, they're unreachable even though their reference counts are non-zero). In Java, you can also influence reachability with `SoftReference` (collected under memory pressure), `WeakReference` (collected on next GC), and `PhantomReference` (for cleanup actions after collection).

# CHAPTER 3: Java Syntax from Scratch

## 3.1 Variables: Declaration, Initialization, and Naming

In JavaScript you write `let x = 5`. In Java, you must declare the **type** explicitly:

```java
// JavaScript: let x = 5;
// Java:
int x = 5;          // declare type, name, and initial value in one line

int count;          // declared but NOT initialized
// System.out.println(count); // ← COMPILE ERROR: "variable count might not have been initialized"
// Java forces you to initialize local variables before reading them

int total = 0;      // correct — initialized
total = total + 1;  // reassignment
```

**Naming conventions in Java (strictly followed by all Java engineers):**
- Variables and methods: `camelCase` → `orderTotal`, `getUserById`
- Classes and interfaces: `PascalCase` → `OrderService`, `UserRepository`
- Constants (static final): `UPPER_SNAKE_CASE` → `MAX_RETRIES`, `DEFAULT_TIMEOUT`
- Packages: all lowercase, reverse domain → `com.company.service`

```java
// Good Java naming
int userAge = 25;
String firstName = "Surya";
final int MAX_CONNECTIONS = 100;    // constant

class OrderProcessor { }            // class
interface PaymentGateway { }        // interface
```

---

## 3.2 Primitive Types: The Eight Building Blocks

Java has exactly 8 primitive types. These are **not objects** — they are raw values stored directly (on the stack if local, inside the object if fields). This is fundamentally different from JavaScript where everything is an object (even numbers).

```
┌──────────────┬──────────┬────────────────────────────────────────────────────┐
│ Type         │ Size     │ Range / Notes                                      │
├──────────────┼──────────┼────────────────────────────────────────────────────┤
│ byte         │ 8 bits   │ -128 to 127                                        │
│ short        │ 16 bits  │ -32,768 to 32,767                                  │
│ int          │ 32 bits  │ -2,147,483,648 to 2,147,483,647 (≈ ±2.1 billion)  │
│ long         │ 64 bits  │ ±9.2 × 10^18 (append L: 100L)                     │
│ float        │ 32 bits  │ ~±3.4 × 10^38, ~7 decimal digits (append f: 3.14f)│
│ double       │ 64 bits  │ ~±1.8 × 10^308, ~15 decimal digits (default float)│
│ char         │ 16 bits  │ 0 to 65,535 (Unicode, single quotes: 'A')         │
│ boolean      │ ~1 bit*  │ true or false only (* JVM uses 1 byte in practice) │
└──────────────┴──────────┴────────────────────────────────────────────────────┘
```

**Default values** (when declared as fields, not local variables):

```java
class Defaults {
    byte   b;     // 0
    short  s;     // 0
    int    i;     // 0
    long   l;     // 0L
    float  f;     // 0.0f
    double d;     // 0.0
    char   c;     // '\u0000' (null character)
    boolean flag; // false
    String str;   // null  (String is an object, not a primitive)
}
```

```java
public class PrimitiveDemo {
    public static void main(String[] args) {
        // Integer types
        byte age = 25;
        short year = 2024;
        int population = 1_400_000_000;  // underscores for readability (Java 7+)
        long nationalDebt = 33_000_000_000_000L; // must append L for long literals

        // Floating-point
        float pi = 3.14159f;    // must append f; otherwise Java treats literal as double
        double precise = 3.141592653589793; // default floating-point type

        // CRITICAL: Never use float/double for money
        double d1 = 0.1 + 0.2;
        System.out.println(d1); // 0.30000000000000004 — IEEE 754 floating-point representation
        // Use java.math.BigDecimal for financial calculations

        // Character
        char letter = 'A';
        char unicode = '\u00E9'; // é
        char newline = '\n';    // escape sequences

        // Boolean
        boolean isActive = true;
        boolean hasError = false;
        // Java booleans are NOT integers. if (1) is a compile error.
        // Unlike JavaScript where if (1) is truthy.

        System.out.printf("age=%d, pi=%.2f, letter=%c%n", age, pi, letter);
    }
}
```

---

## 3.3 Integer Overflow: What Happens at the Boundary

```java
public class OverflowDemo {
    public static void main(String[] args) {
        int max = Integer.MAX_VALUE; // 2,147,483,647
        System.out.println(max);         // 2147483647
        System.out.println(max + 1);     // -2147483648 ← OVERFLOW, wraps around!

        int min = Integer.MIN_VALUE; // -2,147,483,648
        System.out.println(min - 1);     // 2147483647 ← wraps the other way

        // Java does NOT throw an exception on integer overflow — it silently wraps.
        // This is a classic C-inherited behavior.
        // Fix: use long for potentially large values
        long safeMax = (long) Integer.MAX_VALUE + 1; // 2147483648L — correct
        
        // Or use Math.addExact() which throws ArithmeticException on overflow
        try {
            int result = Math.addExact(Integer.MAX_VALUE, 1);
        } catch (ArithmeticException e) {
            System.out.println("Overflow detected: " + e.getMessage()); // integer overflow
        }
    }
}
```

**Why this matters in interviews:** The classic binary search overflow bug:
```java
// WRONG — mid can overflow when lo and hi are large
int mid = (lo + hi) / 2;

// CORRECT — no overflow possible
int mid = lo + (hi - lo) / 2;
```

---

## 3.4 Autoboxing and Unboxing: Primitives Meet Objects

Java has **wrapper classes** for each primitive type. These are real objects, living on the Heap:

```
int       ↔   Integer
long      ↔   Long
double    ↔   Double
float     ↔   Float
byte      ↔   Byte
short     ↔   Short
char      ↔   Character
boolean   ↔   Boolean
```

You need wrapper classes when:
- Storing primitives in Collections (`List<int>` is illegal; `List<Integer>` is correct)
- Using `null` to represent absence of a value
- Calling methods like `Integer.parseInt("42")`

**Autoboxing** is the compiler automatically converting a primitive to its wrapper:
```java
int primitive = 42;
Integer wrapped = primitive;   // autoboxing: compiler inserts Integer.valueOf(42)

List<Integer> list = new ArrayList<>();
list.add(5);                   // autoboxing: 5 → Integer.valueOf(5)
```

**Unboxing** is the reverse:
```java
Integer wrapped = Integer.valueOf(100);
int primitive = wrapped;       // unboxing: compiler inserts wrapped.intValue()

int sum = list.get(0) + 1;    // unboxing the list element before addition
```

**Performance cost of autoboxing:**
```java
// SLOW — autoboxing in a hot loop (1 million Integer objects created on Heap)
long sum = 0;
List<Integer> numbers = new ArrayList<>();
for (int i = 0; i < 1_000_000; i++) {
    numbers.add(i);     // autoboxing: new Integer object each time
}
for (Integer n : numbers) {
    sum += n;           // unboxing: n.longValue() each time
}

// FAST — use int[] array for number crunching
int[] arr = new int[1_000_000];
// no autoboxing, values stored directly in array
```

**Null trap with unboxing:**
```java
Integer nullableInt = null;
int i = nullableInt;    // NullPointerException at runtime — unboxing null!
// Always check for null before unboxing
if (nullableInt != null) {
    int i2 = nullableInt; // safe
}
```

---

## 3.5 The Integer Cache Trap: Why `==` Lies to You

This is one of Java's most famous interview questions.

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b);   // true — but WHY?

Integer c = 128;
Integer d = 128;
System.out.println(c == d);   // false — same code, different result!
```

**The internal explanation:**

`Integer a = 127` triggers autoboxing, which calls `Integer.valueOf(127)`. The `Integer.valueOf()` method contains this optimization:

```java
// Simplified source of Integer.valueOf() (from OpenJDK)
public static Integer valueOf(int i) {
    if (i >= IntegerCache.low && i <= IntegerCache.high) {
        return IntegerCache.cache[i + (-IntegerCache.low)];  // return CACHED object
    }
    return new Integer(i);  // create NEW object
}
```

The `IntegerCache` is a static array of pre-created `Integer` objects for values **-128 to 127**, initialized at JVM startup:

```java
// IntegerCache static initializer (simplified)
static {
    cache = new Integer[(high - low) + 1];
    for (int k = 0; k < cache.length; k++) {
        cache[k] = new Integer(low + k);  // pre-create -128 to 127
    }
}
```

So when you write `Integer a = 127` and `Integer b = 127`, **both variables point to the exact same cached object**. `a == b` compares references → same object → `true`.

When you write `Integer c = 128`, there's no cache entry. `Integer.valueOf(128)` creates a **new** object each time. `c == d` compares references to two **different** objects → `false`.

**The fix: always use `.equals()` for Integer comparison:**
```java
Integer c = 128;
Integer d = 128;
System.out.println(c.equals(d));  // true — compares values, not references
System.out.println(c == d);       // false — DO NOT USE == for Integer
```

**The cache range can be extended with a JVM flag:**
```bash
java -XX:AutoBoxCacheMax=1000 MyApp  # cache -128 to 1000
```

**JavaScript comparison:** In JavaScript, `===` on numbers always compares values because JS numbers are not objects. Java's `==` on Integer compares object identity (references), which is why you need `.equals()`.

---

## 3.6 String: The Special Class

### Why String Is a Class, Not a Primitive

`String` is a class (`java.lang.String`), but Java gives it special syntax (`"hello"` literal) and special behavior (immutability, string pool, `+` operator). Think of it as a "privileged" class.

### String Immutability

Once a `String` object is created, its contents **cannot change**:

```java
String s = "Hello";
s.toUpperCase();              // creates a NEW String "HELLO", does NOT modify s
System.out.println(s);        // still "Hello" — s is unchanged

// To use the result, capture it
String upper = s.toUpperCase();
System.out.println(upper);    // "HELLO"

// Even concatenation creates a new String:
String s2 = "Hello";
s2 = s2 + " World";          // creates NEW String "Hello World", reassigns s2
                              // original "Hello" object still exists until GC'd
```

**Why immutability?** Several benefits: thread safety (immutable objects can be shared freely between threads without synchronization), security (class names, passwords, file paths can't be modified after validation), String pool efficiency (safe to share objects because they can't be mutated).

### The String Pool

Java maintains a **String Pool** (also called interned string pool) — a special area in the Heap where String literals are stored and shared:

```java
String a = "hello";   // "hello" created in String pool
String b = "hello";   // "hello" already exists in pool — b gets the SAME reference

System.out.println(a == b);        // true — same pool object
System.out.println(a.equals(b));   // true — same content

// new String() bypasses the pool — creates a NEW object on the Heap
String c = new String("hello");    // "hello" object NOT in pool (but pool entry still exists)
String d = new String("hello");    // another new object

System.out.println(a == c);        // false — different objects
System.out.println(c == d);        // false — different objects
System.out.println(c.equals(d));   // true — same content

// intern() forces a String to the pool and returns the pool reference
String e = c.intern();             // e now points to the pool entry
System.out.println(a == e);        // true — now both point to pool
```

**Memory diagram:**
```
String Pool (Heap)       Regular Heap
──────────────────       ─────────────────────────────────
┌──────────────┐         ┌──────────────┐  ┌──────────────┐
│  "hello"     │         │ new String() │  │ new String() │
│  (shared)    │         │   "hello"    │  │   "hello"    │
└──────────────┘         └──────────────┘  └──────────────┘
    ↑    ↑                    ↑                  ↑
    a    b                    c                  d
```

### `==` vs `.equals()` — The Single Most Important Java Rule

```java
// == compares REFERENCES (memory addresses), NOT content
// .equals() compares CONTENT

String s1 = "Java";
String s2 = "Java";
String s3 = new String("Java");

System.out.println(s1 == s2);       // true  (same pool object)
System.out.println(s1 == s3);       // false (different objects)
System.out.println(s1.equals(s3));  // true  (same content)

// For all objects: use .equals() to compare content
// Use == only when you deliberately want to check if two variables
// point to the exact same object in memory (rare)

// Common mistake:
if (userInput == "yes") { }         // WRONG — almost never works correctly
if (userInput.equals("yes")) { }    // CORRECT
if ("yes".equals(userInput)) { }    // BEST — null-safe (won't NPE if userInput is null)
```

---

```
┌──────────────────────────────────────────────────────────────────┐
│  JAVASCRIPT VS JAVA: Strings                                       │
│                                                                    │
│  Both JavaScript and Java have immutable strings.                  │
│  The difference is HOW they handle string building:               │
│                                                                    │
│  JavaScript (good):                                                │
│  const result = parts.join('');           // O(n), one allocation  │
│  const result = `Hello ${name}`;          // template literals O(n)│
│  JavaScript concatenation in loops: also bad in theory but        │
│  V8 optimizes it via internal "rope" strings in many cases.       │
│                                                                    │
│  Java (explicit):                                                  │
│  str += part;              // O(n²) — creates new String each time │
│  new StringBuilder();      // O(n)  — mutable buffer, then toString│
│                                                                    │
│  Rule: In Java, always use StringBuilder inside loops.            │
│  The compiler auto-optimizes simple `"a" + "b"` to StringBuilder, │
│  but it CANNOT optimize `str += part` inside a loop.              │
│                                                                    │
│  String pool (Java only): "hello" == "hello" is true because      │
│  both point to the same pool object. new String("hello") ==       │
│  "hello" is FALSE (different object reference). Always use        │
│  .equals() for String comparison in Java.                         │
└──────────────────────────────────────────────────────────────────┘
```

## 3.7 StringBuilder: Efficient String Construction

### Why String Concatenation in a Loop Is O(n²)

```java
// SLOW — do NOT do this
String result = "";
for (int i = 0; i < 1000; i++) {
    result = result + i + ",";  // creates a NEW String object every iteration
}
// Iteration 1: "" + "0" + "," → creates "0,"
// Iteration 2: "0," + "1" + "," → creates "0,1,"
// Iteration 3: "0,1," + "2" + "," → creates "0,1,2,"
// ...copying grows by 1 each time: 0+2+4+6+...+2000 ≈ O(n²) total copies
```

```java
// FAST — use StringBuilder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i).append(",");   // modifies the same buffer — O(1) amortized per append
}
String result = sb.toString();  // ONE final conversion to String
// Total work: O(n) — linear in the number of characters
```

**How StringBuilder works internally:**
- `StringBuilder` wraps a `char[]` (a character array) with initial capacity 16
- `append()` copies characters into the array; if the array fills up, it doubles in size (same amortized growth as ArrayList)
- `toString()` creates a single new String from the internal array

```java
StringBuilder sb = new StringBuilder(100); // pre-size to avoid resizes if you know the rough size
sb.append("Hello")
  .append(", ")
  .append("Surya")
  .append("!")
  .insert(0, "[START] ")            // insert at index 0
  .replace(8, 13, "World")          // replace chars at index 8–13
  .delete(0, 8)                     // delete chars 0–8
  .reverse();                       // reverse
String result = sb.toString();

// StringBuilder is NOT thread-safe — don't share between threads
// StringBuffer is thread-safe but slower — rarely needed
```

**When the compiler is smart about `+`:**
```java
// Java compiler optimizes: String s = "Hello" + " " + "World";
// At compile time, this becomes: String s = "Hello World";  ← single literal
// No StringBuilder needed

// But inside a loop or with runtime values, compiler can't optimize:
// Java 9+ uses StringConcatFactory (invokedynamic) which is cleverer than StringBuilder
// but still creates intermediate objects — use StringBuilder for many concatenations
```

---

## 3.8 Type Casting: Widening and Narrowing

```java
// WIDENING CONVERSION — automatic, no data loss, no syntax needed
byte  b = 100;
short s = b;    // byte → short: OK
int   i = s;    // short → int: OK
long  l = i;    // int → long: OK
float f = l;    // long → float: may lose precision but not range
double d = f;   // float → double: OK

// Widening direction:
// byte → short → int → long → float → double
//                       ↓
//                      char

// NARROWING CONVERSION — explicit cast required, may lose data
double pi = 3.14159;
int approx = (int) pi;  // explicit cast: drops decimal → 3 (truncates, not rounds)
System.out.println(approx); // 3

int large = 300;
byte small = (byte) large; // 300 in binary: 0001_0010_1100
                           // byte takes lower 8 bits: 0010_1100 = 44
System.out.println(small); // 44 — data loss!

// Narrowing for char ↔ int
char c = 'A';
int ascii = c;            // widening: 65 (ASCII code for 'A')
char back = (char) 65;   // narrowing with cast: 'A'

// Checking before narrowing
double value = 9.99;
if (value >= Integer.MIN_VALUE && value <= Integer.MAX_VALUE) {
    int safe = (int) value; // guaranteed to not overflow
}
```

---

## 3.9 Operators

### Arithmetic and Assignment
```java
int a = 10, b = 3;
System.out.println(a + b);   // 13
System.out.println(a - b);   // 7
System.out.println(a * b);   // 30
System.out.println(a / b);   // 3  — INTEGER division, truncates (not 3.333...)
System.out.println(a % b);   // 1  — remainder (modulus)

double d = (double) a / b;   // 3.333... — cast one operand to force float division

// Compound assignment
a += 5;   // a = a + 5 = 15
a -= 3;   // a = a - 3 = 12
a *= 2;   // a = a * 2 = 24
a /= 4;   // a = a / 4 = 6
a %= 4;   // a = a % 4 = 2

// Increment/Decrement
int x = 5;
System.out.println(x++); // 5 — post-increment: use x (5), THEN increment
System.out.println(x);   // 6 — x is now 6
System.out.println(++x); // 7 — pre-increment: increment first, THEN use
```

### Comparison Operators
```java
int a = 5, b = 10;
a == b   // false — equal to
a != b   // true  — not equal to
a < b    // true  — less than
a > b    // false — greater than
a <= b   // true  — less than or equal
a >= b   // false — greater than or equal

// Remember: == on objects compares references, not values
// Use .equals() for content comparison
```

### Logical Operators — Short-Circuit Behavior

```java
boolean result;

// && (AND): short-circuits — if left is false, right is NOT evaluated
result = false && someExpensiveMethod(); // someExpensiveMethod() is NEVER called

// || (OR): short-circuits — if left is true, right is NOT evaluated
result = true || someExpensiveMethod();  // someExpensiveMethod() is NEVER called

// & and | (non-short-circuit): always evaluate BOTH sides
result = false & someExpensiveMethod(); // someExpensiveMethod() IS called
// Use & only when right side has intentional side effects you need (rare)

// Practical short-circuit usage
String name = null;
if (name != null && name.length() > 0) {  // safe: if name is null, length() not called
    System.out.println(name.toUpperCase());
}

// ^ (XOR): true if exactly one is true
System.out.println(true ^ true);   // false
System.out.println(true ^ false);  // true
System.out.println(false ^ false); // false

// ! (NOT)
boolean flag = true;
System.out.println(!flag); // false
```

### Bitwise Operators
```java
int a = 0b1010; // 10 in binary
int b = 0b1100; // 12 in binary

System.out.println(a & b);   // 0b1000 = 8  — AND: bits set in BOTH
System.out.println(a | b);   // 0b1110 = 14 — OR: bits set in EITHER
System.out.println(a ^ b);   // 0b0110 = 6  — XOR: bits set in ONE but not both
System.out.println(~a);      // bitwise NOT: flip all bits = -11 (two's complement)

// Shifts
System.out.println(a << 1);  // 0b10100 = 20 — left shift by 1 = multiply by 2
System.out.println(a >> 1);  // 0b0101  = 5  — right shift by 1 = divide by 2 (preserves sign)
System.out.println(-16 >>> 1); // unsigned right shift: fills with 0s (not sign bit)

// Bitwise tricks used in HashMap (Chapter 5):
int capacity = 16;
int hash = 42;
int bucketIndex = hash & (capacity - 1); // same as hash % capacity when capacity is power of 2
                                         // but much faster — single bitwise AND vs division
```

---

#### The Unsigned Right Shift `>>>` — Deep Dive

Java has three shift operators, and the difference between `>>` and `>>>` is
one of the most commonly misunderstood aspects of Java. This distinction matters
not just academically — Java's HashMap uses `>>>` internally, and understanding
why reveals something deep about how the Collections framework is designed.

**The three shift operators:**

```java
public class ShiftOperators {
    public static void main(String[] args) {

        // LEFT SHIFT: << (same for signed and unsigned)
        // Shifts bits left, fills right with zeros
        // Equivalent to multiplying by 2 for each shift position
        int n = 5;    // binary: 00000000 00000000 00000000 00000101
        System.out.println(n << 1);   // 10  (00...01010) — multiply by 2
        System.out.println(n << 3);   // 40  (00...101000) — multiply by 8

        // SIGNED RIGHT SHIFT: >> (preserves sign bit)
        // Shifts bits right, fills left with the SIGN BIT (0 for positive, 1 for negative)
        // Equivalent to integer division by 2 for each shift position
        int positive = 100;   // 00000000 00000000 00000000 01100100
        int negative = -100;  // 11111111 11111111 11111111 10011100

        System.out.println(positive >> 1);  // 50  (0 shifted in on left — still positive)
        System.out.println(negative >> 1);  // -50 (1 shifted in on left — still negative!)

        // UNSIGNED RIGHT SHIFT: >>> (always fills with 0)
        // Shifts bits right, fills left with ZEROS regardless of sign
        // Treats the number as if it were unsigned
        System.out.println(positive >>> 1);  // 50           (same as >>  for positives)
        System.out.println(negative >>> 1);  // 2147483598   (different! 0 shifted in)
        // negative >>> 1: 11111111...10011100 becomes 01111111...11001110 = 2147483598

        // The dramatic difference:
        System.out.println(Integer.MIN_VALUE >> 1);   // -1073741824 (still negative)
        System.out.println(Integer.MIN_VALUE >>> 1);  // 1073741824  (becomes positive!)
    }
}
```

**Step-by-step trace of -100 with both operators:**

```
-100 in binary (two's complement, 32 bits):
11111111 11111111 11111111 10011100

After -100 >> 1 (signed shift — preserve sign bit):
[1]1111111 11111111 11111111 11001110
 ↑ 1 shifted in (matching original sign bit)
= 11111111 11111111 11111111 11001110
= -50 ✓ (negative preserved)

After -100 >>> 1 (unsigned shift — always fill 0):
[0]1111111 11111111 11111111 11001110
 ↑ 0 always shifted in (regardless of sign)
= 01111111 11111111 11111111 11001110
= 2147483598 (large positive number!)
```

**Where Java uses `>>>` internally — HashMap's hash function:**

```java
// From OpenJDK source — HashMap.java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    //                                                     ↑
    //                             MUST be >>> not >> — here is why:
}

// If hashCode() returns -1640531527 (common negative value):
int h = -1640531527;
// Binary: 11111110 00000000 00000000 00111001

// With >> 16 (signed shift):
int signed = h >> 16;    // 11111111 11111111 11111110 00000000
                         // (-512 — filled with 1s — corrupts the XOR)

// With >>> 16 (unsigned shift):
int unsigned = h >>> 16; // 00000000 00000000 11111110 00000000
                         // (65024 — clean XOR material regardless of sign)

// HashMap uses >>> so ALL hashCode values — positive AND negative —
// get the same XOR spreading treatment. Sign-extension would make negative
// hashCodes spread differently than positive ones.
int bucket = (h ^ (h >>> 16)) & (capacity - 1);
// This works correctly for any hashCode value, negative or positive
```

**When you would write `>>>` in your own code:**

```java
// Finding the middle of two integers without overflow:
// Naive: (low + high) / 2  — OVERFLOWS when low + high > Integer.MAX_VALUE
// Correct: (low + high) >>> 1  — always works, treats sum as unsigned

public int binarySearch(int[] arr, int target) {
    int low = 0, high = arr.length - 1;
    while (low <= high) {
        int mid = (low + high) >>> 1;  // safe mid-point, no overflow
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}
// Note: Java's Arrays.binarySearch() uses this exact >>> trick in its source code
```

**Interview answer:** "The `>>>` operator is an unsigned right shift — it always
fills vacated bits with zeros regardless of whether the original number was positive
or negative. Java uses it in HashMap's hash function specifically because any
hashCode() implementation can return negative numbers, and `>>>` ensures both
positive and negative hashCodes get the same consistent bit-spreading treatment.
If Java used `>>` instead, negative hashCodes would be filled with 1-bits during
spreading, creating a bias toward certain buckets. I also use `>>>` for finding
midpoints in binary search to avoid integer overflow."

---

## 3.10 Control Flow

### if / else if / else
```java
int score = 75;

if (score >= 90) {
    System.out.println("A");
} else if (score >= 80) {
    System.out.println("B");
} else if (score >= 70) {
    System.out.println("C");
} else {
    System.out.println("F");
}

// Ternary operator
String grade = score >= 60 ? "Pass" : "Fail";

// Nested ternary (readable with care, abused easily)
String letter = score >= 90 ? "A" : score >= 80 ? "B" : score >= 70 ? "C" : "F";
```

### Switch Expression (Java 14+ Arrow Syntax) — The Modern Way

```java
// Old switch statement (Java ≤ 13) — fall-through is a common bug source
int day = 3;
switch (day) {
    case 1: System.out.println("Monday"); break;    // break required!
    case 2: System.out.println("Tuesday"); break;
    case 3: System.out.println("Wednesday"); break; // falls through to next without break
    default: System.out.println("Other");
}

// NEW: Switch expression with arrow syntax (Java 14+) — no fall-through, must be exhaustive
String dayName = switch (day) {
    case 1 -> "Monday";
    case 2 -> "Tuesday";
    case 3 -> "Wednesday";
    case 4 -> "Thursday";
    case 5 -> "Friday";
    case 6 -> "Saturday";
    case 7 -> "Sunday";
    default -> "Invalid";
};
System.out.println(dayName); // "Wednesday"

// Switch expression with blocks (for multi-line cases)
int numLetters = switch (dayName) {
    case "Monday", "Friday", "Sunday" -> 6;     // multiple labels
    case "Tuesday" -> 7;
    case "Wednesday" -> 9;
    case "Thursday", "Saturday" -> 8;
    default -> {
        System.out.println("Unknown day: " + dayName);
        yield -1;   // yield returns the value from a block
    }
};

// Switch on Strings (Java 7+)
String command = "start";
switch (command) {
    case "start" -> System.out.println("Starting...");
    case "stop"  -> System.out.println("Stopping...");
    default      -> System.out.println("Unknown command");
}
```

### Loops

```java
// while loop
int i = 0;
while (i < 5) {
    System.out.print(i + " "); // 0 1 2 3 4
    i++;
}

// do-while — executes body at least once
int n = 0;
do {
    System.out.println("Executed at least once"); // prints even if condition is false
    n++;
} while (n < 0);

// for loop
for (int j = 0; j < 5; j++) {
    System.out.print(j + " "); // 0 1 2 3 4
}
// j is out of scope here — scoped to the for loop

// Multiple initialization/update
for (int lo = 0, hi = 10; lo < hi; lo++, hi--) {
    System.out.printf("lo=%d, hi=%d%n", lo, hi);
}

// Enhanced for-each (Java 5+) — iterates over arrays and Iterable
int[] arr = {10, 20, 30, 40, 50};
for (int val : arr) {
    System.out.print(val + " "); // 10 20 30 40 50
}
// val is READ-ONLY — modifying val does NOT modify arr

List<String> names = List.of("Alice", "Bob", "Charlie");
for (String name : names) {
    System.out.println(name.toUpperCase()); // ALICE, BOB, CHARLIE
}
```

### break, continue, and Labeled Break

```java
// break — exits the innermost enclosing loop or switch
for (int i = 0; i < 10; i++) {
    if (i == 5) break;          // stops loop when i reaches 5
    System.out.print(i + " ");  // 0 1 2 3 4
}

// continue — skips rest of current iteration, goes to next
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) continue;  // skip even numbers
    System.out.print(i + " "); // 1 3 5 7 9
}

// Labeled break — breaks out of an OUTER loop from an inner loop
outer:
for (int row = 0; row < 5; row++) {
    for (int col = 0; col < 5; col++) {
        if (row == 2 && col == 3) {
            break outer;    // breaks out of the 'outer' loop entirely
        }
        System.out.printf("[%d,%d] ", row, col);
    }
}
System.out.println("Done"); // jumps here after break outer

// Labeled continue
outer:
for (int row = 0; row < 3; row++) {
    for (int col = 0; col < 3; col++) {
        if (col == 1) continue outer; // skip to next row iteration
        System.out.printf("[%d,%d] ", row, col);
    }
}
```

---

## 3.11 Methods: Defining, Calling, Overloading

```java
public class MethodDemo {
    
    // Method definition: access modifier, return type, name, parameters
    public int add(int a, int b) {
        return a + b;
    }
    
    // void method: no return value
    public void printGreeting(String name) {
        System.out.println("Hello, " + name + "!");
        // no return statement needed (can use bare 'return;' to exit early)
    }
    
    // Static method: called on the class, not an instance
    public static double circleArea(double radius) {
        return Math.PI * radius * radius;
    }
    
    // Variable arguments (varargs): treated as an array inside the method
    public int sum(int... numbers) {
        // numbers is int[] inside the method
        int total = 0;
        for (int n : numbers) total += n;
        return total;
    }
    
    // Method overloading: same name, different parameter types/count
    // Resolved at COMPILE TIME (static dispatch)
    public String describe(int n)    { return "integer: " + n; }
    public String describe(double d) { return "double: " + d; }
    public String describe(String s) { return "string: " + s; }
    public String describe(int a, int b) { return "two ints: " + a + ", " + b; }
    
    public static void main(String[] args) {
        MethodDemo demo = new MethodDemo();
        
        System.out.println(demo.add(3, 4));         // 7
        demo.printGreeting("Surya");                 // Hello, Surya!
        System.out.println(circleArea(5.0));         // 78.539...
        
        System.out.println(demo.sum());              // 0 (empty varargs)
        System.out.println(demo.sum(1, 2, 3));       // 6
        System.out.println(demo.sum(1, 2, 3, 4, 5)); // 15
        
        // Overloaded methods — compiler picks based on argument types
        System.out.println(demo.describe(42));        // "integer: 42"
        System.out.println(demo.describe(3.14));      // "double: 3.14"
        System.out.println(demo.describe("hello"));   // "string: hello"
        System.out.println(demo.describe(1, 2));      // "two ints: 1, 2"
    }
}
```

---

## 3.12 Arrays: Declaration, Initialization, Multidimensional

```java
import java.util.Arrays;

public class ArrayDemo {
    public static void main(String[] args) {
        // Declaration + allocation (all elements get default value: 0 for int)
        int[] scores = new int[5];
        scores[0] = 95;
        scores[1] = 87;
        // scores[2] = 0 (default)
        // scores[3] = 0 (default)
        scores[4] = 91;
        
        // Declaration + initialization in one line
        int[] primes = {2, 3, 5, 7, 11};
        String[] names = {"Alice", "Bob", "Charlie"};
        
        // Array length (a field, not a method — no parentheses)
        System.out.println(primes.length); // 5
        
        // Array index: 0 to length-1
        System.out.println(primes[0]);   // 2
        System.out.println(primes[4]);   // 11
        // primes[5] → ArrayIndexOutOfBoundsException at runtime
        
        // Arrays utility class
        Arrays.sort(scores);                     // sort in-place
        System.out.println(Arrays.toString(scores)); // [0, 0, 87, 91, 95]
        
        int[] copy = Arrays.copyOf(scores, 3);       // first 3 elements: [0, 0, 87]
        int[] range = Arrays.copyOfRange(scores, 2, 5); // index 2 to 4: [87, 91, 95]
        
        int idx = Arrays.binarySearch(scores, 91);   // 3 (array must be sorted)
        
        int[] filled = new int[5];
        Arrays.fill(filled, 42);                     // [42, 42, 42, 42, 42]
        
        System.out.println(Arrays.equals(copy, range)); // false — different content
        
        // Multidimensional arrays — array of arrays
        int[][] matrix = new int[3][4]; // 3 rows, 4 columns
        matrix[0][0] = 1;
        matrix[2][3] = 12;
        
        // Jagged arrays — rows can have different lengths
        int[][] triangle = new int[3][];
        triangle[0] = new int[]{1};
        triangle[1] = new int[]{2, 3};
        triangle[2] = new int[]{4, 5, 6};
        
        // 2D array initialization
        int[][] grid = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        
        // Iterate 2D array
        for (int[] row : grid) {
            for (int val : row) {
                System.out.printf("%3d", val);
            }
            System.out.println();
        }
        
        // Arrays are objects — array reference on stack, data on heap
        // Copying a reference copies the pointer, not the data
        int[] original = {1, 2, 3};
        int[] aliased = original;      // both point to SAME array
        aliased[0] = 99;
        System.out.println(original[0]); // 99 — original is affected!
        
        int[] trulyCopied = Arrays.copyOf(original, original.length); // deep copy
        trulyCopied[0] = 0;
        System.out.println(original[0]); // 99 — original unaffected
    }
}
```

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "What is the Integer cache? Why does `==` sometimes work and sometimes fail for Integer?"**

**SDE-2 Answer:** `Integer.valueOf()` — which autoboxing always calls — maintains a static cache of `Integer` objects for values -128 to 127. When you box an int in that range, you get back a reference to the cached object rather than a newly created one. So two separately boxed `127` values share the exact same object reference, making `==` return true. For 128 and above, no cache exists: `valueOf(128)` creates a new `Integer` object each call, so `==` compares two different heap objects and returns false. The fix is always using `.equals()` for comparing `Integer` values. The lesson generalizes: use `==` for primitive types (int, long, etc.) where it means value comparison, and `.equals()` for object types. The cache size can be increased with the JVM flag `-XX:AutoBoxCacheMax`.

**Q2: "Why is String immutable in Java? What are the benefits?"**

**SDE-2 Answer:** String immutability is an intentional design decision with several benefits. First, the String pool: since String objects can't change, the JVM can safely share them — two variables holding `"hello"` can point to the same object without risking one mutating the other. This saves significant memory in applications with many repeated strings. Second, thread safety: immutable objects are inherently thread-safe — no synchronization needed to share a String between threads. Third, security: if String were mutable, you could validate a filename, pass it to the file system API, and then mutate it before the API uses it — a security hole. Fourth, HashMap key correctness: if a String key in a HashMap could change after insertion, the hash would no longer match the bucket, corrupting the map. Immutability guarantees that string keys are stable.

**Q3: "What is the difference between String, StringBuilder, and StringBuffer?"**

**SDE-2 Answer:** `String` is immutable — every operation that appears to modify a String (concatenation, toUpperCase, replace) actually creates a new String object. This is memory-efficient for small, fixed strings but O(n²) for repeated concatenation in a loop. `StringBuilder` is a mutable character buffer — `append()` modifies the same underlying `char[]`. It doubles its capacity when full, giving amortized O(1) appends. Use StringBuilder whenever building a String through repeated appends, especially in loops. `StringBuffer` is identical to StringBuilder but every method is `synchronized`, making it thread-safe. However, `synchronized` overhead makes it slower than StringBuilder, and thread-safe String building is almost never actually needed (you'd instead use a dedicated per-thread StringBuilder). Use StringBuilder in virtually all cases; String for fixed values; StringBuffer almost never (it's a Java 1.0 relic).

# CHAPTER 4: Object-Oriented Programming

## 4.1 Why OOP Exists: The Procedural Code Problem

Before OOP, programs were written procedurally — a sequence of functions operating on loose data. Consider a banking system as a procedural program:

```java
// PROCEDURAL style (Java can do this, but it's a bad pattern)
double balance = 1000.0;
String ownerName = "Surya";
boolean isActive = true;

void deposit(double amount) {
    // What account are we depositing into? 'balance' is a global variable?
    balance += amount;
}

void withdraw(double amount) {
    // What if balance is negative? Who enforces the rule?
    balance -= amount;
}

void transfer(double fromBalance, double toBalance, double amount) {
    fromBalance -= amount;  // This modifies a LOCAL COPY, not the actual variable
    toBalance += amount;    // Nothing about this is safe or enforced
}
```

The problems at scale:
1. **No data encapsulation:** Any code can modify `balance` directly — no validation.
2. **No organization:** A 100,000-line codebase of functions is unnavigable.
3. **State is scattered:** The properties of a "bank account" (`balance`, `owner`, `active`) exist as unrelated variables with no enforced relationship.
4. **No reuse with variation:** What if you have a `SavingsAccount` that earns interest and a `CheckingAccount` that doesn't? You'd copy-paste functions and modify them.

OOP solves this by **bundling data (fields) and behavior (methods) that operate on that data into a single unit called a class**.

---

## 4.2 Classes: Blueprint vs Object

A **class** is a blueprint. An **object** (instance) is a specific thing built from that blueprint.

```
Class (Blueprint)                     Objects (Instances)
────────────────────                  ────────────────────────────────────────
BankAccount                           account1 = new BankAccount("Surya", 1000)
  - owner: String                     account2 = new BankAccount("Ravi", 500)
  - balance: double                   
  - isActive: boolean                 account1:               account2:
  + deposit(amount)                   ┌──────────────────┐    ┌──────────────────┐
  + withdraw(amount)                  │ owner: "Surya"   │    │ owner: "Ravi"    │
  + getBalance()                      │ balance: 1000.0  │    │ balance: 500.0   │
                                      │ isActive: true   │    │ isActive: true   │
                                      └──────────────────┘    └──────────────────┘
                                      These are SEPARATE objects on the HEAP
                                      Modifying account1 doesn't affect account2
```

```java
public class BankAccount {
    // FIELDS — instance variables, one copy per object, stored on Heap
    private String owner;
    private double balance;
    private boolean isActive;
    
    // CONSTRUCTOR — special method called when 'new BankAccount(...)' is executed
    // Name MUST match class name exactly. No return type (not even void).
    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;           // 'this.owner' = instance field
        this.balance = initialBalance; // 'owner' alone would be the parameter
        this.isActive = true;
    }
    
    // METHODS — behavior that operates on this object's data
    public void deposit(double amount) {
        balance += amount;  // modifies THIS object's balance
    }
    
    public double getBalance() {
        return balance;
    }
    
    public static void main(String[] args) {
        // 'new' allocates memory on Heap, calls constructor, returns reference
        BankAccount account1 = new BankAccount("Surya", 1000.0);
        BankAccount account2 = new BankAccount("Ravi", 500.0);
        
        account1.deposit(200.0);
        
        System.out.println(account1.getBalance()); // 1200.0
        System.out.println(account2.getBalance()); // 500.0 — unchanged
    }
}
```

---

## 4.3 The `this` Keyword

`this` is a reference to the **current object** — the specific instance that a method is being called on.

```java
public class Counter {
    private int count;
    
    // Without 'this' — parameter name shadows field name
    public void setCount(int count) {
        // count = count;          // WRONG: assigns parameter to itself, field unchanged
        this.count = count;        // CORRECT: 'this.count' = field, 'count' = parameter
    }
    
    // Using 'this' to chain constructors
    public Counter() {
        this(0);  // calls Counter(int) constructor — must be first statement
    }
    
    public Counter(int initialCount) {
        this.count = initialCount;
    }
    
    // Returning 'this' enables fluent/builder-style chaining
    public Counter increment() {
        this.count++;
        return this;  // returns the current object
    }
    
    public Counter add(int n) {
        this.count += n;
        return this;
    }
    
    public int getCount() { return count; }
    
    public static void main(String[] args) {
        Counter c = new Counter();
        int result = c.increment().increment().add(5).increment().getCount();
        System.out.println(result); // 8
    }
}
```

---

## 4.4 Access Modifiers: The Four Levels of Visibility

```
Access Modifier   Same Class   Same Package   Subclass   Any Class
────────────────  ──────────   ─────────────  ─────────  ─────────
private              YES           NO            NO         NO
(package-private)    YES           YES           NO         NO
protected            YES           YES           YES        NO
public               YES           YES           YES        YES
```

```java
package com.bank.accounts;

public class BankAccount {
    private double balance;         // PRIVATE: only this class can access
    String accountType;             // PACKAGE-PRIVATE (no modifier): any class in same package
    protected String owner;         // PROTECTED: this package + subclasses
    public String accountNumber;    // PUBLIC: anywhere
    
    private void validateAmount(double amount) {
        // private helper — implementation detail, never expose
        if (amount <= 0) throw new IllegalArgumentException("Amount must be positive");
    }
    
    public void deposit(double amount) {
        validateAmount(amount);      // can call private method from same class
        balance += amount;           // can access private field from same class
    }
}

// In another class, same package (com.bank.accounts):
class AccountManager {
    void manage(BankAccount account) {
        account.owner = "New Owner"; // OK — protected accessible in same package
        account.accountType = "Savings"; // OK — package-private
        // account.balance = 100;   // COMPILE ERROR — private
    }
}

// In another package:
package com.bank.services;
class PaymentService {
    void pay(BankAccount account) {
        account.deposit(100);        // OK — public method
        // account.owner = ...;     // COMPILE ERROR — protected (not a subclass)
        // account.accountType ...  // COMPILE ERROR — package-private
    }
}
```

**Rule of thumb:** Default to `private`. Make public only what external code genuinely needs. Start restrictive — you can always loosen access later; tightening it breaks existing callers.

---

## 4.5 Static vs Instance Members

```java
public class Company {
    // INSTANCE field: each Company object has its OWN copy
    private String name;
    private int employeeCount;
    
    // STATIC field: ONE shared copy, belongs to the CLASS, not any instance
    private static int totalCompaniesCreated = 0;
    private static final String INDUSTRY = "Technology"; // constant
    
    public Company(String name) {
        this.name = name;
        this.employeeCount = 0;
        totalCompaniesCreated++;  // shared counter incremented for every new Company
    }
    
    // INSTANCE method: operates on a specific object's data (can access instance + static)
    public void hire(int count) {
        this.employeeCount += count;  // modifies THIS company's count
    }
    
    // STATIC method: belongs to class, not an instance
    // Can ONLY access static fields/methods directly (no 'this')
    public static int getTotalCompanies() {
        return totalCompaniesCreated;  // accessing static field — OK
        // return this.employeeCount;  // COMPILE ERROR: no 'this' in static method
    }
    
    // Static factory method pattern (common in Java APIs)
    public static Company createStartup(String name) {
        Company c = new Company(name);
        c.hire(5);   // startups begin with 5 employees
        return c;
    }
    
    public static void main(String[] args) {
        Company google = new Company("Google");
        Company apple = new Company("Apple");
        
        google.hire(1000);
        apple.hire(500);
        
        System.out.println(google.employeeCount);   // 1000
        System.out.println(apple.employeeCount);    // 500
        
        // Static: call on CLASS, not instance
        System.out.println(Company.getTotalCompanies()); // 2
        // google.getTotalCompanies();  // Works but misleading — IntelliJ warns you
        
        Company startup = Company.createStartup("FutureTech");
        System.out.println(Company.getTotalCompanies()); // 3
    }
}
```

**Memory layout:**
```
Class Data (Metaspace):                  Heap:
totalCompaniesCreated: 3                 google object:     apple object:
INDUSTRY: "Technology"                     name: "Google"     name: "Apple"
                                           employeeCount:1000  employeeCount:500
```

---

## 4.6 The Four Pillars of OOP (Built on BankAccount)

### PILLAR 1: ENCAPSULATION

Encapsulation = **private data + controlled access through methods**. The methods act as a contract: they can validate, log, and transform before modifying state.

```java
public class BankAccount {
    private final String accountNumber;  // final: set once, never changed
    private final String owner;
    private double balance;
    private boolean isActive;
    private final List<String> transactionHistory;
    
    public BankAccount(String owner, double initialBalance) {
        if (owner == null || owner.isBlank()) {
            throw new IllegalArgumentException("Owner cannot be blank");
        }
        if (initialBalance < 0) {
            throw new IllegalArgumentException("Initial balance cannot be negative");
        }
        this.accountNumber = generateAccountNumber();
        this.owner = owner;
        this.balance = initialBalance;
        this.isActive = true;
        this.transactionHistory = new ArrayList<>();
        transactionHistory.add("Account opened with balance: " + initialBalance);
    }
    
    // VALIDATED write access — caller cannot bypass validation by setting balance directly
    public void deposit(double amount) {
        if (!isActive) throw new IllegalStateException("Account is closed");
        if (amount <= 0) throw new IllegalArgumentException("Deposit amount must be positive");
        
        balance += amount;
        transactionHistory.add("DEPOSIT: +" + amount + " | Balance: " + balance);
    }
    
    public void withdraw(double amount) {
        if (!isActive) throw new IllegalStateException("Account is closed");
        if (amount <= 0) throw new IllegalArgumentException("Withdrawal amount must be positive");
        if (amount > balance) throw new IllegalStateException("Insufficient funds");
        
        balance -= amount;
        transactionHistory.add("WITHDRAWAL: -" + amount + " | Balance: " + balance);
    }
    
    // READ-ONLY access to balance — cannot set balance directly from outside
    public double getBalance() { return balance; }
    public String getOwner() { return owner; }
    public String getAccountNumber() { return accountNumber; }
    
    // Return defensive copy — caller can't modify the original list
    public List<String> getTransactionHistory() {
        return Collections.unmodifiableList(transactionHistory);
    }
    
    public void close() {
        this.isActive = false;
        transactionHistory.add("Account closed");
    }
    
    private String generateAccountNumber() {
        return "ACC-" + System.nanoTime();  // private implementation detail
    }
}
```

Without encapsulation: `account.balance = -1000000` is perfectly legal. With encapsulation, this is impossible — `balance` is private. The only way to modify it is through `deposit()` and `withdraw()`, which enforce invariants.

---

### PILLAR 2: INHERITANCE

Inheritance lets a class **inherit fields and methods from a parent class** and add or override behavior. Use it to model "is-a" relationships.

```java
// BASE CLASS (Superclass)
public class Animal {
    protected String name;
    protected int age;
    
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // Method to be overridden
    public String makeSound() {
        return "...";  // generic animal sound
    }
    
    // Common method: all animals have this behavior
    public String describe() {
        return name + " (age " + age + ") says: " + makeSound();
    }
    
    @Override
    public String toString() {
        return "Animal[name=" + name + ", age=" + age + "]";
    }
}

// SUBCLASS: inherits everything from Animal
public class Dog extends Animal {
    private String breed;
    
    // Constructor MUST call super() — parent's constructor — as first statement
    public Dog(String name, int age, String breed) {
        super(name, age);         // calls Animal(String, int) constructor
        this.breed = breed;
    }
    
    // @Override annotation: signals intent to override, causes compile error if typo
    // Without @Override, a typo in method name silently creates a NEW method, not an override
    @Override
    public String makeSound() {
        return "Woof!";
    }
    
    // Subclass-specific method — only Dogs have this
    public void fetch(String item) {
        System.out.println(name + " fetches the " + item + "!");
    }
    
    @Override
    public String toString() {
        return "Dog[name=" + name + ", breed=" + breed + "]";
    }
}

// SUBCLASS of Dog — deeper hierarchy
public class GoldenRetriever extends Dog {
    
    public GoldenRetriever(String name, int age) {
        super(name, age, "Golden Retriever"); // calls Dog(String, int, String)
    }
    
    @Override
    public String makeSound() {
        return "Woof woof woof!";  // Golden Retrievers are especially enthusiastic
    }
    
    public void swim() {
        System.out.println(name + " is swimming happily!");
    }
}

// What is inherited, what is not:
// - Fields (name, age, breed): YES — all visible fields are inherited
// - Methods: YES — all non-private methods inherited, can override
// - Constructors: NO — constructors are NOT inherited
//   (GoldenRetriever can't use Dog's constructor directly, must define its own)
// - Private members: technically "inherited" but not accessible without getters

public class InheritanceDemo {
    public static void main(String[] args) {
        Animal generic = new Animal("Creature", 5);
        Dog dog = new Dog("Rex", 3, "Labrador");
        GoldenRetriever golden = new GoldenRetriever("Buddy", 2);
        
        System.out.println(generic.describe());   // Creature (age 5) says: ...
        System.out.println(dog.describe());       // Rex (age 3) says: Woof!
        System.out.println(golden.describe());    // Buddy (age 2) says: Woof woof woof!
        
        dog.fetch("ball");       // Dog-specific method
        golden.fetch("stick");   // Inherited from Dog
        golden.swim();           // GoldenRetriever-specific
        
        // Superclass reference can hold subclass object (upcasting)
        Animal a = new GoldenRetriever("Max", 4);
        System.out.println(a.describe());  // uses GoldenRetriever.makeSound() — runtime dispatch
        // a.swim();  // COMPILE ERROR — Animal reference doesn't know about swim()
    }
}
```

**What's NOT inherited:**
- Constructors (each class must define its own)
- Private fields and methods (technically "inherited" but inaccessible without accessors)
- Static members (belong to the class, not the instance — not subject to inheritance rules in the same way)

---

### PILLAR 3: POLYMORPHISM

Polymorphism = "many forms." The same method call behaves differently depending on the actual type of the object at runtime.

#### Compile-Time Polymorphism: Method Overloading

The compiler resolves which method to call based on the **declared types** of the arguments:

```java
public class Calculator {
    // Three methods with the same name but different parameters
    public int add(int a, int b) { return a + b; }
    public double add(double a, double b) { return a + b; }
    public String add(String a, String b) { return a + b; }
    
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        // Compiler looks at argument TYPES and picks the right method
        System.out.println(calc.add(3, 4));           // int version: 7
        System.out.println(calc.add(3.0, 4.0));       // double version: 7.0
        System.out.println(calc.add("Hello", " World")); // String version: Hello World
    }
}
```

#### Runtime Polymorphism: Method Overriding

The JVM decides which method to call at **runtime**, based on the actual type of the object (not the declared type of the variable):

```java
public class PolymorphismDemo {
    
    abstract static class Shape {
        abstract double area();     // subclasses MUST implement this
        
        void printArea() {          // defined here, uses runtime dispatch
            System.out.printf("Area of %s = %.2f%n", 
                               getClass().getSimpleName(), area());
        }
    }
    
    static class Circle extends Shape {
        double radius;
        Circle(double r) { this.radius = r; }
        
        @Override
        double area() { return Math.PI * radius * radius; }
    }
    
    static class Rectangle extends Shape {
        double width, height;
        Rectangle(double w, double h) { this.width = w; this.height = h; }
        
        @Override
        double area() { return width * height; }
    }
    
    static class Triangle extends Shape {
        double base, height;
        Triangle(double b, double h) { this.base = b; this.height = h; }
        
        @Override
        double area() { return 0.5 * base * height; }
    }
    
    public static void main(String[] args) {
        // Parent reference holds child objects — this is the KEY to polymorphism
        Shape[] shapes = {
            new Circle(5),
            new Rectangle(4, 6),
            new Triangle(3, 8)
        };
        
        // printArea() calls area() — but WHICH area()? Determined at runtime!
        for (Shape s : shapes) {
            s.printArea(); 
        }
        // Output:
        // Area of Circle = 78.54
        // Area of Rectangle = 24.00
        // Area of Triangle = 12.00
        
        // The power: adding a Pentagon class doesn't change this loop at all
        // Polymorphism lets you write code that works with types not yet created
    }
}
```

**How the JVM resolves method calls at runtime (Virtual Method Table):**

```
Every class has a vtable (virtual method table) in Metaspace:

Shape vtable:       Circle vtable:         Rectangle vtable:
area → Shape.area   area → Circle.area     area → Rectangle.area
printArea → Shape.printArea  (inherited)    printArea → Shape.printArea (inherited)

When JVM executes: s.area()
1. Look at s's actual object type → "I'm a Circle"
2. Look up Circle's vtable → area points to Circle.area
3. Call Circle.area()

This is NOT decided at compile time. It's a vtable lookup at runtime.
That's why it's called "late binding" or "dynamic dispatch."
```

#### The `instanceof` Operator and Pattern Matching (Java 16+)

```java
// Old style (pre-Java 16):
if (shape instanceof Circle) {
    Circle c = (Circle) shape;  // explicit cast
    System.out.println("Radius: " + c.radius);
}

// Java 16+ Pattern Matching for instanceof — cast in one step
if (shape instanceof Circle c) {    // binds 'c' if shape is a Circle
    System.out.println("Radius: " + c.radius);
}

// Java 21 Pattern Matching in switch:
String result = switch (shape) {
    case Circle c    -> "Circle with radius " + c.radius;
    case Rectangle r -> "Rectangle " + r.width + "x" + r.height;
    case Triangle t  -> "Triangle with base " + t.base;
    default          -> "Unknown shape";
};
```

---

```
┌──────────────────────────────────────────────────────────────────┐
│  JAVASCRIPT VS JAVA: Object-Oriented Programming                   │
│                                                                    │
│  JavaScript uses PROTOTYPE-BASED OOP:                             │
│  class Animal {}  // syntactic sugar — still prototype chains     │
│  Animal.prototype.speak = function() {};  // actual mechanism     │
│  typeof Animal === 'function'  // a class is just a function      │
│                                                                    │
│  Java uses TRUE CLASS-BASED OOP:                                   │
│  • Access modifiers enforced at compile time (not just convention) │
│  • Interfaces are first-class contracts (JS has TypeScript types) │
│  • Abstract classes exist natively (JS uses convention/comments)  │
│  • Generics are real type parameters, erased at runtime           │
│  • Runtime polymorphism via vtable (JVM resolves at call site)    │
│                                                                    │
│  The JS class keyword is a LIE in a useful way:                   │
│  class Dog extends Animal {}  // looks like Java, but under the   │
│  hood it's just prototype chain manipulation.                      │
│                                                                    │
│  Java's private is genuinely private. JavaScript's #privateField  │
│  (ES2022) is the first real privacy — before that, it was         │
│  convention only (_name) and accessible from outside.             │
└──────────────────────────────────────────────────────────────────┘
```

### PILLAR 4: ABSTRACTION

Abstraction = **hiding implementation details, exposing only a clean interface**.

#### Abstract Classes

```java
// Cannot instantiate AbstractPaymentProcessor directly
// It provides a template with some methods implemented, others deferred to subclasses
public abstract class AbstractPaymentProcessor {
    
    // ABSTRACT method: declared but not implemented — subclasses MUST implement
    protected abstract boolean validatePayment(double amount);
    protected abstract String processTransaction(String cardNumber, double amount);
    
    // CONCRETE method: implemented in abstract class, available to all subclasses
    public final String charge(String cardNumber, double amount) {
        // Template Method Pattern: skeleton of algorithm here, subclasses fill in details
        if (!validatePayment(amount)) {
            throw new IllegalArgumentException("Payment validation failed for amount: " + amount);
        }
        
        String result = processTransaction(cardNumber, amount);
        logTransaction(cardNumber, amount, result);
        return result;
    }
    
    private void logTransaction(String cardNumber, double amount, String result) {
        String maskedCard = "****" + cardNumber.substring(cardNumber.length() - 4);
        System.out.printf("Transaction: %s | $%.2f | Result: %s%n", maskedCard, amount, result);
    }
    
    // 'final' prevents subclasses from overriding this — it's fixed behavior
    public final String getProcessorType() {
        return this.getClass().getSimpleName();
    }
}

public class StripePaymentProcessor extends AbstractPaymentProcessor {
    private static final double MAX_SINGLE_CHARGE = 50_000.0;
    
    @Override
    protected boolean validatePayment(double amount) {
        return amount > 0 && amount <= MAX_SINGLE_CHARGE;
    }
    
    @Override
    protected String processTransaction(String cardNumber, double amount) {
        // Stripe-specific API call simulation
        return "STRIPE_TXN_" + System.nanoTime();
    }
}

public class PayPalPaymentProcessor extends AbstractPaymentProcessor {
    
    @Override
    protected boolean validatePayment(double amount) {
        return amount > 0 && amount <= 10_000.0; // PayPal has lower limit
    }
    
    @Override
    protected String processTransaction(String cardNumber, double amount) {
        // PayPal-specific API call simulation
        return "PP_PAY_" + System.nanoTime();
    }
}
```

#### Interfaces

An interface is a **pure contract** — it specifies what methods a class must have, but (traditionally) not how they work. Since Java 8, interfaces can also have `default` and `static` methods with implementations.

```java
// Interface: pure contract
public interface Drawable {
    // All interface methods are implicitly public abstract (unless default/static)
    void draw();
    void resize(double factor);
    
    // Default method (Java 8+): provides a default implementation
    // Implementing classes get this for free, but can override it
    default void drawWithBorder() {
        System.out.println("Drawing border...");
        draw();    // calls the implementing class's draw()
        System.out.println("Border complete.");
    }
    
    // Static method (Java 8+): called on interface itself
    static Drawable createDefault() {
        return new Rectangle(1, 1); // factory method
    }
}

public interface Serializable {
    String serialize();
    static <T> T deserialize(String data, Class<T> type) {
        // Static factory in interface
        throw new UnsupportedOperationException("Use specific deserializer");
    }
}

// A class CAN implement multiple interfaces (unlike inheritance — single superclass only)
public class Circle implements Drawable, Serializable {
    private double radius;
    
    public Circle(double radius) { this.radius = radius; }
    
    @Override
    public void draw() {
        System.out.println("Drawing circle with radius " + radius);
    }
    
    @Override
    public void resize(double factor) {
        radius *= factor;
    }
    
    @Override
    public String serialize() {
        return "{\"type\":\"circle\",\"radius\":" + radius + "}";
    }
    // drawWithBorder() is inherited from Drawable — no need to override
}
```

#### Abstract Class vs Interface: The Decision Guide

```
                  Abstract Class          Interface
────────────────────────────────────────────────────────────────────
Can instantiate?   NO                      NO
Multiple inherit?  NO (single extends)     YES (multiple implements)
State (fields)?    YES (instance fields)   NO (only static final constants)
Constructor?       YES                     NO
Method impl?       YES (any method)        YES (only default/static)
Access modifiers?  Any                     Public only (methods)

Use Abstract Class when:
  ✓ "is-a" relationship: SavingsAccount IS-A BankAccount
  ✓ Sharing state (fields) between related classes
  ✓ Providing partial implementation (template methods)
  ✓ Internal framework extension points

Use Interface when:
  ✓ "can-do" relationship: Order IS Serializable, IS Printable
  ✓ Defining a contract multiple unrelated classes should fulfill
  ✓ A class needs to satisfy multiple contracts simultaneously
  ✓ Defining a type for polymorphism without implementation coupling
  
Rule of thumb: Start with interface. Only use abstract class if you need
to share state (fields) or you have a true is-a hierarchy.
```

---

## 4.7 Records (Java 16+): Replacing Boilerplate DTOs

Before records, a simple data carrier class required enormous boilerplate:

```java
// OLD WAY — Data Transfer Object (DTO) — 40+ lines of boilerplate
public final class UserDTO {
    private final Long id;
    private final String name;
    private final String email;
    
    public UserDTO(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof UserDTO)) return false;
        UserDTO that = (UserDTO) o;
        return Objects.equals(id, that.id) && Objects.equals(name, that.name) && Objects.equals(email, that.email);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id, name, email);
    }
    
    @Override
    public String toString() {
        return "UserDTO{id=" + id + ", name='" + name + "', email='" + email + "'}";
    }
}
```

```java
// NEW WAY with Records — same semantics, 1 line
public record UserDTO(Long id, String name, String email) {}
// Java auto-generates:
//   - final fields
//   - canonical constructor (all fields as parameters)
//   - accessors: id(), name(), email() (NOTE: no "get" prefix in records)
//   - equals() based on all fields
//   - hashCode() based on all fields
//   - toString() with all fields

UserDTO user = new UserDTO(1L, "Surya", "surya@example.com");
System.out.println(user.name());   // "Surya" (accessor, not getName())
System.out.println(user.email());  // "surya@example.com"
System.out.println(user);         // UserDTO[id=1, name=Surya, email=surya@example.com]

UserDTO user2 = new UserDTO(1L, "Surya", "surya@example.com");
System.out.println(user.equals(user2)); // true — value-based equality

// Records can have custom constructors (compact constructor for validation):
public record OrderDTO(Long id, BigDecimal amount, String status) {
    // Compact constructor: no parameter list, automatically assigns fields after body
    public OrderDTO {
        Objects.requireNonNull(id, "id cannot be null");
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        status = status.toUpperCase(); // can normalize in compact constructor
    }
    
    // Custom methods are allowed
    public boolean isPending() {
        return "PENDING".equals(status);
    }
}
```

**Records are immutable** — you can't change their fields after construction. They're ideal for DTOs, response objects, value objects, and configuration data.

---

## 4.8 Sealed Classes (Java 17+)

Sealed classes let you define a **closed set of subclasses** — the compiler knows all possible subtypes, enabling exhaustive pattern matching:

```java
// Shape can ONLY be extended by Circle, Rectangle, or Triangle
// The 'permits' clause lists all allowed subclasses
public sealed interface Shape permits Circle, Rectangle, Triangle {}

public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}
public record Triangle(double base, double height) implements Shape {}

// The power: exhaustive switch — compiler verifies all cases are covered
public class ShapeCalculator {
    public static double area(Shape shape) {
        return switch (shape) {
            case Circle c    -> Math.PI * c.radius() * c.radius();
            case Rectangle r -> r.width() * r.height();
            case Triangle t  -> 0.5 * t.base() * t.height();
            // No 'default' needed! Compiler knows these are ALL the cases.
            // If you add 'Pentagon' to permits but forget a case here → COMPILE ERROR
        };
    }
}
```

---

## 4.9 Enums: Beyond Simple Constants

```java
// Basic enum — commonly misused as just a set of string constants
public enum Direction {
    NORTH, SOUTH, EAST, WEST
}

// FULL POWER: enums can have fields, constructors, methods
public enum Planet {
    MERCURY(3.303e+23, 2.4397e6),
    VENUS  (4.869e+24, 6.0518e6),
    EARTH  (5.976e+24, 6.37814e6),
    MARS   (6.421e+23, 3.3972e6);
    
    private final double mass;   // in kilograms
    private final double radius; // in meters
    
    // Enum constructors are always private
    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }
    
    static final double G = 6.67300E-11; // gravitational constant
    
    public double surfaceGravity() {
        return G * mass / (radius * radius);
    }
    
    public double surfaceWeight(double otherMass) {
        return otherMass * surfaceGravity();
    }
}

public class EnumDemo {
    public static void main(String[] args) {
        double earthWeight = 75.0;  // kg
        double mass = earthWeight / Planet.EARTH.surfaceGravity();
        
        for (Planet p : Planet.values()) {
            System.out.printf("Weight on %s: %.2f%n", p, p.surfaceWeight(mass));
        }
        
        // Enum in switch — exhaustive by default
        Direction d = Direction.NORTH;
        String description = switch (d) {
            case NORTH -> "Heading north";
            case SOUTH -> "Heading south";
            case EAST  -> "Heading east";
            case WEST  -> "Heading west";
        };
        
        // Useful enum methods
        Direction fromString = Direction.valueOf("NORTH"); // "NORTH" → Direction.NORTH
        Direction[] all = Direction.values();              // all enum constants
        int ordinal = Direction.NORTH.ordinal();           // 0 (position in declaration)
        String name = Direction.SOUTH.name();              // "SOUTH"
    }
}

// Abstract method per constant — each constant has its own behavior
public enum Operation {
    PLUS("+")  { @Override public int apply(int x, int y) { return x + y; } },
    MINUS("-") { @Override public int apply(int x, int y) { return x - y; } },
    TIMES("*") { @Override public int apply(int x, int y) { return x * y; } },
    DIVIDE("/") { @Override public int apply(int x, int y) { return x / y; } };
    
    private final String symbol;
    Operation(String symbol) { this.symbol = symbol; }
    
    // Abstract method — every constant must implement this
    public abstract int apply(int x, int y);
    
    @Override
    public String toString() { return symbol; }
}
```

---

## 4.10 Inner Classes

```java
public class OuterClass {
    private int outerField = 10;
    
    // STATIC NESTED CLASS: belongs to the outer class but doesn't hold a reference to it
    // Can access outer class static members only
    // Use: logically grouping a helper class that doesn't need outer state
    public static class StaticNested {
        public void display() {
            System.out.println("Static nested class");
            // System.out.println(outerField); // COMPILE ERROR — no outer instance
        }
    }
    
    // INNER CLASS (non-static): every instance holds an implicit reference to outer instance
    // Can access ALL outer class members including private
    // Use: Iterator, Builder — things tightly coupled to the outer class
    public class Inner {
        public void display() {
            System.out.println("Inner class, outer field: " + outerField); // can access!
        }
    }
    
    public void demonstrateAnonymous() {
        // ANONYMOUS CLASS: inline implementation of an interface/abstract class
        // No name, defined and instantiated at the same time
        // Pre-lambda Java pattern (now usually replaced by lambdas)
        Runnable r = new Runnable() {
            @Override
            public void run() {
                System.out.println("Anonymous Runnable running");
                System.out.println("Can access outer: " + outerField); // can access outer
            }
        };
        r.run();
        
        // Modern equivalent with lambda:
        Runnable modern = () -> System.out.println("Lambda Runnable");
        modern.run();
    }
}

// Usage:
OuterClass outer = new OuterClass();

// Static nested: instantiated without outer instance
OuterClass.StaticNested nested = new OuterClass.StaticNested();

// Inner: requires outer instance
OuterClass.Inner inner = outer.new Inner();
inner.display(); // "Inner class, outer field: 10"
```

---

## 4.11 SOLID Principles

### S — Single Responsibility Principle

A class should have **one reason to change** — one job.

```java
// VIOLATION: OrderService does too many unrelated things
class OrderService_Bad {
    public void processOrder(Order order) {
        // Responsibility 1: business logic
        validateOrder(order);
        calculateTotal(order);
        
        // Responsibility 2: persistence (should be OrderRepository)
        String sql = "INSERT INTO orders VALUES (...)";
        jdbcTemplate.update(sql, order);
        
        // Responsibility 3: notifications (should be NotificationService)
        emailClient.send(order.getCustomerEmail(), "Order confirmed");
        smsClient.send(order.getPhoneNumber(), "Your order is ready");
        
        // Responsibility 4: PDF generation (should be InvoiceService)
        PdfDocument pdf = pdfGenerator.createInvoice(order);
        fileStorage.save(pdf);
    }
}
// If email API changes, if PDF library upgrades, if DB schema changes — 
// ALL require modifying OrderService. One class, four reasons to change.

// FIX: Each class has ONE job
class OrderService_Good {
    private final OrderRepository repository;
    private final NotificationService notifier;
    private final InvoiceService invoiceService;
    
    public void processOrder(Order order) {
        validateOrder(order);
        calculateTotal(order);
        repository.save(order);       // delegate to specialist
        notifier.notifyCustomer(order);
        invoiceService.generate(order);
    }
}
```

### O — Open/Closed Principle

Classes should be **open for extension, closed for modification**. Add behavior by creating new classes, not modifying existing ones.

```java
// VIOLATION: Adding a new payment type requires modifying PaymentProcessor
class PaymentProcessor_Bad {
    public void process(Payment payment) {
        if (payment.getType().equals("CREDIT_CARD")) {
            // credit card logic...
        } else if (payment.getType().equals("PAYPAL")) {
            // paypal logic...
        } else if (payment.getType().equals("CRYPTO")) {  // ← had to modify this class
            // crypto logic...
        }
        // Every new payment type = another modification here
    }
}

// FIX: Define an abstraction; each payment type is a new class
interface PaymentStrategy {
    void process(Payment payment);
}

class CreditCardPayment implements PaymentStrategy {
    @Override
    public void process(Payment payment) { /* credit card logic */ }
}

class PayPalPayment implements PaymentStrategy {
    @Override
    public void process(Payment payment) { /* paypal logic */ }
}

// Adding Crypto: create a NEW class, don't touch existing ones
class CryptoPayment implements PaymentStrategy {
    @Override
    public void process(Payment payment) { /* crypto logic */ }
}

class PaymentProcessor_Good {
    // Closed for modification — this class never changes
    public void process(Payment payment, PaymentStrategy strategy) {
        strategy.process(payment);
    }
}
```

### L — Liskov Substitution Principle

**Subclasses must be substitutable for their superclass without breaking the program.** A subclass should honor all the contracts (preconditions, postconditions, invariants) of its superclass.

```java
// VIOLATION: Square extends Rectangle — mathematically a square IS a rectangle,
// but as objects, Square BREAKS Rectangle's contract
class Rectangle {
    protected int width;
    protected int height;
    
    public void setWidth(int w) { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int getArea() { return width * height; }
}

class Square extends Rectangle {
    // Square's invariant: width == height always
    @Override
    public void setWidth(int w) {
        this.width = w;
        this.height = w;  // must keep equal
    }
    
    @Override
    public void setHeight(int h) {
        this.width = h;   // must keep equal
        this.height = h;
    }
}

// This method works for Rectangle but BREAKS with Square — LSP violation!
void testRectangle(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    // Expected: 5 * 10 = 50
    assert r.getArea() == 50; // FAILS for Square! Square.setHeight(10) also set width to 10 → area = 100
}

// FIX: Don't make Square extend Rectangle — they're not substitutable
// Instead, use an interface that both can implement:
interface Shape { int getArea(); }
class Rectangle implements Shape { ... }
class Square implements Shape { ... }
// They're separate things; no inheritance between them
```

### I — Interface Segregation Principle

**Clients should not be forced to depend on interfaces they don't use.** Fat interfaces break cohesion.

```java
// VIOLATION: Fat Animal interface forces all animals to implement all methods
interface Animal_Fat {
    void breathe();
    void eat();
    void fly();     // What about dogs? They can't fly!
    void swim();    // What about eagles? They don't swim!
    void run();
    void makeSound();
}

// Dog has to implement fly() even though it can't fly
class Dog implements Animal_Fat {
    public void breathe() { ... }
    public void eat() { ... }
    public void fly() {
        throw new UnsupportedOperationException("Dogs can't fly"); // ← BAD
    }
    // ...
}

// FIX: Segregate into small, focused interfaces
interface Breathable { void breathe(); }
interface Eatable    { void eat(); }
interface Flyable    { void fly(); }
interface Swimmable  { void swim(); }
interface Runnable   { void run(); }

// Each class implements only what it can actually do
class Dog implements Breathable, Eatable, Runnable {
    // No swim(), no fly() — exactly the capabilities Dog has
}

class Eagle implements Breathable, Eatable, Flyable {
    // Eagles can fly, not swim (mostly)
}

class Duck implements Breathable, Eatable, Flyable, Swimmable {
    // Ducks do it all
}
```

### D — Dependency Inversion Principle

**High-level modules should not depend on low-level modules. Both should depend on abstractions.** Depend on interfaces, not concrete classes.

```java
// VIOLATION: OrderService depends directly on MySQLOrderRepository
class OrderService_Bad {
    // Hard dependency on a concrete class — cannot swap databases, cannot mock in tests
    private MySQLOrderRepository repository = new MySQLOrderRepository();
    
    public void save(Order order) {
        repository.save(order); // tied to MySQL forever
    }
}

// FIX: Depend on the abstraction (interface), inject the concrete implementation
interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(Long id);
}

// Concrete implementations
class MySQLOrderRepository implements OrderRepository {
    @Override
    public void save(Order order) { /* MySQL implementation */ }
    @Override
    public Optional<Order> findById(Long id) { /* MySQL query */ }
}

class InMemoryOrderRepository implements OrderRepository {
    private Map<Long, Order> store = new HashMap<>();
    
    @Override
    public void save(Order order) { store.put(order.getId(), order); }
    @Override
    public Optional<Order> findById(Long id) { return Optional.ofNullable(store.get(id)); }
}

class OrderService_Good {
    // Depends on ABSTRACTION, not concrete class
    private final OrderRepository repository;
    
    // Dependency is INJECTED (constructor injection — preferred)
    public OrderService_Good(OrderRepository repository) {
        this.repository = repository;
    }
    
    public void save(Order order) {
        repository.save(order);  // works with any implementation
    }
}

// In production:
OrderService_Good service = new OrderService_Good(new MySQLOrderRepository());

// In tests — use in-memory repo, no real database needed:
OrderService_Good testService = new OrderService_Good(new InMemoryOrderRepository());
```

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "What is polymorphism? How does Java resolve method calls at runtime?"**

**SDE-2 Answer:** Polymorphism means the same operation behaves differently depending on the type of object involved. Java has two kinds: compile-time polymorphism (method overloading — the compiler selects the right method based on the declared types of arguments, resolved statically) and runtime polymorphism (method overriding — when a method is called on a supertype reference holding a subtype object, the JVM uses dynamic dispatch). At runtime, the JVM resolves overridden method calls through the virtual method table (vtable). Each class has a vtable in Metaspace listing its methods with pointers to their implementations. When `animal.makeSound()` is called and `animal` holds a `Dog` object, the JVM looks up the vtable for `Dog`, finds `makeSound` points to `Dog.makeSound`, and calls it. This is sometimes called late binding — the binding of the method call to the method implementation happens at execution time, not compile time. `final` methods and `private` methods bypass vtable lookup since they can't be overridden.

**Q2: "What is the difference between an abstract class and an interface? When would you use each?"**

**SDE-2 Answer:** An abstract class can have instance fields, constructors, and methods of any access modifier. It can be partially implemented — some methods have bodies, some are abstract (forcing subclasses to implement them). A class can extend only ONE abstract class. An interface (traditionally) has only method signatures — it's a pure contract. Since Java 8, interfaces can have `default` (instance, inheritable) and `static` methods with implementations. A class can implement multiple interfaces. The decision comes down to the relationship: if it's a true "is-a" with shared state and you want to provide default behavior — use an abstract class. Example: `AbstractPaymentProcessor` with a shared `logTransaction` method and shared retry logic. If it's a "can-do" capability that unrelated classes might need — use an interface. Example: `Serializable`, `Comparable`, `Runnable` — a `String`, a `Dog`, and an `Order` might all implement `Comparable` without being related to each other. In modern Java, prefer interfaces with default methods unless you genuinely need to share state (fields) between related classes.

**Q3: "Explain the SOLID principles with an example."**

**SDE-2 Answer (abbreviated for brevity):** SOLID guides class and module design. S (Single Responsibility): a class should have one reason to change — `OrderService` should process orders, not also send emails and generate PDFs. O (Open/Closed): extend behavior by adding new classes, not modifying existing ones — add a `CryptoPaymentStrategy` without touching `PaymentProcessor`. L (Liskov Substitution): subclasses must honor the parent's contract — `Square extends Rectangle` is the classic violation because setting width independently breaks Rectangle's expected behavior. I (Interface Segregation): prefer many small focused interfaces over one fat interface — split `Animal` into `Flyable`, `Swimmable`, `Runnable` so a Dog only implements what it can do. D (Dependency Inversion): depend on abstractions, not concrete implementations — `OrderService` should take an `OrderRepository` interface in its constructor, not hardcode `new MySQLOrderRepository()`, enabling testing with in-memory implementations and production with real ones.

# CHAPTER 5: The Collections Framework

## 5.1 Why Collections Exist: The Problems with Raw Arrays

Arrays are primitive. They have a fixed size set at creation. Adding an element when full requires manually creating a larger array and copying. Removing from the middle requires shifting everything right. There's no built-in search, sort (with lambdas), filter, or transform. There's no type-safe heterogeneous grouping.

The Collections Framework solves all of this with a rich hierarchy of data structures, each optimized for specific access patterns.

---

```
┌──────────────────────────────────────────────────────────────────┐
│  JAVASCRIPT VS JAVA: Collections                                   │
│                                                                    │
│  JavaScript has just Array and Object for most use cases.         │
│  ES6 added Map and Set. That is the entire collection story.      │
│                                                                    │
│  Java has a full Collections Framework hierarchy:                  │
│  List, Set, Queue, Deque, Map — each with multiple implementations│
│  optimized for different access patterns.                          │
│                                                                    │
│  JS Map vs Java HashMap:                                           │
│  const map = new Map();        // JS: maintains insertion order    │
│  map.set('key', value);        // O(1) average                     │
│  Map<K,V> map = new HashMap<>(); // Java: no insertion order       │
│  map.put("key", value);          // O(1) average                   │
│                                                                    │
│  JS Set vs Java HashSet:                                           │
│  Both O(1) for add, contains, delete.                             │
│  Java HashSet is backed by HashMap — same internals.              │
│                                                                    │
│  The BIG difference: Java's type system means you know at compile  │
│  time what is in your collection. JS Array<any> has no type       │
│  guarantee. List<User> in Java guarantees every element is a User. │
└──────────────────────────────────────────────────────────────────┘
```

## 5.2 The Complete Hierarchy

```
java.lang.Iterable<T>
    └── java.util.Collection<T>
            ├── java.util.List<T>                    (ordered, duplicates allowed, index access)
            │       ├── ArrayList<T>                  ← dynamic array
            │       ├── LinkedList<T>                 ← doubly-linked list
            │       ├── Vector<T>                     ← legacy, synchronized ArrayList
            │       └── Stack<T>                      ← legacy, use ArrayDeque instead
            │
            ├── java.util.Set<T>                     (no duplicates, no guaranteed order)
            │       ├── HashSet<T>                    ← backed by HashMap, O(1) avg
            │       ├── LinkedHashSet<T>              ← HashSet + insertion order
            │       └── TreeSet<T>                    ← sorted set, O(log n), NavigableSet
            │
            └── java.util.Queue<T>                   (FIFO ordering, head-tail access)
                    ├── LinkedList<T>                 ← also implements Queue
                    ├── PriorityQueue<T>              ← min-heap, priority-ordered
                    └── java.util.Deque<T>            (double-ended queue)
                            ├── ArrayDeque<T>         ← correct stack AND queue
                            └── LinkedList<T>

java.util.Map<K,V>    (NOT a Collection — key→value pairs)
        ├── HashMap<K,V>                              ← hash table, O(1) avg, unordered
        ├── LinkedHashMap<K,V>                        ← HashMap + insertion/access order
        ├── TreeMap<K,V>                              ← red-black tree, sorted by key
        ├── Hashtable<K,V>                            ← legacy, synchronized HashMap
        └── java.util.concurrent.ConcurrentHashMap   ← thread-safe, Chapter 7
```

---

## 5.3 ArrayList: The Workhorse

`ArrayList` is the most commonly used collection. Understand its internals cold.

### Internal Structure

```java
// Simplified source (actual OpenJDK ArrayList):
public class ArrayList<E> extends AbstractList<E> {
    private static final int DEFAULT_CAPACITY = 10;
    
    // The actual storage: a plain Object array
    transient Object[] elementData;
    
    // Number of elements currently stored (NOT array.length)
    private int size;
    
    // Default constructor: starts with EMPTY array (not capacity 10 yet!)
    // On first add, grows to 10
    public ArrayList() {
        this.elementData = {};
    }
    
    // Pre-size constructor: avoids resizes if you know expected size
    public ArrayList(int initialCapacity) {
        this.elementData = new Object[initialCapacity];
    }
}
```

### Growth Strategy

```
Initial state:  elementData = [], size = 0

add("A"):       elementData = ["A", _, _, _, _, _, _, _, _, _], size = 1
                (first add triggers growth to capacity 10)

add("B"):       elementData = ["A","B", _, _, _, _, _, _, _, _], size = 2
...
add("J"):       elementData = ["A","B","C","D","E","F","G","H","I","J"], size = 10

add("K"):       FULL! Resize triggered:
                newCapacity = (10 + 10/2) = 15  (grows by 50%)
                1. Allocate new Object[15]
                2. System.arraycopy(old → new)  — copies all 10 elements
                3. elementData points to new array
                elementData = ["A".."J","K", _, _, _, _], size = 11
```

**Growth formula:** `newCapacity = oldCapacity + (oldCapacity >> 1)` = 1.5× growth

### Time Complexity

```
get(index):        O(1) — elementData[index] is direct array access
                   Address = base_address + index * element_size
                   Single pointer dereference: constant time

add(end):          O(1) amortized
                   - Normally: elementData[size++] = e → O(1)
                   - On resize: O(n) to copy, but this happens 1/n of the time
                   - Total cost over n inserts: O(n) total → O(1) per insert amortized

add(middle i):     O(n) — must shift elements right to make room
                   System.arraycopy(data, i, data, i+1, size-i) — shifts n-i elements

remove(index i):   O(n) — must shift elements left to fill the gap

contains(obj):     O(n) — linear scan (uses .equals())
```

### Code Example

```java
import java.util.*;

public class ArrayListDemo {
    public static void main(String[] args) {
        // Basic operations
        List<String> names = new ArrayList<>();
        names.add("Alice");
        names.add("Bob");
        names.add("Charlie");
        names.add(1, "Dave");   // insert at index 1 — O(n) shift
        
        System.out.println(names);           // [Alice, Dave, Bob, Charlie]
        System.out.println(names.get(2));    // "Bob" — O(1)
        System.out.println(names.size());    // 4
        
        names.remove(0);                     // remove by index — O(n) shift
        names.remove("Charlie");             // remove by value — O(n) scan + shift
        
        // Iteration — preferred: for-each
        for (String name : names) {
            System.out.println(name);
        }
        
        // Index-based iteration
        for (int i = 0; i < names.size(); i++) {
            System.out.println(i + ": " + names.get(i));
        }
        
        // Bulk operations
        List<String> extras = List.of("Eve", "Frank");
        names.addAll(extras);
        
        names.sort(Comparator.naturalOrder());       // ["Alice", "Dave", "Eve", "Frank"]
        names.sort(Comparator.reverseOrder());       // ["Frank", "Eve", "Dave", "Alice"]
        names.sort(Comparator.comparingInt(String::length));  // by string length
        
        Collections.sort(names);                    // also works
        Collections.shuffle(names);
        Collections.reverse(names);
        
        int index = Collections.binarySearch(names, "Alice"); // requires sorted list!
        
        // Pre-sizing for performance
        int expectedSize = 100_000;
        List<Integer> large = new ArrayList<>(expectedSize); // no resizes needed
        for (int i = 0; i < expectedSize; i++) {
            large.add(i);
        }
        
        // subList — returns a VIEW (backed by original list, not a copy)
        List<String> sub = names.subList(0, 2); // elements 0 and 1
        sub.clear(); // THIS MODIFIES the original 'names' list!
        
        // To get an independent copy:
        List<String> copy = new ArrayList<>(names.subList(0, 2));
        
        // Conversion
        String[] array = names.toArray(new String[0]);
        List<String> fromArray = Arrays.asList(array);  // FIXED SIZE — cannot add/remove
        List<String> mutableFromArray = new ArrayList<>(Arrays.asList(array)); // mutable
    }
}
```

---

## 5.4 LinkedList: When to Actually Use It (Almost Never)

### Internal Structure

```java
// Each element is a Node with references to previous and next nodes
private static class Node<E> {
    E item;
    Node<E> next;
    Node<E> prev;
}

// LinkedList holds references to first and last nodes
private Node<E> first;
private Node<E> last;
private int size;
```

```
LinkedList: A → B → C → D
(each node holds item + pointer to next + pointer to prev)

first → [prev=null][A][next=→] → [prev=←][B][next=→] → [prev=←][C][next=→] → [prev=←][D][next=null] ← last
```

### Time Complexity

```
addFirst/addLast:     O(1) — just update first/last pointers
removeFirst/removeLast: O(1) — just update first/last pointers

get(index):           O(n) — must traverse from first (or last if index > size/2)
add(middle index i):  O(n) to find position, O(1) to insert (update 4 pointers)

Memory: each node uses ~32-48 bytes (item + prev ref + next ref + object header)
vs ArrayList: ~8 bytes per element (just the reference in Object[])
```

### Cache Performance: Why LinkedList Usually Loses

```
ArrayList: [elem0][elem1][elem2][elem3]...  ← contiguous memory
           CPU prefetcher loads cache line → adjacent elements already in L1 cache
           Iterating: next element is probably already in cache

LinkedList: [nodeA at 0x1000] → [nodeB at 0xABC0] → [nodeC at 0x4500]...
            Pointer chasing: each access may miss the cache → fetch from RAM
            Iterating: each "next" may be a cache miss → 100x slower than ArrayList
```

**The honest truth about LinkedList:** In almost all practical cases, `ArrayList` beats `LinkedList` because of cache performance and lower memory overhead. `LinkedList` only wins when you have a reference to a node in the middle and need O(1) insertion/deletion there — which almost never comes up in application code. Use `ArrayDeque` as a queue and stack. Use `ArrayList` for lists.

---

## 5.5 HashMap: The Most Important Collection Internally

HashMap is the most important collection to understand deeply. It powers `HashSet`, `LinkedHashMap`, `ConcurrentHashMap`, and is central to every Java application.

### Internal Structure

```java
// Simplified internal representation
public class HashMap<K,V> {
    // The hash table — an array of "buckets"
    // Each bucket is a linked list (Java 7) or tree (Java 8+)
    transient Node<K,V>[] table;  // default length: 16 (always power of 2)
    
    int size;            // number of key-value pairs
    float loadFactor;    // default 0.75
    int threshold;       // size > threshold triggers resize (capacity * loadFactor)
    
    static class Node<K,V> {
        final int hash;  // pre-computed hash of the key
        final K key;
        V value;
        Node<K,V> next;  // linked list chaining for collision
    }
    
    // Java 8+: TreeNode (extends Node) — used when bucket has 8+ entries
    static final class TreeNode<K,V> extends LinkedHashMap.Entry<K,V> {
        TreeNode<K,V> parent, left, right, prev;
        boolean red;
        // Red-black tree node — O(log n) instead of O(n) for large buckets
    }
}
```

### How `put(key, value)` Works — Step by Step

```java
map.put("hello", 42);

Step 1: Compute hash
    int hash = key.hashCode();
    // "hello".hashCode() = 99162322 (in JDK)
    
    // Additional spread (why?): keys with same low bits but different high bits
    // would all collide in small tables. XOR with shifted hash improves distribution.
    hash = hash ^ (hash >>> 16);
    // 99162322 ^ (99162322 >>> 16) = 99162322 ^ 1513 = 99161371
    
Step 2: Find bucket index
    int capacity = table.length;  // 16 initially
    int index = hash & (capacity - 1);
    // 99161371 & 15 = 99161371 & 0b00001111
    // = 0b00000011 = 3
    // Why & (capacity-1) instead of % capacity?
    //   When capacity is power of 2, they're equivalent.
    //   But bitwise AND is a single CPU instruction; % involves division.
    
Step 3: Check bucket 3
    if (table[3] == null) {
        table[3] = new Node(hash, "hello", 42, null);
        // no collision — done
    } else {
        // Collision: traverse the list/tree at table[3]
        // Check each node: if hash matches AND key.equals(existingKey),
        // update the value. Otherwise, append new node.
    }
    
Step 4: Check if resize needed
    size++;
    if (size > threshold) {  // threshold = capacity * loadFactor = 16 * 0.75 = 12
        resize();            // double capacity, rehash everything
    }
```

### The Load Factor and Resizing

```
capacity=16, loadFactor=0.75 → threshold=12

When size reaches 12:
  resize() creates table[32]  (doubles capacity)
  For EVERY existing entry:
    recompute bucket index with new capacity (index = hash & (32-1))
    place in new table
  This is O(n) — expensive, but amortized O(1) per put

Why 0.75?
  - Too low (e.g. 0.25): resize too often, wastes memory
  - Too high (e.g. 1.0): many collisions, O(n) lookup in worst case
  - 0.75: empirically good balance between memory and performance
```

### Java 8 Treeification

```
When bucket has ≥ 8 nodes (chain too long → O(n) lookup):
  Convert linked list → Red-Black Tree → O(log n) worst case

When bucket shrinks to ≤ 6 nodes (after removes):
  Convert tree back to linked list (lower overhead for small sets)

This prevents denial-of-service attacks where an attacker crafts keys
that all hash to the same bucket, making every operation O(n).
```

### The hashCode() and equals() Contract

This is critical — violating it corrupts HashMap:

```java
// The contract (from Java documentation):
// 1. If a.equals(b) is true → a.hashCode() MUST equal b.hashCode()
// 2. If a.hashCode() != b.hashCode() → a.equals(b) MUST be false
// 3. The converse of rule 1 is NOT required:
//    a.hashCode() == b.hashCode() does NOT mean a.equals(b)
//    (this is a collision — acceptable but slow)

// VIOLATION — equals but different hashCodes:
class BadKey {
    int id;
    
    @Override
    public boolean equals(Object o) {
        return o instanceof BadKey bk && this.id == bk.id;
    }
    
    // FORGOT hashCode — uses Object.hashCode() (memory address) by default!
    // Two BadKey objects with same id will have equals()=true but different hashCodes
}

Map<BadKey, String> map = new HashMap<>();
BadKey k1 = new BadKey(1);
map.put(k1, "value");

BadKey k2 = new BadKey(1);      // same id as k1
map.get(k2);  // returns NULL!
// Why? HashMap computes k2.hashCode() → different from k1.hashCode()
// → looks in wrong bucket → "key not found" → returns null
// The entry is there, but the contract violation makes it unfindable!

// CORRECT: Always override BOTH equals AND hashCode together
@Override
public boolean equals(Object o) {
    return o instanceof BadKey bk && this.id == bk.id;
}

@Override
public int hashCode() {
    return Integer.hashCode(id);  // consistent with equals
}
```

### Build a Simplified HashMap from Scratch

```java
public class SimpleHashMap<K, V> {
    private static final int INITIAL_CAPACITY = 16;
    private static final float LOAD_FACTOR = 0.75f;
    
    private Object[][] table;  // [bucket_index][0]=key, [1]=value — simplified (no chaining)
    private int size;
    
    @SuppressWarnings("unchecked")
    public SimpleHashMap() {
        table = new Object[INITIAL_CAPACITY][];
    }
    
    private int bucketIndex(Object key) {
        int hash = key.hashCode();
        hash ^= (hash >>> 16); // spread the bits
        return Math.abs(hash) % table.length;
    }
    
    public void put(K key, V value) {
        int index = bucketIndex(key);
        table[index] = new Object[]{key, value};
        size++;
        
        if ((float) size / table.length > LOAD_FACTOR) {
            resize();
        }
    }
    
    @SuppressWarnings("unchecked")
    public V get(K key) {
        int index = bucketIndex(key);
        Object[] entry = table[index];
        if (entry != null && key.equals(entry[0])) {
            return (V) entry[1];
        }
        return null;
    }
    
    @SuppressWarnings("unchecked")
    private void resize() {
        Object[][] oldTable = table;
        table = new Object[oldTable.length * 2];
        size = 0;
        for (Object[] entry : oldTable) {
            if (entry != null) {
                put((K) entry[0], (V) entry[1]);
            }
        }
    }
    
    public int size() { return size; }
}
```

### Common HashMap Operations

```java
import java.util.*;

public class HashMapDemo {
    public static void main(String[] args) {
        Map<String, Integer> wordCount = new HashMap<>();
        
        // put: add/update
        wordCount.put("Java", 1);
        wordCount.put("is", 1);
        wordCount.put("Java", 2);  // updates existing key — returns old value (1)
        
        // get: returns null if key absent
        Integer count = wordCount.get("Java");     // 2
        Integer missing = wordCount.get("Python"); // null — not an exception
        
        // getOrDefault: avoid null checks
        int javaCount = wordCount.getOrDefault("Java", 0);    // 2
        int rubyCount = wordCount.getOrDefault("Ruby", 0);    // 0 (default)
        
        // containsKey / containsValue
        wordCount.containsKey("Java");   // true
        wordCount.containsValue(2);      // true
        
        // putIfAbsent: only puts if key not present
        wordCount.putIfAbsent("Java", 99);   // does nothing — "Java" exists
        wordCount.putIfAbsent("Kotlin", 1);  // puts — "Kotlin" not present
        
        // compute: transform existing value (or create new entry)
        // Word frequency counter pattern:
        Map<String, Integer> freq = new HashMap<>();
        String[] words = {"the", "cat", "sat", "on", "the", "mat", "the"};
        for (String w : words) {
            freq.merge(w, 1, Integer::sum);
            // if w absent: put w→1
            // if w present: apply Integer::sum(existing, 1) → existing + 1
        }
        System.out.println(freq); // {the=3, cat=1, sat=1, on=1, mat=1}
        
        // computeIfAbsent: atomic check-then-create (critical for caches)
        Map<String, List<String>> grouped = new HashMap<>();
        grouped.computeIfAbsent("fruits", k -> new ArrayList<>()).add("apple");
        grouped.computeIfAbsent("fruits", k -> new ArrayList<>()).add("banana");
        // "fruits" → ["apple", "banana"] — lambda only called on first invocation
        
        // Iteration
        for (Map.Entry<String, Integer> entry : wordCount.entrySet()) {
            System.out.printf("%s → %d%n", entry.getKey(), entry.getValue());
        }
        
        for (String key : wordCount.keySet()) { /* ... */ }
        for (int value : wordCount.values()) { /* ... */ }
        
        // forEach (Java 8+)
        wordCount.forEach((key, value) -> 
            System.out.printf("%s → %d%n", key, value));
        
        // replaceAll
        wordCount.replaceAll((key, value) -> value * 10);
        
        // null key: HashMap allows exactly one null key (goes to bucket 0)
        wordCount.put(null, 0);       // OK
        wordCount.get(null);           // returns 0
        // TreeMap and Hashtable do NOT allow null keys
    }
}
```

---

#### Mandatory Coding Exercise: Implement HashMap from First Principles

This exercise is not optional. Building a HashMap once converts the internals
from abstract knowledge to embodied understanding. After completing this,
every HashMap interview question becomes answerable from code you have written.

```java
/**
 * A simplified HashMap implementation demonstrating:
 * - Hash function with spreading (XOR trick)
 * - Bucket array with chaining for collision handling
 * - Dynamic resizing when load factor exceeded
 * - null key support
 *
 * This is NOT the production Java HashMap — it is a teaching implementation
 * that reveals every important internal mechanism.
 */
public class SimpleHashMap<K, V> {

    // ─── Inner class: one entry in a bucket chain ───────────────────────
    private static class Entry<K, V> {
        final K key;
        V value;
        Entry<K, V> next;  // next entry in the SAME bucket (collision chain)
        final int hash;    // cached hash to avoid recomputing during resize

        Entry(K key, V value, int hash) {
            this.key = key;
            this.value = value;
            this.hash = hash;
        }
    }

    // ─── Constants (same values as real Java HashMap) ───────────────────
    private static final int   DEFAULT_CAPACITY   = 16;    // must be power of 2
    private static final float DEFAULT_LOAD_FACTOR = 0.75f;
    private static final int   MAXIMUM_CAPACITY   = 1 << 30;

    // ─── State ──────────────────────────────────────────────────────────
    private Entry<K, V>[] table;  // the bucket array
    private int size;             // number of key-value pairs stored
    private int threshold;        // size threshold that triggers resize

    // ─── Constructor ────────────────────────────────────────────────────
    @SuppressWarnings("unchecked")
    public SimpleHashMap(int initialCapacity) {
        // Round up to next power of 2 (HashMap requires power-of-2 capacity
        // so that bitwise AND works as modulo: hash & (capacity-1))
        int cap = 1;
        while (cap < initialCapacity) cap <<= 1;
        this.table = new Entry[cap];
        this.threshold = (int)(cap * DEFAULT_LOAD_FACTOR);
    }

    public SimpleHashMap() {
        this(DEFAULT_CAPACITY);
    }

    // ─── Hash function ──────────────────────────────────────────────────
    /**
     * Spread the hash to reduce clustering in small arrays.
     * XOR the high 16 bits into the low 16 bits because bucket index only
     * uses low bits: hash & (capacity-1). Without spreading, keys with
     * identical low bits would always collide regardless of high bits.
     */
    private int hash(K key) {
        if (key == null) return 0;
        int h = key.hashCode();
        return h ^ (h >>> 16);  // must be >>> not >> (see Chapter 3 operators section)
    }

    // ─── Bucket index ───────────────────────────────────────────────────
    /**
     * Convert hash to bucket array index.
     * Bitwise AND with (capacity-1) is equivalent to hash % capacity
     * but only works when capacity is a power of 2.
     * Example: capacity=16, capacity-1=15 (binary: 01111)
     * Any hash ANDed with 01111 gives a result 0-15.
     */
    private int bucketIndex(int hash) {
        return hash & (table.length - 1);
    }

    // ─── put ────────────────────────────────────────────────────────────
    /**
     * Insert or update a key-value pair.
     * Returns the previous value if key existed, null otherwise.
     */
    public V put(K key, V value) {
        int hash = hash(key);
        int index = bucketIndex(hash);

        // Walk the chain in this bucket looking for an existing key
        for (Entry<K, V> e = table[index]; e != null; e = e.next) {
            if (e.hash == hash && (e.key == key || (key != null && key.equals(e.key)))) {
                V oldValue = e.value;
                e.value = value;  // update existing
                return oldValue;
            }
        }

        // Key not found — prepend new entry at the HEAD of the bucket chain
        // (prepending is O(1); appending would require walking to the tail)
        Entry<K, V> newEntry = new Entry<>(key, value, hash);
        newEntry.next = table[index];  // new entry points to old head
        table[index] = newEntry;       // new entry becomes the new head
        size++;

        // Resize if we have exceeded the load factor threshold
        if (size > threshold) resize();
        return null;
    }

    // ─── get ────────────────────────────────────────────────────────────
    public V get(K key) {
        int hash = hash(key);
        int index = bucketIndex(hash);

        for (Entry<K, V> e = table[index]; e != null; e = e.next) {
            if (e.hash == hash && (e.key == key || (key != null && key.equals(e.key)))) {
                return e.value;
            }
        }
        return null; // key not found
    }

    // ─── containsKey ────────────────────────────────────────────────────
    public boolean containsKey(K key) {
        return get(key) != null;
    }

    // ─── remove ─────────────────────────────────────────────────────────
    public V remove(K key) {
        int hash = hash(key);
        int index = bucketIndex(hash);
        Entry<K, V> prev = null;

        for (Entry<K, V> e = table[index]; e != null; prev = e, e = e.next) {
            if (e.hash == hash && (e.key == key || (key != null && key.equals(e.key)))) {
                if (prev == null) table[index] = e.next;  // removing head
                else prev.next = e.next;                  // bypass this entry
                size--;
                return e.value;
            }
        }
        return null;
    }

    // ─── resize ─────────────────────────────────────────────────────────
    /**
     * Double the capacity and rehash all entries.
     * This is why resize is O(n) — every entry must be re-placed.
     * Amortized over all puts: O(1) per put because resize happens rarely.
     */
    @SuppressWarnings("unchecked")
    private void resize() {
        int oldCapacity = table.length;
        if (oldCapacity == MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return;
        }

        int newCapacity = oldCapacity << 1;  // double the capacity
        Entry<K, V>[] newTable = new Entry[newCapacity];
        threshold = (int)(newCapacity * DEFAULT_LOAD_FACTOR);

        // Rehash: every entry gets a NEW bucket index because capacity changed
        for (Entry<K, V> head : table) {
            Entry<K, V> e = head;
            while (e != null) {
                Entry<K, V> next = e.next;
                int newIndex = e.hash & (newCapacity - 1); // new bucket index
                e.next = newTable[newIndex]; // prepend to new bucket chain
                newTable[newIndex] = e;
                e = next;
            }
        }
        table = newTable;
    }

    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }

    // ─── Test ───────────────────────────────────────────────────────────
    public static void main(String[] args) {
        SimpleHashMap<String, Integer> map = new SimpleHashMap<>();

        // Basic put and get
        map.put("Alice", 30);
        map.put("Bob", 25);
        map.put("Charlie", 35);
        System.out.println(map.get("Alice"));    // 30
        System.out.println(map.get("Bob"));      // 25
        System.out.println(map.size());          // 3

        // Update existing key
        map.put("Alice", 31);
        System.out.println(map.get("Alice"));    // 31 (updated)
        System.out.println(map.size());          // 3 (no size increase)

        // null key
        map.put(null, 99);
        System.out.println(map.get(null));       // 99

        // Remove
        map.remove("Bob");
        System.out.println(map.get("Bob"));      // null
        System.out.println(map.size());          // 3

        // Force resize by adding many entries
        SimpleHashMap<Integer, String> bigMap = new SimpleHashMap<>(4); // small initial capacity
        for (int i = 0; i < 20; i++) {
            bigMap.put(i, "value-" + i);          // triggers resize at 3, 6, 12 entries
        }
        System.out.println(bigMap.size());       // 20 — all entries survive resize
        System.out.println(bigMap.get(15));      // "value-15"
    }
}
```

**Key observations from building this:**

1. **The hash function `h ^ (h >>> 16)`:** Without this, keys that differ only
   in high bits would hash to the same bucket in small arrays (capacity 16 uses
   only the lowest 4 bits of the hash). The XOR spreading makes all 32 bits
   participate in bucket selection.

2. **Why `capacity - 1` for bucket index:** `hash & 15` (capacity=16) gives
   0-15 in one CPU instruction. This only works because 15 in binary is `01111`
   — a sequence of 1s that acts as a perfect mask. If capacity were 17 (not a
   power of 2), you would need expensive modulo division instead.

3. **Why resize doubles:** After doubling, each bucket chain splits roughly in
   half because the new index bit (the one that changed when capacity doubled)
   routes half the entries to the "old" bucket index and half to `old + oldCapacity`.
   This distributes entries without recomputing all hashes from scratch.

4. **The equals/hashCode contract:** The `get()` method checks `e.hash == hash`
   first (fast int comparison) before calling `key.equals()` (potentially
   expensive). This is why the contract is: if `a.equals(b)` then
   `a.hashCode() == b.hashCode()`. Violating this means `get()` will compute
   the wrong bucket index and never find the entry.

**The question you must be able to answer after this exercise:**
"Why do we cache `e.hash` in the Entry node?"
Because during resize, we recompute the new bucket index from `e.hash & (newCapacity-1)`.
If we didn't cache it, we would have to call `key.hashCode()` again — expensive for
complex keys and potentially inconsistent if hashCode() is not stable.

---

## 5.6 HashSet: Nothing New

`HashSet<E>` is literally backed by a `HashMap<E, Object>`:

```java
// From OpenJDK source:
public class HashSet<E> {
    private transient HashMap<E,Object> map;
    private static final Object PRESENT = new Object(); // dummy value
    
    public boolean add(E e) {
        return map.put(e, PRESENT) == null;  // if put returns null, key was new
    }
    
    public boolean contains(Object o) {
        return map.containsKey(o);
    }
    
    public boolean remove(Object o) {
        return map.remove(o) == PRESENT;
    }
}
```

All the same O(1) average, hashCode/equals contract, resize behavior applies. If you understand HashMap, you understand HashSet.

---

## 5.7 TreeMap and TreeSet: Sorted Collections

`TreeMap` stores keys in a **Red-Black Tree** — a self-balancing BST. Every operation is O(log n).

```java
import java.util.*;

public class TreeMapDemo {
    public static void main(String[] args) {
        // Natural ordering (Comparable)
        TreeMap<String, Integer> scores = new TreeMap<>();
        scores.put("Charlie", 85);
        scores.put("Alice", 92);
        scores.put("Bob", 78);
        scores.put("Dave", 95);
        
        // Iteration is always in SORTED ORDER (alphabetical for String keys)
        for (Map.Entry<String, Integer> e : scores.entrySet()) {
            System.out.println(e.getKey() + ": " + e.getValue());
        }
        // Alice: 92
        // Bob: 78
        // Charlie: 85
        // Dave: 95
        
        // NavigableMap operations (unique to TreeMap):
        System.out.println(scores.firstKey());          // "Alice" — smallest key
        System.out.println(scores.lastKey());           // "Dave" — largest key
        System.out.println(scores.floorKey("Brenda"));  // "Bob" — largest key ≤ "Brenda"
        System.out.println(scores.ceilingKey("Brenda")); // "Charlie" — smallest key ≥ "Brenda"
        
        // Range views (backed by original map — modifications reflected both ways)
        SortedMap<String, Integer> subMap = scores.subMap("Bob", "Dave"); // Bob ≤ key < Dave
        NavigableMap<String, Integer> headMap = scores.headMap("Charlie", false); // key < Charlie
        NavigableMap<String, Integer> tailMap = scores.tailMap("Charlie", true);  // key ≥ Charlie
        
        // Custom ordering with Comparator
        TreeMap<String, Integer> byLength = new TreeMap<>(Comparator.comparingInt(String::length)
                                                           .thenComparing(Comparator.naturalOrder()));
        byLength.put("Cat", 1);
        byLength.put("Dog", 2);
        byLength.put("Elephant", 3);
        // Sorted by name length, then alphabetically within same length
        
        // TreeSet is backed by TreeMap with dummy values
        TreeSet<Integer> sortedNumbers = new TreeSet<>(Arrays.asList(5, 3, 8, 1, 9, 2));
        System.out.println(sortedNumbers);  // [1, 2, 3, 5, 8, 9]
        System.out.println(sortedNumbers.floor(4));    // 3 — largest ≤ 4
        System.out.println(sortedNumbers.ceiling(4));  // 5 — smallest ≥ 4
        System.out.println(sortedNumbers.headSet(5));  // [1, 2, 3] — elements < 5
        System.out.println(sortedNumbers.tailSet(5));  // [5, 8, 9] — elements ≥ 5
    }
}
```

---

## 5.8 LinkedHashMap: Order-Preserving HashMap

`LinkedHashMap` extends `HashMap` and adds a **doubly-linked list** through all entries in insertion order (or optionally access order):

```java
// Insertion order (default)
Map<String, Integer> linked = new LinkedHashMap<>();
linked.put("banana", 2);
linked.put("apple", 1);
linked.put("cherry", 3);

for (String key : linked.keySet()) {
    System.out.print(key + " ");
}
// banana apple cherry  ← preserves insertion order (HashMap would be unpredictable)

// LRU Cache using LinkedHashMap access-order mode
// 3rd parameter true = access order (most-recently-accessed at end)
Map<Integer, String> lruCache = new LinkedHashMap<>(16, 0.75f, true) {
    private static final int MAX_SIZE = 3;
    
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, String> eldest) {
        return size() > MAX_SIZE;  // evict oldest when over capacity
    }
};

lruCache.put(1, "one");
lruCache.put(2, "two");
lruCache.put(3, "three");
System.out.println(lruCache); // {1=one, 2=two, 3=three}

lruCache.get(1);               // access "one" — moves to end
System.out.println(lruCache); // {2=two, 3=three, 1=one}

lruCache.put(4, "four");       // exceeds MAX_SIZE → "two" (least recently used) evicted
System.out.println(lruCache); // {3=three, 1=one, 4=four}
```

---

## 5.9 PriorityQueue: The Heap-Based Priority Queue

```java
import java.util.*;

public class PriorityQueueDemo {
    public static void main(String[] args) {
        // Default: MIN-heap (smallest element at head)
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.offer(5);
        minHeap.offer(1);
        minHeap.offer(3);
        minHeap.offer(2);
        
        // peek(): O(1) — view min without removing
        System.out.println(minHeap.peek());  // 1
        
        // poll(): O(log n) — remove and return min
        while (!minHeap.isEmpty()) {
            System.out.print(minHeap.poll() + " "); // 1 2 3 5
        }
        
        // MAX-heap: reverse comparator
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
        maxHeap.offer(5);
        maxHeap.offer(1);
        maxHeap.offer(3);
        System.out.println(maxHeap.peek());  // 5
        
        // Custom comparator — useful for objects
        PriorityQueue<Task> taskQueue = new PriorityQueue<>(
            Comparator.comparingInt(Task::getPriority)
        );
        taskQueue.offer(new Task("Low priority",  3));
        taskQueue.offer(new Task("High priority", 1));
        taskQueue.offer(new Task("Medium",        2));
        
        while (!taskQueue.isEmpty()) {
            System.out.println(taskQueue.poll().getName());
        }
        // High priority (1), Medium (2), Low priority (3)
        
        // Internal structure: binary heap (complete binary tree stored in array)
        // Heap property: parent ≤ both children (for min-heap)
        // add: O(log n) — add at end, "bubble up" to restore heap property
        // poll: O(log n) — remove root, put last element at root, "bubble down"
        // peek: O(1) — root is always min
        // contains: O(n) — no ordering other than heap property
    }
    
    static class Task {
        private String name;
        private int priority;
        Task(String n, int p) { name = n; priority = p; }
        String getName() { return name; }
        int getPriority() { return priority; }
    }
}
```

---

## 5.10 ArrayDeque: Your Stack AND Queue

`ArrayDeque` (Array Double-Ended Queue) is backed by a resizable circular array. It is **faster than both `Stack` and `LinkedList`** as a stack or queue.

```java
import java.util.*;

public class ArrayDequeDemo {
    public static void main(String[] args) {
        // As a STACK (LIFO)
        Deque<String> stack = new ArrayDeque<>();
        stack.push("first");     // addFirst
        stack.push("second");    // addFirst
        stack.push("third");     // addFirst
        
        System.out.println(stack.peek());  // "third" — top of stack, O(1)
        System.out.println(stack.pop());   // "third" — remove top, O(1)
        System.out.println(stack.pop());   // "second"
        System.out.println(stack.pop());   // "first"
        
        // As a QUEUE (FIFO)
        Deque<String> queue = new ArrayDeque<>();
        queue.offer("first");    // addLast
        queue.offer("second");
        queue.offer("third");
        
        System.out.println(queue.peek());  // "first" — head, O(1)
        System.out.println(queue.poll());  // "first" — remove head, O(1)
        System.out.println(queue.poll());  // "second"
        
        // As a Deque — both ends available
        Deque<Integer> deque = new ArrayDeque<>();
        deque.addFirst(1);   // [1]
        deque.addLast(2);    // [1, 2]
        deque.addFirst(0);   // [0, 1, 2]
        deque.addLast(3);    // [0, 1, 2, 3]
        
        System.out.println(deque.peekFirst()); // 0
        System.out.println(deque.peekLast());  // 3
        deque.pollFirst();   // removes 0
        deque.pollLast();    // removes 3
        // [1, 2]
        
        // Why ArrayDeque beats Stack and LinkedList:
        // - Stack is synchronized (slow) and extends Vector (broken design)
        // - LinkedList has cache-unfriendly pointer chasing
        // - ArrayDeque is a circular array: O(1) for both ends, cache-friendly
    }
}
```

---

## 5.11 Choosing the Right Collection

```
QUESTION                        ANSWER           COLLECTION
──────────────────────────────────────────────────────────────────────────
Need indexed access by position?  Yes            ArrayList
Need FIFO queue?                  Yes            ArrayDeque
Need LIFO stack?                  Yes            ArrayDeque
Need priority ordering?           Yes            PriorityQueue
Need insertion order preserved?   Yes            LinkedHashMap or LinkedHashSet
Need sorted order by key?         Yes            TreeMap or TreeSet
Need unique elements, O(1)?       Yes            HashSet
Need key→value lookup, O(1)?      Yes            HashMap
Need sorted key→value?            Yes            TreeMap
Need thread-safe map?             Yes            ConcurrentHashMap (Chapter 7)
Need LRU cache?                   Yes            LinkedHashMap (access-order mode)
Need iteration over everything?   Yes (simple)   ArrayList
Frequent middle insert/remove?    (rare)         LinkedList (but profile first!)
```

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "Explain how HashMap works internally in Java 8 and beyond."**

**SDE-2 Answer:** HashMap is backed by an array of `Node[]` buckets, default capacity 16. When you `put(key, value)`, HashMap computes a hash by XORing `key.hashCode()` with its upper 16 bits — this "spreads" bits to reduce clustering. The bucket index is `hash & (capacity-1)` — bitwise AND is equivalent to modulo for power-of-two capacities and is faster. If the bucket is empty, a new `Node` is placed there. On collision (different keys map to same bucket), Java 7 chained into a linked list. Java 8 converts a bucket's linked list to a red-black tree when it reaches 8 entries, ensuring O(log n) worst-case instead of O(n). When `size > capacity * loadFactor (0.75)`, the table doubles and all entries rehash. For keys to work correctly in HashMap, `hashCode()` and `equals()` must follow the contract: equal objects must have equal hashCodes, meaning you must override both or neither. The canonical patterns are `Objects.hash(field1, field2)` for hashCode and field-by-field comparison for equals.

**Q2: "What is the time complexity of ArrayList.get() vs LinkedList.get()? Why?"**

**SDE-2 Answer:** `ArrayList.get(i)` is O(1) because ArrayList is backed by a `Object[]` array. Array elements are stored contiguously in memory. The address of element `i` is `base_address + i * pointer_size` — computed directly, no traversal. It's a single pointer dereference. `LinkedList.get(i)` is O(n) because there's no way to directly compute the address of node `i`. LinkedList must traverse from the head (or tail, if i > size/2) one node at a time until reaching position `i`. This also means O(n) for each iteration if you call `get(i)` in a loop — O(n²) total, which is a classic performance bug. For iteration, use a for-each loop (which uses the iterator and traverses the linked list once) rather than index-based access. For virtually all practical use cases, ArrayList outperforms LinkedList due to lower memory overhead (no prev/next pointers) and cache-friendly contiguous storage.

**Q3: "How does HashSet guarantee uniqueness? What happens if you put a duplicate?"**

**SDE-2 Answer:** HashSet is implemented as a `HashMap<E, Object>` where all values are the same dummy `PRESENT` object. When you call `set.add(e)`, it calls `map.put(e, PRESENT)`. HashMap's `put` first computes the bucket for `e`'s hash, then walks that bucket's chain checking `existing.hash == e.hash && existing.key.equals(e)`. If a matching key is found, its value is updated (to the same `PRESENT` — effectively a no-op) and the old value is returned. HashSet's `add()` checks whether `put` returned null (new key — added) or non-null (key existed — not added). Because HashSet depends on HashMap's key uniqueness, the hashCode/equals contract is critical: two objects that are `.equals()` must have the same hashCode, or you'll insert "duplicates" into different buckets and HashSet won't deduplicate them correctly.

# CHAPTER 6: Generics and Functional Programming

## 6.1 Why Generics Exist: The Pre-Generics Nightmare

Before generics (Java 1.4 and earlier), collections stored `Object` references. Every retrieval required a manual cast, and errors wouldn't be caught until runtime:

```java
// PRE-GENERICS (Java 1.4 style) — DON'T write this
List names = new ArrayList();
names.add("Alice");
names.add("Bob");
names.add(42);        // compiles fine — everything is Object!

// Casting nightmare — must cast every element
String first = (String) names.get(0);  // OK
String second = (String) names.get(1); // OK
String third = (String) names.get(2);  // ClassCastException at RUNTIME — 42 is not a String!

// No type safety. Bugs appear at runtime, not compile time.
```

**With generics (Java 5+):**
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
// names.add(42);  // COMPILE ERROR: incompatible types — found: int, required: String

String first = names.get(0);  // No cast needed — compiler knows it's String
// ClassCastException is impossible — type is checked at compile time
```

---

## 6.2 Generic Classes

```java
// T is a "type parameter" — a placeholder for whatever type the user provides
// Naming conventions: T = Type, E = Element, K = Key, V = Value, R = Return
public class Box<T> {
    private T content;
    
    public Box(T content) {
        this.content = content;
    }
    
    public T getContent() {
        return content;
    }
    
    public void setContent(T content) {
        this.content = content;
    }
    
    @Override
    public String toString() {
        return "Box[" + content + "]";
    }
}

// Multiple type parameters
public class Pair<A, B> {
    private final A first;
    private final B second;
    
    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }
    
    public A getFirst() { return first; }
    public B getSecond() { return second; }
    
    // Factory method — avoids repeating type on the right
    public static <X, Y> Pair<X, Y> of(X x, Y y) {
        return new Pair<>(x, y);
    }
}

// Usage
Box<String> strBox = new Box<>("Hello");
Box<Integer> intBox = new Box<>(42);
Box<List<String>> listBox = new Box<>(new ArrayList<>());  // nested generics

String s = strBox.getContent();   // No cast needed — compiler knows it's String
// intBox = strBox;  // COMPILE ERROR: type mismatch

Pair<String, Integer> nameAge = Pair.of("Surya", 3);
String name = nameAge.getFirst();  // "Surya"
int age = nameAge.getSecond();     // 3 (unboxed)
```

---

## 6.3 Generic Methods

A method can introduce its own type parameters, independent of the class's:

```java
public class GenericUtils {
    // <T extends Comparable<T>> — T can be compared to itself
    // This constrains T to types that implement Comparable (String, Integer, etc.)
    public static <T extends Comparable<T>> T max(T a, T b) {
        return a.compareTo(b) >= 0 ? a : b;
    }
    
    // T must extend Number (int, double, long, etc.)
    public static <T extends Number> double sum(List<T> list) {
        double total = 0;
        for (T item : list) {
            total += item.doubleValue();  // available because T extends Number
        }
        return total;
    }
    
    // Swap elements in an array — works for any reference type
    public static <T> void swap(T[] arr, int i, int j) {
        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    // Return first non-null element
    @SafeVarargs
    public static <T> T firstNonNull(T... values) {
        for (T val : values) {
            if (val != null) return val;
        }
        throw new NoSuchElementException("All values are null");
    }
}

// Usage — type is INFERRED from arguments:
int maxInt = GenericUtils.max(5, 10);         // T inferred as Integer
String maxStr = GenericUtils.max("apple", "banana"); // T inferred as String
double total = GenericUtils.sum(List.of(1, 2, 3));    // 6.0

String[] arr = {"a", "b", "c"};
GenericUtils.swap(arr, 0, 2);  // ["c", "b", "a"]
```

---

## 6.4 Bounded Type Parameters

```java
// Upper bounded: T must be Number or a subtype of Number
public static <T extends Number> void printSquare(T number) {
    double n = number.doubleValue();
    System.out.println(n * n);
}

printSquare(5);       // Integer extends Number — OK
printSquare(3.14);    // Double extends Number — OK
// printSquare("5");  // COMPILE ERROR: String doesn't extend Number

// Multiple bounds: T must extend Cloneable AND implement Serializable
public <T extends Cloneable & java.io.Serializable> void process(T item) { }

// A generic class with a bounded type parameter
public class SortedList<T extends Comparable<T>> {
    private List<T> items = new ArrayList<>();
    
    public void add(T item) {
        items.add(item);
        Collections.sort(items);  // can sort because T implements Comparable
    }
}
```

---

## 6.5 Wildcards: The PECS Rule

Wildcards (`?`) are for **use sites** — when calling a method that takes a generic type, not when defining a class.

### `? extends T` — Upper Bounded Wildcard (Producer Extends)

```java
// This method only READS from the list (list PRODUCES values)
public static double sumList(List<? extends Number> list) {
    double total = 0;
    for (Number n : list) {   // can read as Number
        total += n.doubleValue();
    }
    // list.add(3.14);  // COMPILE ERROR — can't add to a wildcard producer!
    // Why? list might be List<Integer>, and 3.14 (double) can't go in a List<Integer>
    return total;
}

// Works with any subtype of Number:
sumList(List.of(1, 2, 3));            // List<Integer> — OK
sumList(List.of(1.5, 2.5));          // List<Double>  — OK
sumList(List.of(1L, 2L));            // List<Long>    — OK
```

### `? super T` — Lower Bounded Wildcard (Consumer Super)

```java
// This method only WRITES to the list (list CONSUMES values)
public static void addNumbers(List<? super Integer> list) {
    list.add(1);    // OK — can add Integer
    list.add(2);
    list.add(3);
    // Integer x = list.get(0);  // COMPILE ERROR — could be List<Number>, so get() returns Object
    Object obj = list.get(0);   // can only read as Object
}

List<Integer> ints = new ArrayList<>();
List<Number> nums = new ArrayList<>();
List<Object> objs = new ArrayList<>();

addNumbers(ints);  // List<Integer> — ? super Integer: OK
addNumbers(nums);  // List<Number>  — Number is supertype of Integer: OK
addNumbers(objs);  // List<Object>  — Object is supertype of Integer: OK
```

### The PECS Mnemonic

```
PECS: Producer Extends, Consumer Super

If the collection PRODUCES elements you READ:  List<? extends T>
If the collection CONSUMES elements you WRITE: List<? super T>
If the collection does BOTH:                   List<T> (no wildcard)

Real example (Collections.copy):
public static <T> void copy(List<? super T> dest, List<? extends T> src) {
    //                             CONSUMER ↑              PRODUCER ↑
    for (T item : src) {     // read from src (producer, extends)
        dest.add(item);      // write to dest (consumer, super)
    }
}
```

---

## 6.6 Type Erasure: What Generics Are at Runtime

**Type erasure** means generic type information exists only at compile time. At runtime, all generic types are erased to their **raw types** (usually `Object` or the bound).

```java
// At compile time:        At runtime (after erasure):
List<String>         →    List
List<Integer>        →    List
Box<String>          →    Box
Box<Integer>         →    Box
T extends Number     →    Number (upper bound)
T                    →    Object (unbounded)
```

**Why this matters:**

```java
// You CANNOT do this — generic type info is gone at runtime:
public <T> void problematic() {
    // COMPILE ERROR: Cannot create generic array
    T[] arr = new T[10];  
    
    // COMPILE ERROR: Cannot use instanceof with generic type
    if (something instanceof T) { }
    
    // COMPILE ERROR: Cannot instantiate generic type
    T obj = new T();
}

// WORKAROUND: Pass the Class object explicitly
public <T> T[] createArray(Class<T> type, int size) {
    @SuppressWarnings("unchecked")
    T[] arr = (T[]) java.lang.reflect.Array.newInstance(type, size);
    return arr;
}

String[] strings = createArray(String.class, 10);
```

**Runtime type check — use the bound or cast:**
```java
// At runtime, List<String> and List<Integer> are BOTH just List
List<String> strings = new ArrayList<>();
List<Integer> ints = new ArrayList<>();

System.out.println(strings.getClass() == ints.getClass()); // true — both are ArrayList

// This compiles because of erasure (unchecked cast):
List rawList = strings;           // raw type (no generic) — warning
List<Integer> wrongType = rawList; // compiles! But ClassCastException when you actually use it

// So-called "heap pollution": a variable of parameterized type refers to an object
// that is not of that parameterized type. Results in ClassCastException deep in code.
```

---

## 6.7 Functional Interfaces and Lambdas

A **functional interface** is any interface with **exactly one abstract method**. It's the foundation for lambdas.

```java
// Any interface with one abstract method is a functional interface
@FunctionalInterface  // optional annotation — causes compile error if > 1 abstract method
interface MathOperation {
    int operate(int a, int b);  // one abstract method
    
    // Default methods don't count toward the "one abstract method" limit
    default MathOperation andThen(MathOperation after) {
        return (a, b) -> after.operate(this.operate(a, b), 0);
    }
}

// Before lambdas (Java 7): anonymous inner class
MathOperation add_old = new MathOperation() {
    @Override
    public int operate(int a, int b) { return a + b; }
};

// With lambda (Java 8+): same thing, much less ceremony
MathOperation add = (a, b) -> a + b;
MathOperation multiply = (a, b) -> a * b;
MathOperation max_op = (a, b) -> Math.max(a, b);

System.out.println(add.operate(5, 3));       // 8
System.out.println(multiply.operate(5, 3));  // 15
```

### Lambda Syntax

```java
// Form 1: No parameters
Runnable r = () -> System.out.println("Hello");

// Form 2: One parameter (parentheses optional for single param)
Consumer<String> print = s -> System.out.println(s);
Consumer<String> printParen = (s) -> System.out.println(s);

// Form 3: Multiple parameters
BiFunction<Integer, Integer, Integer> sum = (a, b) -> a + b;

// Form 4: Block body (multiple statements, explicit return)
BiFunction<Integer, Integer, Integer> sumWithLog = (a, b) -> {
    System.out.println("Adding " + a + " and " + b);
    int result = a + b;
    return result;  // explicit return required in block body
};

// Form 5: Type inference (compiler figures out types)
Comparator<String> byLength = (s1, s2) -> s1.length() - s2.length();
// Could also write: (String s1, String s2) -> s1.length() - s2.length()

// Variable capture: lambdas can capture final or effectively-final variables
int threshold = 10;  // effectively final (never reassigned after this)
Predicate<Integer> isAboveThreshold = n -> n > threshold;  // captures threshold
// threshold = 20;  // Would make threshold not effectively-final → compile error
```

---

## 6.8 Method References: Four Types

Method references are shorthand for lambdas that just call a method:

```java
import java.util.*;
import java.util.function.*;

public class MethodRefDemo {
    
    static int doubleIt(int n) { return n * 2; }  // static method
    
    int triple(int n) { return n * 3; }           // instance method
    
    public static void main(String[] args) {
        MethodRefDemo obj = new MethodRefDemo();
        
        // TYPE 1: Static method reference — ClassName::staticMethod
        Function<Integer, Integer> doubler = MethodRefDemo::doubleIt;
        // equivalent to: n -> MethodRefDemo.doubleIt(n)
        
        // TYPE 2: Instance method of a specific instance — instance::method
        Function<Integer, Integer> tripler = obj::triple;
        // equivalent to: n -> obj.triple(n)
        
        // TYPE 3: Instance method of an arbitrary instance — ClassName::method
        // The first lambda parameter becomes "this" (the instance to call on)
        Function<String, String> toUpper = String::toUpperCase;
        // equivalent to: s -> s.toUpperCase()
        
        // Comparator using method reference
        Comparator<String> byLength = Comparator.comparingInt(String::length);
        // equivalent to: (s1, s2) -> s1.length() - s2.length()
        
        // TYPE 4: Constructor reference — ClassName::new
        Supplier<ArrayList<String>> listFactory = ArrayList::new;
        // equivalent to: () -> new ArrayList<>()
        
        Function<String, StringBuilder> sbFactory = StringBuilder::new;
        // equivalent to: s -> new StringBuilder(s)
        
        // Practical example — sort list by length using method reference
        List<String> names = Arrays.asList("Charlie", "Alice", "Bob", "Dave");
        names.sort(Comparator.comparingInt(String::length));
        System.out.println(names);  // [Bob, Dave, Alice, Charlie]
        
        // forEach with method reference
        names.forEach(System.out::println);  // prints each name
        
        // Stream + method reference
        List<String> upper = names.stream()
            .map(String::toUpperCase)
            .collect(Collectors.toList());
    }
}
```

---

## 6.9 The Core Functional Interfaces

Java's `java.util.function` package provides a standard library of functional interfaces:

```java
import java.util.function.*;
import java.util.*;

public class FunctionalInterfaceDemo {
    public static void main(String[] args) {
        
        // ── PREDICATE<T>: T → boolean ──────────────────────────────────────
        Predicate<String> isLong = s -> s.length() > 5;
        Predicate<String> startsWithA = s -> s.startsWith("A");
        
        System.out.println(isLong.test("Hello"));           // false
        System.out.println(isLong.test("HelloWorld"));       // true
        
        // Combinators
        Predicate<String> longAndA = isLong.and(startsWithA);
        Predicate<String> longOrA = isLong.or(startsWithA);
        Predicate<String> notLong = isLong.negate();
        
        System.out.println(longAndA.test("Algorithms"));    // true (long AND starts with A)
        System.out.println(longOrA.test("At"));             // true (starts with A)
        System.out.println(notLong.test("Hi"));             // true
        
        // ── FUNCTION<T,R>: T → R ───────────────────────────────────────────
        Function<String, Integer> length = String::length;
        Function<Integer, String> intToStr = n -> "Number: " + n;
        
        // compose: apply other FIRST, then this
        // andThen: apply this FIRST, then other
        Function<String, String> lengthAsString = length.andThen(intToStr);
        System.out.println(lengthAsString.apply("Hello"));  // "Number: 5"
        
        // ── CONSUMER<T>: T → void ──────────────────────────────────────────
        Consumer<String> printer = System.out::println;
        Consumer<String> upperPrinter = s -> System.out.println(s.toUpperCase());
        
        Consumer<String> printBoth = printer.andThen(upperPrinter);
        printBoth.accept("hello");  // prints "hello" then "HELLO"
        
        // ── SUPPLIER<T>: () → T ────────────────────────────────────────────
        Supplier<String> greeting = () -> "Hello, World!";
        Supplier<List<String>> listFactory = ArrayList::new;
        
        System.out.println(greeting.get());        // "Hello, World!"
        List<String> newList = listFactory.get();  // fresh empty list
        
        // ── BIFUNCTION<T,U,R>: (T,U) → R ──────────────────────────────────
        BiFunction<String, Integer, String> repeat = (s, n) -> s.repeat(n);
        System.out.println(repeat.apply("ha", 3));  // "hahaha"
        
        // ── UNARYOPERATOR<T>: T → T (Function where input == output type) ──
        UnaryOperator<String> trim = String::trim;
        UnaryOperator<Integer> square = n -> n * n;
        
        System.out.println(trim.apply("  hello  "));  // "hello"
        System.out.println(square.apply(5));           // 25
        
        // ── BINARYOPERATOR<T>: (T,T) → T ──────────────────────────────────
        BinaryOperator<Integer> add = Integer::sum;
        BinaryOperator<String> concat = String::concat;
        
        System.out.println(add.apply(3, 4));          // 7
        System.out.println(concat.apply("foo", "bar")); // "foobar"
        
        // Useful with Stream.reduce:
        List<Integer> nums = List.of(1, 2, 3, 4, 5);
        int product = nums.stream().reduce(1, (a, b) -> a * b);
        System.out.println(product); // 120
    }
}
```

---

```
┌──────────────────────────────────────────────────────────────────┐
│  JAVASCRIPT VS JAVA: Functional Programming and Streams           │
│                                                                    │
│  JavaScript Array methods vs Java Streams — superficially similar,│
│  fundamentally different in one critical way: LAZINESS.           │
│                                                                    │
│  JavaScript (EAGER — executes immediately):                        │
│  const result = arr                                                │
│    .filter(x => x > 0)     // executes NOW, returns new Array     │
│    .map(x => x * 2)        // executes NOW, returns new Array     │
│    .slice(0, 10);           // executes NOW                        │
│  // 3 full passes through the data                                │
│                                                                    │
│  Java Streams (LAZY — nothing executes until terminal):           │
│  List<Integer> result = stream                                     │
│    .filter(x -> x > 0)     // DOES NOTHING YET (intermediate)    │
│    .map(x -> x * 2)        // DOES NOTHING YET (intermediate)    │
│    .limit(10)              // DOES NOTHING YET (intermediate)    │
│    .collect(toList());     // terminal — NOW everything executes  │
│  // 1 pass through the data, stops after finding 10 elements      │
│                                                                    │
│  Java's laziness enables short-circuit optimization:              │
│  Stream.of(1,2,3,4,5).filter(x -> x > 0).findFirst()            │
│  → stops after finding the FIRST match, never processes 2,3,4,5  │
│  In JS: arr.filter(x => x > 0)[0] — processes the ENTIRE array   │
│                                                                    │
│  JavaScript has no parallel processing equivalent.                │
│  Java: stream.parallel() distributes work across CPU cores.       │
└──────────────────────────────────────────────────────────────────┘
```

## 6.10 Streams API: Complete Reference

A `Stream` is a pipeline of operations on a sequence of elements. It is **lazy**: intermediate operations don't execute until a terminal operation triggers processing.

```
DATA SOURCE                   INTERMEDIATE OPS             TERMINAL OP
(collection, array, file)    (lazy, can chain)            (triggers execution, returns result)
         ↓                         ↓↓↓                            ↓
  List.stream()    →    .filter()  →  .map()  →  .sorted()  →  .collect()
                                                               .count()
                                                               .findFirst()
                                                               .forEach()
                                                               .reduce()
                                                               .anyMatch()
```

### Complete Stream Operations Reference

```java
import java.util.*;
import java.util.stream.*;
import java.util.function.*;

public class StreamReference {
    
    record Employee(String name, String dept, double salary, int joinYear) {}
    
    public static void main(String[] args) {
        List<Employee> employees = List.of(
            new Employee("Alice",   "Engineering", 95000, 2019),
            new Employee("Bob",     "Marketing",   72000, 2020),
            new Employee("Charlie", "Engineering", 88000, 2021),
            new Employee("Dave",    "HR",          65000, 2018),
            new Employee("Eve",     "Engineering", 102000, 2017),
            new Employee("Frank",   "Marketing",   78000, 2022),
            new Employee("Grace",   "HR",          69000, 2020)
        );
        
        // ─────────────────── CREATING STREAMS ───────────────────────────────
        Stream<String> fromList = List.of("a","b","c").stream();
        Stream<String> fromArray = Arrays.stream(new String[]{"x","y"});
        Stream<String> ofValues = Stream.of("hello", "world");
        Stream<Integer> range = IntStream.rangeClosed(1, 10).boxed();
        Stream<String> generated = Stream.generate(() -> "repeat").limit(5);
        Stream<Integer> iterate = Stream.iterate(0, n -> n + 2).limit(10); // 0,2,4,6...
        Stream<String> concat = Stream.concat(fromList, ofValues);
        
        // ─────────────────── FILTERING ──────────────────────────────────────
        List<Employee> engineers = employees.stream()
            .filter(e -> "Engineering".equals(e.dept()))   // keeps matching elements
            .collect(Collectors.toList());
        
        // ─────────────────── MAPPING (TRANSFORMING) ─────────────────────────
        List<String> names = employees.stream()
            .map(Employee::name)           // Employee → String
            .collect(Collectors.toList()); // ["Alice","Bob","Charlie","Dave","Eve","Frank","Grace"]
        
        // flatMap: each element → multiple elements (flattens nested streams)
        List<String> words = List.of("Hello World", "Java Streams");
        List<String> allWords = words.stream()
            .flatMap(s -> Arrays.stream(s.split(" ")))  // each String → Stream<String>
            .collect(Collectors.toList()); // ["Hello","World","Java","Streams"]
        
        // mapToInt, mapToDouble, mapToLong → primitive streams (avoid boxing)
        IntStream salaries = employees.stream()
            .mapToInt(e -> (int) e.salary());
        int totalSalary = salaries.sum(); // primitive stream has sum(), average(), etc.
        
        // ─────────────────── SORTING ────────────────────────────────────────
        List<Employee> bySalaryDesc = employees.stream()
            .sorted(Comparator.comparingDouble(Employee::salary).reversed())
            .collect(Collectors.toList());
        
        // Multiple sort keys
        List<Employee> byDeptThenSalary = employees.stream()
            .sorted(Comparator.comparing(Employee::dept)
                              .thenComparingDouble(Employee::salary).reversed())
            .collect(Collectors.toList());
        
        // ─────────────────── LIMITING / SKIPPING ────────────────────────────
        List<Employee> top3 = employees.stream()
            .sorted(Comparator.comparingDouble(Employee::salary).reversed())
            .limit(3)         // take first 3
            .collect(Collectors.toList());
        
        List<Employee> skipFirst2 = employees.stream()
            .skip(2)          // skip first 2 elements
            .collect(Collectors.toList());
        
        // ─────────────────── DISTINCT / PEEK ────────────────────────────────
        List<String> depts = employees.stream()
            .map(Employee::dept)
            .distinct()                   // remove duplicates (uses equals/hashCode)
            .sorted()
            .collect(Collectors.toList()); // ["Engineering", "HR", "Marketing"]
        
        List<Employee> debugPipeline = employees.stream()
            .peek(e -> System.out.println("Before filter: " + e.name()))
            .filter(e -> e.salary() > 80000)
            .peek(e -> System.out.println("After filter: " + e.name()))
            .collect(Collectors.toList()); // peek: debug only, no transformation
        
        // ─────────────────── TERMINAL: COLLECTING ────────────────────────────
        // toList (Java 16+)
        List<String> nameList = employees.stream().map(Employee::name).toList(); // immutable
        
        // toSet
        Set<String> deptSet = employees.stream()
            .map(Employee::dept)
            .collect(Collectors.toSet());
        
        // toMap
        Map<String, Double> nameSalary = employees.stream()
            .collect(Collectors.toMap(
                Employee::name,     // keyMapper
                Employee::salary,   // valueMapper
                // merge function — needed only if duplicate keys possible:
                (existing, replacement) -> Math.max(existing, replacement)
            ));
        
        // groupingBy — groups elements by a classifier
        Map<String, List<Employee>> byDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::dept));
        // {"Engineering": [Alice, Charlie, Eve], "Marketing": [Bob, Frank], "HR": [Dave, Grace]}
        
        // groupingBy with downstream collector
        Map<String, Long> countByDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::dept, Collectors.counting()));
        // {"Engineering": 3, "Marketing": 2, "HR": 2}
        
        Map<String, Double> avgSalaryByDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::dept,
                     Collectors.averagingDouble(Employee::salary)));
        
        Map<String, Optional<Employee>> highestPaidByDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::dept,
                     Collectors.maxBy(Comparator.comparingDouble(Employee::salary))));
        
        // partitioningBy — special groupingBy for boolean predicates
        Map<Boolean, List<Employee>> partitioned = employees.stream()
            .collect(Collectors.partitioningBy(e -> e.salary() > 80000));
        // {true: [Alice, Charlie, Eve], false: [Bob, Dave, Frank, Grace]}
        
        // joining
        String namesCsv = employees.stream()
            .map(Employee::name)
            .collect(Collectors.joining(", ", "[", "]"));
        // "[Alice, Bob, Charlie, Dave, Eve, Frank, Grace]"
        
        // ─────────────────── TERMINAL: AGGREGATION ──────────────────────────
        long count = employees.stream().filter(e -> e.salary() > 80000).count();
        
        Optional<Employee> richest = employees.stream()
            .max(Comparator.comparingDouble(Employee::salary));
        richest.ifPresent(e -> System.out.println("Highest paid: " + e.name()));
        
        OptionalDouble avg = employees.stream()
            .mapToDouble(Employee::salary)
            .average(); // 81285.71...
        
        double total = employees.stream()
            .mapToDouble(Employee::salary)
            .sum();
        
        DoubleSummaryStatistics stats = employees.stream()
            .mapToDouble(Employee::salary)
            .summaryStatistics();
        // count, sum, min, max, average all in one pass
        
        // reduce: fold elements using a BinaryOperator
        Optional<Double> sumSalary = employees.stream()
            .map(Employee::salary)
            .reduce(Double::sum);  // (a, b) -> a + b
        
        double sumWithIdentity = employees.stream()
            .map(Employee::salary)
            .reduce(0.0, Double::sum);  // 0.0 is identity value
        
        // ─────────────────── TERMINAL: SEARCHING ────────────────────────────
        Optional<Employee> first = employees.stream()
            .filter(e -> "Engineering".equals(e.dept()))
            .findFirst();   // deterministic — returns first in encounter order
        
        Optional<Employee> any = employees.stream()
            .filter(e -> e.salary() > 90000)
            .findAny();     // may return any match — better for parallel streams
        
        boolean anyHighEarner = employees.stream().anyMatch(e -> e.salary() > 100000);  // true (Eve)
        boolean allHighEarner = employees.stream().allMatch(e -> e.salary() > 60000);   // true
        boolean noneNegative  = employees.stream().noneMatch(e -> e.salary() < 0);      // true
        
        // ─────────────────── TERMINAL: forEach ──────────────────────────────
        employees.stream()
            .filter(e -> "Engineering".equals(e.dept()))
            .sorted(Comparator.comparingDouble(Employee::salary).reversed())
            .forEach(e -> System.out.printf("%-10s $%.0f%n", e.name(), e.salary()));
    }
}
```

### Practical Stream Exercises on Employee Data

```java
public class StreamExercises {
    record Employee(String name, String dept, double salary, int joinYear) {}
    
    static List<Employee> employees = List.of( /* same list as above */ );
    
    public static void main(String[] args) {
        // Exercise 1: Names of all employees in Engineering, sorted alphabetically
        List<String> engNames = employees.stream()
            .filter(e -> "Engineering".equals(e.dept()))
            .map(Employee::name)
            .sorted()
            .collect(Collectors.toList());
        System.out.println(engNames); // [Alice, Charlie, Eve]
        
        // Exercise 2: Average salary per department
        Map<String, Double> avgByDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::dept,
                     Collectors.averagingDouble(Employee::salary)));
        
        // Exercise 3: Total salary bill for employees who joined before 2021
        double oldBill = employees.stream()
            .filter(e -> e.joinYear() < 2021)
            .mapToDouble(Employee::salary)
            .sum();
        
        // Exercise 4: Top 2 highest-paid employees (name and salary)
        employees.stream()
            .sorted(Comparator.comparingDouble(Employee::salary).reversed())
            .limit(2)
            .forEach(e -> System.out.printf("%s: $%.0f%n", e.name(), e.salary()));
        
        // Exercise 5: Count employees in each department
        Map<String, Long> countByDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::dept, Collectors.counting()));
        
        // Exercise 6: Does any HR employee earn > 70000?
        boolean hrHighEarner = employees.stream()
            .filter(e -> "HR".equals(e.dept()))
            .anyMatch(e -> e.salary() > 70000);
        System.out.println(hrHighEarner); // false
        
        // Exercise 7: Comma-separated names of all employees
        String allNames = employees.stream()
            .map(Employee::name)
            .collect(Collectors.joining(", "));
        
        // Exercise 8: Highest-paid employee in each department
        Map<String, Optional<Employee>> richestByDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::dept,
                     Collectors.maxBy(Comparator.comparingDouble(Employee::salary))));
        
        // Exercise 9: Employees hired in 2020, sorted by salary desc
        List<Employee> hired2020 = employees.stream()
            .filter(e -> e.joinYear() == 2020)
            .sorted(Comparator.comparingDouble(Employee::salary).reversed())
            .collect(Collectors.toList());
        
        // Exercise 10: Is everyone earning above minimum wage ($20,000/yr)? 
        boolean allAboveMin = employees.stream().allMatch(e -> e.salary() > 20_000);
    }
}
```

### Parallel Streams: When to Use and When Not To

```java
// Use: large datasets, CPU-bound operations, no shared mutable state
List<Integer> huge = IntStream.rangeClosed(1, 10_000_000)
    .boxed()
    .collect(Collectors.toList());

double sum = huge.parallelStream()
    .mapToDouble(Integer::doubleValue)
    .sum();  // splits work across CPU cores — may be 2-4x faster

// DO NOT USE parallel streams for:
// 1. Small datasets (overhead > gain)
List<String> small = List.of("a", "b", "c");
small.parallelStream().forEach(System.out::println);  // silly — overhead kills benefit

// 2. I/O-bound operations (threads block; use CompletableFuture instead)
// 3. Stateful lambdas (accumulating into shared mutable state = data races)
List<Integer> results = new ArrayList<>();
IntStream.range(0, 100).parallel().forEach(results::add);
// results is NOT thread-safe — concurrent adds cause corruption!
// FIX: use collect() instead of forEach with shared mutable state

// 4. Order-dependent operations (parallel reorders elements)
// findFirst() on parallel stream may return different element than sequential
```

---

## 6.11 Optional: Null Safety Done Right

`Optional<T>` is a container that may or may not contain a value. It's a type-safe alternative to returning `null`.

```java
import java.util.Optional;

public class OptionalDemo {
    
    record User(Long id, String name, Address address) {}
    record Address(String city, String country) {}
    
    // Traditional: returns null if not found (caller must remember to null-check!)
    public User findUserOld(Long id) {
        return null; // "user not found" — caller might NPE
    }
    
    // Modern: return type signals "might not exist"
    public Optional<User> findUser(Long id) {
        if (id == 1L) return Optional.of(new User(1L, "Alice", new Address("NYC", "USA")));
        return Optional.empty();  // explicit "not found"
    }
    
    public static void main(String[] args) {
        OptionalDemo demo = new OptionalDemo();
        
        // Creating Optional values
        Optional<String> present = Optional.of("Hello");        // NEVER null — throws NPE if null
        Optional<String> nullable = Optional.ofNullable(null);  // may be null — wraps as empty
        Optional<String> empty = Optional.empty();               // explicitly empty
        
        // Checking presence (basic but necessary)
        System.out.println(present.isPresent()); // true
        System.out.println(empty.isEmpty());     // true (Java 11+)
        
        // BAD pattern — defeats the purpose of Optional
        Optional<User> userOpt = demo.findUser(1L);
        if (userOpt.isPresent()) {
            User u = userOpt.get(); // .get() on potentially-empty Optional is an anti-pattern
            System.out.println(u.name());
        }
        
        // GOOD patterns — chain operations without ever calling .get()
        
        // map: transform value if present
        Optional<String> cityOpt = demo.findUser(1L)
            .map(User::address)            // Optional<User> → Optional<Address>
            .map(Address::city);           // Optional<Address> → Optional<String>
        System.out.println(cityOpt);       // Optional[NYC]
        
        // flatMap: when the mapping function itself returns Optional
        Optional<String> cityFlatMapped = demo.findUser(1L)
            .flatMap(u -> Optional.ofNullable(u.address())) // User → Optional<Address>
            .map(Address::city);
        
        // filter: keep value only if it matches predicate
        Optional<User> aliceOnly = demo.findUser(1L)
            .filter(u -> "Alice".equals(u.name()));
        
        // Getting the value safely
        String city1 = demo.findUser(1L)
            .map(User::address)
            .map(Address::city)
            .orElse("Unknown");                     // default if empty: "NYC"
        
        String city2 = demo.findUser(999L)
            .map(User::address)
            .map(Address::city)
            .orElse("Unknown");                     // default if empty: "Unknown"
        
        String city3 = demo.findUser(999L)
            .map(User::address)
            .map(Address::city)
            .orElseGet(() -> computeDefaultCity()); // lazy — lambda only called if empty
        
        // orElseThrow: throw exception if empty
        User user = demo.findUser(1L)
            .orElseThrow(() -> new RuntimeException("User not found"));
        
        // ifPresent: perform action only if value present
        demo.findUser(1L).ifPresent(u -> System.out.println("Found: " + u.name()));
        
        // ifPresentOrElse (Java 9+)
        demo.findUser(999L).ifPresentOrElse(
            u -> System.out.println("Found: " + u.name()),
            () -> System.out.println("User not found")
        );
        
        // Anti-patterns:
        // 1. Optional as method parameter — forces caller to wrap value needlessly
        //    void process(Optional<User> user) { }  // BAD
        //    void process(User user) { }             // GOOD — use @Nullable annotation
        
        // 2. Optional in collections/fields — use null or empty string instead
        //    Map<String, Optional<User>> map;  // BAD — ugly and wasteful
        
        // 3. Using .get() without checking — same problem as null
        //    optional.get();  // throws NoSuchElementException if empty — NO improvement
    }
    
    static String computeDefaultCity() {
        System.out.println("Computing default...");
        return "Global";
    }
}
```

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "What is type erasure? What are bounded wildcards?"**

**SDE-2 Answer:** Type erasure means generic type parameters exist only at compile time. After compilation, the compiler replaces all type parameters with their bounds (or Object if unbounded): `List<String>` becomes `List`, `T extends Number` becomes `Number`. This means at runtime, `List<String>` and `List<Integer>` are both just `List`, and you can't use `instanceof T` or `new T()`. Erasure was a design choice for backward compatibility with pre-generics Java code. Bounded wildcards (`? extends T` and `? super T`) let you express constraints on what type arguments are acceptable. `? extends T` is an upper-bounded wildcard used for producers — you can read elements from the collection as type T but can't add to it. `? super T` is a lower-bounded wildcard used for consumers — you can add T values to it but can only read as Object. The PECS mnemonic (Producer Extends, Consumer Super) helps choose. Example: `Collections.copy(List<? super T> dest, List<? extends T> src)` — source produces, destination consumes.

**Q2: "What is the difference between intermediate and terminal Stream operations? Why are intermediate operations lazy?"**

**SDE-2 Answer:** Intermediate operations (filter, map, flatMap, sorted, distinct, limit, skip, peek) describe transformations but don't execute — they build a pipeline descriptor. Terminal operations (collect, forEach, count, reduce, min, max, findFirst, anyMatch, allMatch, etc.) trigger the actual execution. Laziness is the key optimization: if you write `stream.filter(...).map(...).findFirst()`, the JVM doesn't build a filtered-and-mapped intermediate list. Instead, it evaluates elements one at a time: take element 0, run it through filter, if it passes run it through map, check if it satisfies findFirst (terminal). As soon as findFirst finds a result, the entire stream stops — no remaining elements are processed at all. For a stream of 1 million elements where the first element passes the filter, you do exactly one filter check and one map — not one million. This is called "short-circuit evaluation" for terminal operations like findFirst, anyMatch, limit.

**Q3: "Explain Optional and how to use it correctly."**

**SDE-2 Answer:** `Optional<T>` is a container type that explicitly represents "a value that might not be present." Its purpose is to make absence of a value visible in the type signature rather than returning null (which callers can forget to check). Correct usage: return `Optional.empty()` from repository/service methods when a resource isn't found; chain operations using `.map()`, `.flatMap()`, `.filter()` without unwrapping; use `.orElse()` or `.orElseGet()` (lazy version for expensive defaults) for a fallback, or `.orElseThrow()` when absence is exceptional. Anti-patterns: using `.get()` directly without checking (same NPE risk as null), using Optional as a method parameter (caller should just pass null or overload the method), storing Optional in collections or as instance fields (adds object allocation overhead without benefit). Optional does NOT replace null in all cases — it's specifically for method return types to signal potential absence.

# CHAPTER 7: Java Concurrency

```
┌──────────────────────────────────────────────────────────────────┐
│  JAVASCRIPT VS JAVA: The Most Important Mental Model Shift         │
│                                                                    │
│  JavaScript: Single-threaded event loop                           │
│  • ONE call stack — only one thing runs at a time                 │
│  • async/await is cooperative yielding, NOT parallelism           │
│  • Promise.all() fires multiple promises but they interleave      │
│    on a single thread — not truly parallel                        │
│  • CANNOT have a race condition in pure JS code                   │
│  • Web Workers: separate threads but NO shared memory             │
│                                                                    │
│  Java: True OS-level threads sharing memory                       │
│  • Multiple threads run LITERALLY SIMULTANEOUSLY on different CPUs │
│  • Two threads CAN read and write the same memory at the same time│
│  • Race conditions, deadlocks, and visibility bugs are REAL       │
│  • synchronized, volatile, and atomic classes exist for this      │
│                                                                    │
│  The analogy that makes it click:                                  │
│  JavaScript: one chef in a kitchen, switching between tasks       │
│  Java: multiple chefs in a kitchen, all cooking simultaneously    │
│  The risk in Java: two chefs reaching for the same knife at once  │
│                                                                    │
│  EVERYTHING in this chapter exists because Java has multiple       │
│  chefs. If Java were single-threaded like JavaScript, there       │
│  would be no need for synchronized, volatile, or AtomicInteger.  │
└──────────────────────────────────────────────────────────────────┘
```

## 7.1 The JavaScript vs Java Mental Model Shift

Before writing a single line of concurrent Java, you must discard your JavaScript mental model completely.

**JavaScript:** Single-threaded event loop. Your code never truly runs in parallel. Asynchronous operations (`setTimeout`, `fetch`, Promises) schedule callbacks, but only one piece of JavaScript executes at a time. There are no shared mutable state problems because there's only ever one thread of execution.

```javascript
// JavaScript: no race condition possible here
let counter = 0;
setTimeout(() => counter++, 0);
setTimeout(() => counter++, 0);
// After both fire: counter = 2. Guaranteed. Always.
// The event loop ensures they never overlap.
```

**Java:** True OS threads running in parallel on multiple CPU cores. Multiple threads can read and write the same memory location simultaneously. If you don't coordinate access, the results are unpredictable, non-reproducible, and data-corrupting.

```java
// Java: race condition — counter value after 1000 threads is unpredictable
int counter = 0;
for (int i = 0; i < 1000; i++) {
    new Thread(() -> counter++).start();  // DANGER: unsynchronized
}
// counter might be 997, 945, 1000, anything — depends on timing
```

The mental shift: in Java, **concurrent access to shared mutable state is the default problem** you must actively solve. Every field that multiple threads can reach requires deliberate protection.

---

## 7.2 Thread Creation: Three Approaches

```java
public class ThreadCreation {
    public static void main(String[] args) throws InterruptedException {
        
        // ── APPROACH 1: Runnable (lambda) — preferred ─────────────────────
        Runnable task = () -> {
            System.out.println("Running in: " + Thread.currentThread().getName());
        };
        Thread t1 = new Thread(task, "worker-1");
        t1.start();     // start() creates the OS thread and schedules it
        // t1.run();    // DON'T call run() directly — it runs on the CURRENT thread!
        
        // ── APPROACH 2: Callable — can return a value and throw checked exceptions ──
        Callable<Integer> computation = () -> {
            Thread.sleep(100);
            return 42;
        };
        // Callable needs an executor to run (covered in ExecutorService section)
        
        // ── APPROACH 3: Extend Thread — rarely done in modern code ──────────
        Thread t2 = new Thread("worker-2") {
            @Override
            public void run() {
                System.out.println("Running in: " + getName());
            }
        };
        t2.start();
        
        // ── Thread methods ───────────────────────────────────────────────────
        Thread current = Thread.currentThread();
        System.out.println(current.getName());     // "main"
        System.out.println(current.getId());       // thread ID (long)
        System.out.println(current.getPriority()); // 1–10, default 5
        System.out.println(current.isDaemon());    // false for main thread
        
        t1.join();  // block current thread until t1 finishes
        t2.join();  // block current thread until t2 finishes
        
        // Daemon threads: JVM exits when only daemon threads remain
        Thread daemon = new Thread(() -> {
            while (true) { /* background work */ }
        });
        daemon.setDaemon(true);  // must set BEFORE start()
        daemon.start();
        // JVM will exit even while daemon runs — good for background services
    }
}
```

---

## 7.3 Thread Lifecycle

```
                         ┌─────────────────────────────────┐
                         │           BLOCKED               │
                         │   Waiting for monitor lock      │
                         │   (another thread holds it)     │
                         └───────────┬─────────────────────┘
                                     │ lock released
┌───────┐  start()  ┌───────────┐    │         ┌───────────────────────────────┐
│  NEW  │ ────────→ │ RUNNABLE  │ ←──┘         │           WAITING             │
│       │           │           │              │   Object.wait()               │
│Thread │           │ Scheduled │ ─────────────→  Thread.join() (no timeout)   │
│created│           │ by OS to  │  wait()      │   LockSupport.park()          │
│not yet│           │ run on CPU │              └──────────────┬────────────────┘
│started│           │           │                             │ notify/interrupt
└───────┘           │           │ ←───────────────────────────┘
                    │           │
                    │           │ sleep(ms)  ┌────────────────────────────────┐
                    │           │ ────────→  │      TIMED_WAITING             │
                    │           │ ←────────  │  Thread.sleep(n)               │
                    │           │ timeout    │  Object.wait(n)                │
                    └─────┬─────┘            │  Thread.join(n)                │
                          │                 └────────────────────────────────┘
                          │ run() completes or exception
                          ▼
                    ┌──────────┐
                    │TERMINATED│
                    └──────────┘

Key transitions:
- NEW → RUNNABLE: Thread.start()
- RUNNABLE → BLOCKED: trying to enter synchronized block held by another thread
- RUNNABLE → WAITING: Object.wait(), Thread.join(), LockSupport.park()
- RUNNABLE → TIMED_WAITING: Thread.sleep(n), Object.wait(n), Thread.join(n)
- WAITING/TIMED_WAITING → RUNNABLE: notify(), interrupt(), timeout expires
- Any → TERMINATED: run() returns, or uncaught exception propagates out
```

---

## 7.4 The Three Concurrency Problems

Every concurrency bug is a manifestation of one or more of these three problems:

### Problem 1: Visibility

Modern CPUs have multi-level caches (L1, L2, L3). When a thread writes to a variable, the value may sit in that CPU core's L1 cache for a while before being flushed to main memory. Another thread running on a different core may read a stale value from its own cache.

```
CPU Core 0              CPU Core 1
(Thread A running)      (Thread B running)
L1 Cache: counter=5     L1 Cache: counter=0   ← stale!
    │                       │
    ▼                       ▼
          Main Memory: counter=5
          
Thread B reads counter=0 because its cache is stale.
Thread B's write of counter++ is based on wrong data.
```

### Problem 2: Atomicity

A single Java statement often compiles to multiple CPU instructions. The thread scheduler can preempt a thread between any two instructions.

```
Java: counter++
Compiles to 3 CPU instructions:
   1. READ:  load counter from memory into register
   2. MODIFY: increment register by 1
   3. WRITE: store register back to memory

Thread A (READ: counter=5, MODIFY: register=6) ← preempted here!
Thread B (READ: counter=5, MODIFY: register=6, WRITE: counter=6)
Thread A resumes (WRITE: counter=6)           ← LOST UPDATE! counter should be 7
```

### Problem 3: Ordering (Instruction Reordering)

Both the JVM/JIT compiler and the CPU hardware can **reorder instructions** for optimization, as long as the result appears correct *within a single thread*. But this can break multi-thread assumptions.

```java
// Within one thread, this reordering is valid (same result):
// Original:  a = 1; b = 2; x = a + b;
// Reordered: b = 2; a = 1; x = a + b;  // same final result

// But if another thread is watching 'a' and 'b':
// Another thread may see b=2 before a=1 even though code says a=1 first
```

---

## 7.5 Proving a Race Condition: `counter++` with 100 Threads

```java
import java.util.concurrent.CountDownLatch;

public class RaceConditionDemo {
    private static int counter = 0;
    
    public static void main(String[] args) throws InterruptedException {
        int threadCount = 100;
        int incrementsPerThread = 1000;
        
        CountDownLatch latch = new CountDownLatch(threadCount); // covered below
        
        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter++;  // NOT thread-safe! read-modify-write is not atomic
                }
                latch.countDown();
            }).start();
        }
        
        latch.await(); // wait for all threads to finish
        
        // Expected: 100 * 1000 = 100,000
        // Actual: somewhere between ~95,000 and 100,000 (varies each run!)
        System.out.println("Expected: " + (threadCount * incrementsPerThread));
        System.out.println("Actual:   " + counter);
        // Typical output: "Actual: 97,842" — data loss from race conditions!
    }
}
```

Run this five times and you'll get five different answers. That non-reproducibility is the hallmark of a race condition.

---

## 7.6 `synchronized`: Mutual Exclusion + Memory Barrier

`synchronized` solves all three concurrency problems at once:
1. **Atomicity:** Only one thread can hold the lock at a time — critical section executes atomically.
2. **Visibility:** On **unlock**, all writes are flushed to main memory. On **lock**, the thread reads fresh values from main memory (happens-before guarantee).
3. **Ordering:** Code inside a synchronized block cannot be reordered across lock boundaries by the JVM.

```java
public class SynchronizedCounter {
    private int counter = 0;
    private final Object lock = new Object(); // explicit lock object
    
    // Form 1: synchronized method — locks on 'this' (the instance)
    public synchronized void increment() {
        counter++;  // now safe: only one thread in this method at a time
    }
    
    // Form 2: synchronized block — more granular control
    public void incrementBlock() {
        // do non-shared work here...
        synchronized (this) {     // locks on 'this'
            counter++;
        }
        // non-shared work continues...
    }
    
    // Form 3: separate lock object — allows two independent locks on same object
    private final Object balanceLock = new Object();
    private final Object historyLock = new Object();
    private double balance;
    private List<String> history;
    
    public void deposit(double amount) {
        synchronized (balanceLock) {     // only blocks other balance operations
            balance += amount;
        }
        synchronized (historyLock) {     // only blocks other history operations
            history.add("+" + amount);   // can run concurrently with a balance read
        }
    }
    
    // Form 4: static synchronized — locks on the Class object
    private static int instanceCount = 0;
    
    public static synchronized void trackCreation() {
        instanceCount++;  // Class-level lock, shared across all instances
    }
    
    // Re-entrancy: a thread can re-enter a lock it ALREADY holds
    public synchronized void outerMethod() {
        innerMethod();  // this thread already holds the lock on 'this'
                        // Java's synchronized is REENTRANT — no deadlock here
    }
    
    public synchronized void innerMethod() {
        // This works because the thread calling outerMethod already has the lock
        // A non-reentrant lock would deadlock here
    }
    
    public int getCounter() {
        synchronized (this) {
            return counter;  // reading shared state also needs synchronization!
        }
    }
}

// Fix for the race condition demo:
public class FixedCounter {
    private int counter = 0;
    
    public synchronized void increment() { counter++; }
    public synchronized int getCounter() { return counter; }
    
    public static void main(String[] args) throws InterruptedException {
        FixedCounter fc = new FixedCounter();
        int threadCount = 100;
        int incrementsPerThread = 1000;
        
        CountDownLatch latch = new CountDownLatch(threadCount);
        for (int i = 0; i < threadCount; i++) {
            new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    fc.increment();  // synchronized — no more race condition
                }
                latch.countDown();
            }).start();
        }
        
        latch.await();
        System.out.println("Result: " + fc.getCounter()); // Always 100,000
    }
}
```

---

## 7.7 `volatile`: Visibility Only

`volatile` ensures that reads and writes to a variable go directly to main memory — bypassing CPU caches. It provides **visibility** but NOT **atomicity**.

```java
public class VolatileDemo {
    // Without volatile: JIT may optimize the loop by caching 'running' in a register
    // Other thread's write to 'running' would never be seen → infinite loop
    private volatile boolean running = true;
    
    public void start() {
        new Thread(() -> {
            System.out.println("Worker starting...");
            while (running) {    // volatile read: checks main memory every iteration
                doWork();
            }
            System.out.println("Worker stopped.");
        }).start();
    }
    
    public void stop() {
        running = false;  // volatile write: immediately visible to all threads
    }
    
    private void doWork() { /* some non-critical work */ }
    
    // WRONG use of volatile — counter++ is still not atomic!
    private volatile int count = 0;
    
    public void badIncrement() {
        count++;  // READ count (from memory), increment, WRITE back
                  // The gap between READ and WRITE is still a race condition window
                  // volatile makes the write visible, but doesn't prevent interleaving
    }
    
    // CORRECT: use AtomicInteger for compound operations
    // CORRECT: use volatile only for single, independent reads/writes
    
    // Perfect volatile use cases:
    // 1. Simple boolean flag (stop signals, initialization flags)
    // 2. Reference replacement (swapping an entire object reference atomically)
    //    volatile Map<K,V> cache; 
    //    cache = new HashMap<>(newData);  // atomic reference replacement
    // 3. Double-checked locking (see below)
}
```

### Double-Checked Locking Pattern (Classic volatile Use Case)

```java
// Singleton with lazy initialization — thread-safe, efficient
public class Singleton {
    // 'volatile' is CRITICAL here — without it, partially-constructed
    // objects can be observed by other threads due to instruction reordering
    private static volatile Singleton instance;
    
    private Singleton() { /* expensive initialization */ }
    
    public static Singleton getInstance() {
        if (instance == null) {                  // First check (no lock, fast path)
            synchronized (Singleton.class) {
                if (instance == null) {          // Second check (inside lock, safe)
                    instance = new Singleton();  // volatile write
                }
            }
        }
        return instance;  // volatile read
    }
}
// Without volatile, the JVM can reorder:
//   1. Allocate memory for Singleton
//   2. Assign reference to 'instance'   ← another thread sees non-null instance
//   3. Call constructor                 ← but construction not finished yet!
// volatile forces: allocate + construct first, THEN assign reference
```

---

## 7.8 Atomic Classes: Lock-Free Thread Safety

The `java.util.concurrent.atomic` package provides classes that use **CAS (Compare-And-Swap)** — a single hardware instruction that is atomically safe.

### How CAS Works

```
CAS(address, expectedValue, newValue):
   if (memory[address] == expectedValue) {
       memory[address] = newValue;
       return true;   // SUCCESS
   } else {
       return false;  // FAIL — someone else changed it; retry
   }
// This is a SINGLE CPU instruction — can't be interrupted between check and write
```

```java
import java.util.concurrent.atomic.*;

public class AtomicDemo {
    
    // AtomicInteger: thread-safe int operations
    private AtomicInteger counter = new AtomicInteger(0);
    
    public void increment() {
        counter.incrementAndGet();   // atomic equivalent of ++counter
        // or:
        counter.getAndIncrement();   // atomic equivalent of counter++
        counter.addAndGet(5);        // atomic counter += 5
    }
    
    public int getCount() {
        return counter.get();  // simple read (already visible)
    }
    
    // CAS directly — for custom atomic logic
    public boolean setIfLessThan(int threshold, int newValue) {
        int current;
        do {
            current = counter.get();
            if (current >= threshold) return false;
        } while (!counter.compareAndSet(current, newValue)); // retry if value changed
        return true;
    }
    
    // AtomicLong — same but for long values
    AtomicLong seqNo = new AtomicLong(0);
    public long nextSequenceNumber() { return seqNo.incrementAndGet(); }
    
    // AtomicReference — atomic object reference replacement
    AtomicReference<String> status = new AtomicReference<>("PENDING");
    
    public boolean transition(String from, String to) {
        return status.compareAndSet(from, to); // atomic: only updates if still 'from'
    }
    
    // AtomicStampedReference — solves ABA problem
    // ABA problem: thread reads value A, another changes A→B→A,
    // original thread's CAS succeeds even though value changed
    AtomicStampedReference<String> stamped = new AtomicStampedReference<>("initial", 0);
    
    public boolean updateSafely(String expected, String newVal, int expectedStamp) {
        return stamped.compareAndSet(expected, newVal, expectedStamp, expectedStamp + 1);
        // Version stamp prevents ABA: even if value is same, stamp changed
    }
    
    // LongAdder: better than AtomicLong under HIGH CONTENTION
    // Distributes updates across multiple internal cells → reduces CAS contention
    // Perfect for counters, but only getSum() aggregates — not for CAS logic
    LongAdder hitCounter = new LongAdder();
    
    public void recordHit() {
        hitCounter.increment();   // updates local cell — rarely contends
    }
    
    public long totalHits() {
        return hitCounter.sum();  // sums all cells — slightly more expensive than get()
    }
    // Use LongAdder for: high-throughput counters (metrics, stats)
    // Use AtomicLong for: when you need CAS / compareAndSet semantics
}
```

---

## 7.9 `ReentrantLock`: More Flexible Than synchronized

```java
import java.util.concurrent.locks.*;
import java.util.concurrent.*;

public class ReentrantLockDemo {
    private final ReentrantLock lock = new ReentrantLock();
    private int count = 0;
    
    // Basic lock/unlock — ALWAYS use finally to release!
    public void increment() {
        lock.lock();        // blocks until lock acquired
        try {
            count++;
        } finally {
            lock.unlock();  // ALWAYS release, even if exception thrown
        }
    }
    
    // tryLock — non-blocking attempt
    public boolean tryIncrement() {
        if (lock.tryLock()) {  // returns immediately: true if acquired, false if not
            try {
                count++;
                return true;
            } finally {
                lock.unlock();
            }
        }
        return false;  // lock was busy — caller decides what to do
    }
    
    // tryLock with timeout — wait up to N units for the lock
    public boolean tryIncrementWithTimeout() throws InterruptedException {
        if (lock.tryLock(100, TimeUnit.MILLISECONDS)) {
            try {
                count++;
                return true;
            } finally {
                lock.unlock();
            }
        }
        System.out.println("Timeout: could not acquire lock in 100ms");
        return false;
    }
    
    // Fair lock: longest-waiting thread gets the lock first
    // Prevents starvation but reduces throughput (disable if not needed)
    private final ReentrantLock fairLock = new ReentrantLock(true);
    
    // lockInterruptibly — can be interrupted while waiting for lock
    // Useful for implementing cancellable operations
    public void interruptibleIncrement() throws InterruptedException {
        lock.lockInterruptibly();  // throws InterruptedException if thread is interrupted
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }
    
    // Diagnostic methods
    public void printLockInfo() {
        System.out.println("Hold count: " + lock.getHoldCount()); // reentrant depth
        System.out.println("Queued threads: " + lock.getQueueLength()); // threads waiting
        System.out.println("Is locked: " + lock.isLocked());
        System.out.println("Locked by me: " + lock.isHeldByCurrentThread());
    }
}
```

### ReadWriteLock: Many Readers, One Writer

```java
public class ConcurrentCache<K, V> {
    private final Map<K, V> cache = new HashMap<>();
    private final ReadWriteLock rwLock = new ReentrantReadWriteLock();
    private final Lock readLock = rwLock.readLock();
    private final Lock writeLock = rwLock.writeLock();
    
    // Multiple threads can read simultaneously — great for read-heavy caches
    public V get(K key) {
        readLock.lock();
        try {
            return cache.get(key);
        } finally {
            readLock.unlock();
        }
    }
    
    // Only one thread can write at a time — and no readers while writing
    public void put(K key, V value) {
        writeLock.lock();
        try {
            cache.put(key, value);
        } finally {
            writeLock.unlock();
        }
    }
    
    public int size() {
        readLock.lock();
        try { return cache.size(); }
        finally { readLock.unlock(); }
    }
}

// StampedLock (Java 8+): even faster for read-heavy scenarios
// Supports "optimistic reads" — read without acquiring a lock, then validate
import java.util.concurrent.locks.StampedLock;

public class StampedPoint {
    private double x, y;
    private final StampedLock lock = new StampedLock();
    
    public void move(double dx, double dy) {
        long stamp = lock.writeLock();
        try { x += dx; y += dy; }
        finally { lock.unlockWrite(stamp); }
    }
    
    public double distanceFromOrigin() {
        long stamp = lock.tryOptimisticRead(); // no lock acquired — fast
        double cx = x, cy = y;
        if (!lock.validate(stamp)) {           // was there a write while we read?
            stamp = lock.readLock();           // fall back to proper read lock
            try { cx = x; cy = y; }
            finally { lock.unlockRead(stamp); }
        }
        return Math.hypot(cx, cy);
    }
}
```

---

## 7.10 Condition: Multiple Wait Queues

`Condition` provides per-lock wait queues, equivalent to multiple `wait()`/`notify()` sets. Classic use: bounded blocking queue.

```java
import java.util.concurrent.locks.*;

public class BoundedQueue<T> {
    private final Object[] items;
    private int head, tail, count;
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();   // "I'm waiting for space"
    private final Condition notEmpty = lock.newCondition();  // "I'm waiting for items"
    
    public BoundedQueue(int capacity) {
        items = new Object[capacity];
    }
    
    public void put(T item) throws InterruptedException {
        lock.lock();
        try {
            while (count == items.length) {
                notFull.await();    // release lock, suspend thread, re-acquire on signal
            }
            items[tail] = item;
            tail = (tail + 1) % items.length;
            count++;
            notEmpty.signal();      // wake one waiting consumer
        } finally {
            lock.unlock();
        }
    }
    
    @SuppressWarnings("unchecked")
    public T take() throws InterruptedException {
        lock.lock();
        try {
            while (count == 0) {
                notEmpty.await();   // wait until item available
            }
            T item = (T) items[head];
            items[head] = null;
            head = (head + 1) % items.length;
            count--;
            notFull.signal();       // wake one waiting producer
            return item;
        } finally {
            lock.unlock();
        }
    }
}
// Note: This is essentially what java.util.concurrent.ArrayBlockingQueue implements
```

---

## 7.11 Deadlock: Definition, Example, Prevention

A deadlock occurs when two or more threads are each waiting for a lock held by the other — a circular dependency with no way out.

### The Four Coffman Conditions (all must hold for deadlock):
1. **Mutual exclusion:** Resources can't be shared (locks are exclusive)
2. **Hold and wait:** Thread holds a lock while waiting for another
3. **No preemption:** Locks can't be forcibly taken
4. **Circular wait:** Thread A waits for B, B waits for A (or longer cycle)

```java
public class DeadlockDemo {
    private static final Object lockA = new Object();
    private static final Object lockB = new Object();
    
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            synchronized (lockA) {
                System.out.println("T1: acquired lockA");
                try { Thread.sleep(50); } catch (InterruptedException e) {}
                System.out.println("T1: waiting for lockB");
                synchronized (lockB) {  // BLOCKED: T2 holds lockB
                    System.out.println("T1: acquired lockB");
                }
            }
        }, "T1");
        
        Thread t2 = new Thread(() -> {
            synchronized (lockB) {
                System.out.println("T2: acquired lockB");
                try { Thread.sleep(50); } catch (InterruptedException e) {}
                System.out.println("T2: waiting for lockA");
                synchronized (lockA) {  // BLOCKED: T1 holds lockA
                    System.out.println("T2: acquired lockA");
                }
            }
        }, "T2");
        
        t1.start();
        t2.start();
        // DEADLOCK: T1 waits for lockB (held by T2), T2 waits for lockA (held by T1)
        // Program hangs forever — never prints "acquired lockB" or "acquired lockA"
    }
}
```

### Prevention Strategy 1: Consistent Lock Ordering

```java
// ALWAYS acquire locks in the same order across all threads
// If every thread acquires lockA before lockB, circular wait is impossible
public void safeOperation() {
    synchronized (lockA) {      // Both threads acquire A first...
        synchronized (lockB) {  // ...then B. No circular wait possible.
            // critical section
        }
    }
}
```

### Prevention Strategy 2: `tryLock()` with Timeout

```java
public boolean transferMoney(Account from, Account to, double amount) 
        throws InterruptedException {
    
    while (true) {  // retry loop
        if (from.lock.tryLock(50, TimeUnit.MILLISECONDS)) {
            try {
                if (to.lock.tryLock(50, TimeUnit.MILLISECONDS)) {
                    try {
                        from.debit(amount);
                        to.credit(amount);
                        return true;
                    } finally {
                        to.lock.unlock();
                    }
                }
            } finally {
                from.lock.unlock();
            }
        }
        // Failed to acquire both locks in 50ms — back off and retry
        Thread.sleep(1);  // brief pause before retry (reduces contention)
    }
}
```

### Detecting Deadlocks with jstack

```bash
# Get PID of running Java process
jps

# Print thread dump (shows deadlock info)
jstack <pid>

# In the output, look for:
# Found one Java-level deadlock:
# =============================
# "T1":
#   waiting to lock monitor 0x00007f... (object 0x..., a java.lang.Object)
#   which is held by "T2"
# "T2":
#   waiting to lock monitor 0x00007f... (object 0x..., a java.lang.Object)
#   which is held by "T1"
```

---

## 7.12 Livelock and Starvation

**Livelock:** Threads are not blocked but keep changing state in response to each other, making no actual progress. Like two people in a hallway both stepping the same direction to let the other pass.

```java
// Livelock example: both threads keep retrying but never succeed simultaneously
while (true) {
    if (!other.isAcquired()) {
        Thread.sleep(random.nextInt(100)); // "politely" wait
        // But other thread does the same thing at the same time → repeat forever
    }
}
// Fix: randomize back-off time, or use a coordinator
```

**Starvation:** A thread perpetually fails to acquire a resource because other threads always get it first. A low-priority thread starved by high-priority threads.

**Fix:** Use `new ReentrantLock(true)` (fair lock) to give longest-waiting thread priority, or explicitly manage priorities.

---

## 7.13 Java Memory Model: Happens-Before

The Java Memory Model (JMM) defines when one thread's actions are **guaranteed visible** to another. The key concept is **happens-before (HB)**: if action A HB action B, then B is guaranteed to see everything A did.

### The Happens-Before Rules:

```java
// 1. PROGRAM ORDER: within a single thread, each action HB the next
x = 1;  // HB
y = 2;  // this line

// 2. MONITOR LOCK: an unlock HB every subsequent lock of the same monitor
synchronized(lock) { counter = 5; }  // unlock HB →
synchronized(lock) { read counter; } // ← lock: GUARANTEED to see counter=5

// 3. VOLATILE WRITE/READ: volatile write HB subsequent reads of same variable
flag = true;   // volatile write HB →
if (flag) {}   // ← volatile read in another thread: GUARANTEED to see true

// 4. THREAD START: Thread.start() HB all actions in the started thread
x = 10;         // HB →
thread.start(); // HB →
                // all of thread's actions (they see x=10)

// 5. THREAD JOIN: all actions in thread HB the thread.join() return
thread.join();  // ← everything done by 'thread' HB this line completing
y = thread.result; // GUARANTEED to see thread's final state

// 6. TRANSITIVE: if A HB B and B HB C, then A HB C
```

```java
// Classic visibility bug (no HB relationship):
boolean ready = false;
int answer = 0;

Thread writer = new Thread(() -> {
    answer = 42;  // write to answer
    ready = true; // write to ready
    // WITHOUT volatile/sync, JVM may reorder: ready=true before answer=42!
    // Other thread may see ready=true but answer=0
});

Thread reader = new Thread(() -> {
    while (!ready) { /* spin */ }
    System.out.println(answer); // might print 0! No HB relationship guarantees answer
});

// Fix: make 'ready' volatile OR use synchronized OR use CountDownLatch
volatile boolean ready = false; // volatile write HB volatile read → answer guaranteed visible
```

---

## 7.14 ExecutorService: Thread Pool Management

Creating a new `Thread` for every task is expensive (OS thread creation takes ~1ms). `ExecutorService` manages a pool of reusable threads.

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ExecutorServiceDemo {
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        
        // ── Fixed Thread Pool ────────────────────────────────────────────────
        // N threads, tasks queue up when all busy
        // Good for: CPU-bound tasks (N = number of CPU cores)
        ExecutorService fixedPool = Executors.newFixedThreadPool(4);
        
        // ── Cached Thread Pool ───────────────────────────────────────────────
        // Creates new threads as needed, reuses idle ones
        // DANGEROUS in production: unbounded — can create millions of threads under load
        ExecutorService cachedPool = Executors.newCachedThreadPool();
        
        // ── Single Thread Executor ───────────────────────────────────────────
        // One thread, tasks run sequentially in submission order
        // Good for: ordered background processing
        ExecutorService singleThread = Executors.newSingleThreadExecutor();
        
        // ── Scheduled Executor ───────────────────────────────────────────────
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
        // Run after delay:
        scheduler.schedule(() -> System.out.println("Delayed"), 5, TimeUnit.SECONDS);
        // Run periodically:
        scheduler.scheduleAtFixedRate(
            () -> System.out.println("Periodic"), 0, 1, TimeUnit.SECONDS);
        
        // ── Submit tasks ─────────────────────────────────────────────────────
        
        // submit(Runnable): returns Future<?> (no return value)
        Future<?> future1 = fixedPool.submit(() -> {
            System.out.println("Task running in: " + Thread.currentThread().getName());
        });
        future1.get(); // block until done (returns null for Runnable)
        
        // submit(Callable<T>): returns Future<T> (has return value)
        Future<Integer> future2 = fixedPool.submit(() -> {
            Thread.sleep(100);
            return 42;
        });
        int result = future2.get();   // blocks until result available
        // future2.get(500, TimeUnit.MILLISECONDS); // with timeout
        future2.cancel(true);         // try to cancel (interrupt if running)
        
        // invokeAll: submit multiple tasks, wait for all to complete
        List<Callable<String>> tasks = List.of(
            () -> { Thread.sleep(100); return "task1"; },
            () -> { Thread.sleep(200); return "task2"; },
            () -> "task3"
        );
        List<Future<String>> futures = fixedPool.invokeAll(tasks); // blocks until all done
        for (Future<String> f : futures) {
            System.out.println(f.get()); // each get() is instant (already done)
        }
        
        // invokeAny: submit multiple tasks, return first result
        String first = fixedPool.invokeAny(tasks); // blocks until one completes
        System.out.println("First result: " + first);
        
        // ── ThreadPoolExecutor: full control ─────────────────────────────────
        ThreadPoolExecutor customPool = new ThreadPoolExecutor(
            4,                               // corePoolSize: min threads to keep alive
            8,                               // maximumPoolSize: max threads allowed
            60L, TimeUnit.SECONDS,           // keepAliveTime: how long idle threads over core survive
            new LinkedBlockingQueue<>(1000), // workQueue: bounded queue (prevents OOM)
            new ThreadFactory() {            // custom thread names for debugging
                AtomicInteger count = new AtomicInteger(0);
                @Override
                public Thread newThread(Runnable r) {
                    return new Thread(r, "order-processor-" + count.incrementAndGet());
                }
            },
            new ThreadPoolExecutor.CallerRunsPolicy() // rejection policy when queue full
            // AbortPolicy:       throw RejectedExecutionException (default)
            // CallerRunsPolicy:  caller thread runs the task (natural backpressure)
            // DiscardPolicy:     silently discard
            // DiscardOldestPolicy: discard oldest queued task
        );
        
        // ── Shutdown ─────────────────────────────────────────────────────────
        // ALWAYS shutdown executors (in a finally block or via try-with-resources)
        fixedPool.shutdown();               // no new tasks accepted; existing tasks finish
        fixedPool.awaitTermination(30, TimeUnit.SECONDS); // wait for all to complete
        
        // or:
        fixedPool.shutdownNow();            // interrupt running tasks, return queued ones
        
        // Java 19+ try-with-resources style:
        try (ExecutorService pool = Executors.newFixedThreadPool(4)) {
            pool.submit(() -> System.out.println("Auto-shutdown when block exits"));
        } // pool.close() called automatically, waits for tasks to complete
    }
}
```

---

## 7.15 CompletableFuture: Async Without Callbacks

`CompletableFuture` is Java's answer to JavaScript Promises — composable, non-blocking async computation.

```java
import java.util.concurrent.CompletableFuture;

public class CompletableFutureDemo {
    
    record User(Long id, String name) {}
    record Order(Long userId, String item, double total) {}
    record Recommendation(String item) {}
    
    // Simulated async services (in real code, these call HTTP APIs, databases, etc.)
    static CompletableFuture<User> fetchUser(Long userId) {
        return CompletableFuture.supplyAsync(() -> {
            simulateLatency(100); // simulate 100ms DB call
            return new User(userId, "Alice");
        });
    }
    
    static CompletableFuture<List<Order>> fetchOrders(Long userId) {
        return CompletableFuture.supplyAsync(() -> {
            simulateLatency(150);
            return List.of(new Order(userId, "Laptop", 999.99));
        });
    }
    
    static CompletableFuture<Recommendation> fetchRecommendation(Long userId) {
        return CompletableFuture.supplyAsync(() -> {
            simulateLatency(80);
            return new Recommendation("Mechanical Keyboard");
        });
    }
    
    public static void main(String[] args) throws Exception {
        
        // ── supplyAsync: start async computation ────────────────────────────
        CompletableFuture<String> cf = CompletableFuture.supplyAsync(() -> {
            simulateLatency(200);
            return "Hello from async";
        });
        
        // ── thenApply: transform result (sync, on same thread) ──────────────
        CompletableFuture<Integer> length = cf.thenApply(String::length);
        
        // ── thenApplyAsync: transform on a different thread ─────────────────
        CompletableFuture<String> upper = cf.thenApplyAsync(String::toUpperCase);
        
        // ── thenAccept: consume result (no return value) ────────────────────
        cf.thenAccept(s -> System.out.println("Got: " + s));
        
        // ── thenRun: run action after completion (no access to result) ──────
        cf.thenRun(() -> System.out.println("Completed!"));
        
        // ── thenCompose: flatMap — when next step is also async ─────────────
        // WRONG: thenApply(fetchOrders) returns CompletableFuture<CompletableFuture<Orders>>
        // CORRECT: thenCompose unwraps the nested future
        CompletableFuture<List<Order>> ordersForUser = fetchUser(1L)
            .thenCompose(user -> fetchOrders(user.id())); // user → Future<Orders>
        
        // ── PARALLEL EXECUTION: allOf ────────────────────────────────────────
        // Fetch user, orders, AND recommendations all at the same time
        // Total time ≈ max(100ms, 150ms, 80ms) = 150ms  (vs 330ms sequential)
        long start = System.currentTimeMillis();
        
        CompletableFuture<User> userFuture = fetchUser(1L);
        CompletableFuture<List<Order>> ordersFuture = fetchOrders(1L);
        CompletableFuture<Recommendation> recFuture = fetchRecommendation(1L);
        
        CompletableFuture<Void> allDone = CompletableFuture.allOf(
            userFuture, ordersFuture, recFuture
        ); // fires when ALL three complete
        
        allDone.thenRun(() -> {
            User user = userFuture.join();             // join() = get() but unchecked
            List<Order> orders = ordersFuture.join();
            Recommendation rec = recFuture.join();
            
            System.out.printf("User: %s, Orders: %d, Recommendation: %s%n",
                user.name(), orders.size(), rec.item());
        }).get(); // block main thread until done
        
        System.out.println("Parallel time: " + (System.currentTimeMillis() - start) + "ms");
        // ~150ms, not 330ms
        
        // ── anyOf: return first result ───────────────────────────────────────
        CompletableFuture<Object> fastest = CompletableFuture.anyOf(
            CompletableFuture.supplyAsync(() -> { simulateLatency(300); return "slow"; }),
            CompletableFuture.supplyAsync(() -> { simulateLatency(100); return "fast"; }),
            CompletableFuture.supplyAsync(() -> { simulateLatency(200); return "medium"; })
        );
        System.out.println("Fastest result: " + fastest.get()); // "fast"
        
        // ── ERROR HANDLING ───────────────────────────────────────────────────
        CompletableFuture<String> risky = CompletableFuture.supplyAsync(() -> {
            if (Math.random() > 0.5) throw new RuntimeException("Service unavailable");
            return "OK";
        });
        
        // exceptionally: handle exception, provide fallback
        CompletableFuture<String> recovered = risky
            .exceptionally(ex -> "FALLBACK: " + ex.getMessage());
        
        // handle: handle both success and failure in one handler
        CompletableFuture<String> handled = risky
            .handle((result, ex) -> {
                if (ex != null) return "Error: " + ex.getMessage();
                return "Success: " + result;
            });
        
        // whenComplete: side effect on completion (doesn't change result)
        risky.whenComplete((result, ex) -> {
            if (ex != null) System.err.println("Failed: " + ex.getMessage());
            else System.out.println("Succeeded: " + result);
        });
        
        // ── Chaining a real workflow ─────────────────────────────────────────
        CompletableFuture<String> workflow = CompletableFuture
            .supplyAsync(() -> { simulateLatency(50); return "RAW_DATA"; })
            .thenApply(data -> data.toLowerCase())            // transform
            .thenApply(data -> "processed: " + data)         // transform again
            .thenApplyAsync(data -> data.toUpperCase())       // on another thread
            .exceptionally(ex -> "fallback")                  // error recovery
            .thenCompose(data ->                              // async next step
                CompletableFuture.supplyAsync(() -> "FINAL: " + data));
        
        System.out.println(workflow.get()); // FINAL: PROCESSED: raw_data
    }
    
    static void simulateLatency(long ms) {
        try { Thread.sleep(ms); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    }
}
```

---

## 7.16 Virtual Threads (Java 21): Project Loom

Traditional Java threads map 1:1 to OS threads. OS threads are heavy: ~1MB of stack memory each, limited to tens of thousands per JVM. Blocking I/O ties up an OS thread for the entire duration.

**Virtual threads** are JVM-managed lightweight threads. The JVM multiplexes thousands of virtual threads onto a small pool of OS "carrier" threads:

```
Without virtual threads:
  Request 1 → OS Thread 1 [waits for DB... 200ms... response] → return thread to pool
  Request 2 → OS Thread 2 [waits for HTTP... 300ms... response]
  ...with 500 concurrent requests: need 500 OS threads (~500MB RAM)

With virtual threads:
  Request 1 → Virtual Thread 1 [calls DB, YIELDS to carrier thread]
  Carrier Thread ← picks up Request 2 → Virtual Thread 2 [calls HTTP, YIELDS]
  Carrier Thread ← picks up Request 3 → ...
  DB responds → Virtual Thread 1 RESUMED on any available carrier
  ...with 500 concurrent requests: 500 virtual threads, ~8 OS carrier threads
```

```java
import java.util.concurrent.*;

public class VirtualThreadDemo {
    
    public static void main(String[] args) throws Exception {
        
        // Create a single virtual thread
        Thread vt = Thread.ofVirtual()
            .name("my-virtual-thread")
            .start(() -> {
                System.out.println("Running on: " + Thread.currentThread());
                System.out.println("Is virtual: " + Thread.currentThread().isVirtual());
            });
        vt.join();
        
        // Virtual thread per task executor — ideal for I/O-bound work
        try (ExecutorService vExecutor = Executors.newVirtualThreadPerTaskExecutor()) {
            // Each task gets its OWN virtual thread — no pooling needed!
            // (Virtual threads are cheap enough to create per-task)
            List<Future<String>> futures = new ArrayList<>();
            
            for (int i = 0; i < 10_000; i++) {
                final int id = i;
                futures.add(vExecutor.submit(() -> {
                    // Simulates I/O — virtual thread YIELDS during sleep/block
                    Thread.sleep(100);  // non-blocking for carrier thread
                    return "result-" + id;
                }));
            }
            // 10,000 concurrent tasks, but only ~handful of OS threads
            // Total time ≈ 100ms (all run concurrently) not 1,000,000ms
            
            int count = 0;
            for (Future<String> f : futures) { f.get(); count++; }
            System.out.println("Completed: " + count); // 10000
        }
        
        // Structured concurrency (Java 21 preview, 22 final):
        // Group related tasks, cancel all if one fails
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            Subtask<String> task1 = scope.fork(() -> fetchFromService1());
            Subtask<String> task2 = scope.fork(() -> fetchFromService2());
            
            scope.join();           // wait for all
            scope.throwIfFailed();  // throw if any failed (cancels remaining)
            
            return task1.get() + task2.get(); // both available
        }
    }
    
    // When to use virtual threads:
    // ✓ I/O-bound work: HTTP calls, DB queries, file operations
    // ✓ High-concurrency servers: each request gets its own virtual thread
    // ✓ Replacing reactive/async code (WebFlux, RxJava) for I/O workloads
    
    // When NOT to use virtual threads:
    // ✗ CPU-bound work: virtual threads offer no benefit (still one computation at a time per core)
    // ✗ Code holding monitors during I/O: synchronized blocks "pin" virtual threads to carrier threads
    //   Use ReentrantLock instead (virtual-thread-friendly)
    
    static String fetchFromService1() throws Exception { Thread.sleep(100); return "service1"; }
    static String fetchFromService2() throws Exception { Thread.sleep(150); return "service2"; }
}
```

---

## 7.17 ConcurrentHashMap in Depth

`ConcurrentHashMap` is thread-safe without locking the entire map. Instead it uses **CAS for reads** and **per-bucket synchronized blocks for writes**:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class ConcurrentHashMapDemo {
    
    public static void main(String[] args) {
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        
        // Thread-safe put/get
        map.put("count", 0);
        map.get("count");
        
        // computeIfAbsent: atomic check-then-create (critical for caches/registries)
        // The lambda is called at most once per key, even with concurrent threads
        map.computeIfAbsent("newKey", k -> expensiveCompute(k));
        
        // merge: atomic read-modify-write
        // If key absent: put value. If present: apply merge function.
        map.merge("count", 1, Integer::sum);  // count++ but thread-safe
        
        // compute: atomic update (can return null to remove)
        map.compute("count", (k, v) -> v == null ? 1 : v + 1);
        
        // Thread-safe word frequency counter (compare to HashMap — needs synchronization)
        ConcurrentHashMap<String, Long> wordFreq = new ConcurrentHashMap<>();
        String[] words = {"the", "cat", "the", "mat", "the"};
        
        for (String word : words) {
            wordFreq.merge(word, 1L, Long::sum);
        }
        System.out.println(wordFreq); // {the=3, cat=1, mat=1}
        
        // forEach, reduce, search — parallel bulk operations
        wordFreq.forEach(2, (k, v) ->  // parallelismThreshold=2: parallelize if > 2 entries
            System.out.println(k + "=" + v));
        
        long totalWords = wordFreq.reduceValues(1, Long::sum); // 5
        String highFreqWord = wordFreq.search(1, (k, v) -> v > 2 ? k : null); // "the"
        
        // computeIfAbsent for building concurrent caches:
        ConcurrentHashMap<Long, User> userCache = new ConcurrentHashMap<>();
        
        User getOrLoadUser(Long id) {
            return userCache.computeIfAbsent(id, userId -> {
                // This lambda called ONCE per userId even with 100 concurrent threads
                return loadFromDatabase(userId);
            });
        }
    }
    
    static Integer expensiveCompute(String k) { return k.hashCode(); }
    static User loadFromDatabase(Long id) { return new User(id, "User" + id); }
    record User(Long id, String name) {}
}
```

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "What is the difference between synchronized, volatile, and AtomicInteger?"**

**SDE-2 Answer:** All three address different aspects of thread safety. `synchronized` provides mutual exclusion (only one thread executes the block at a time) and a full memory barrier on both acquire and release, solving visibility, atomicity, and ordering simultaneously. It uses a monitor lock — threads not holding the lock block and wait. It's the most powerful but most heavyweight. `volatile` provides only a visibility guarantee — reads always go to main memory, writes are immediately visible to all threads. It does NOT provide atomicity. `counter++` is three operations (read, increment, write) and is still a race condition even on a `volatile` variable. Use `volatile` for single-variable flags, reference replacements, or the published reference in double-checked locking. `AtomicInteger` (and other atomic classes) provides lock-free, hardware-supported atomic operations using CAS (compare-and-swap) instructions. It's faster than `synchronized` under low-to-moderate contention because it avoids OS-level thread blocking. Use `AtomicInteger` for counters and `AtomicReference` for atomic reference updates without needing a full synchronized block. Choose: `volatile` for simple flags, `AtomicXxx` for counters and CAS patterns, `synchronized`/`ReentrantLock` for compound operations involving multiple variables.

**Q2: "Explain CompletableFuture and how you would use it to make parallel API calls."**

**SDE-2 Answer:** `CompletableFuture` is Java's composable async primitive. Unlike raw `Future`, it supports chaining transformations (`thenApply` for sync transforms, `thenApplyAsync` for async), sequencing dependent async calls (`thenCompose` / flatMap), error recovery (`exceptionally`, `handle`), and fork-join patterns. To make parallel API calls, I use `CompletableFuture.supplyAsync()` to launch each call concurrently, then `CompletableFuture.allOf(cf1, cf2, cf3)` to wait for all to complete. After `allOf` resolves, I call `.join()` on each individual future to retrieve results. For example, fetching a user profile, their orders, and their recommendations simultaneously: three `supplyAsync` calls start all three HTTP requests in parallel; `allOf` waits for the slowest; then I combine the results. This reduces latency from the sum of all call times to the max — if the three calls take 100ms, 150ms, and 80ms, sequential would be 330ms; parallel is 150ms. I'd typically provide a custom `ExecutorService` to `supplyAsync` to control the thread pool rather than using the common fork-join pool, which is better reserved for CPU-bound work.

**Q3: "What are virtual threads and when should you use them?"**

**SDE-2 Answer:** Virtual threads (Project Loom, finalized in Java 21) are JVM-managed lightweight threads that do not map 1:1 to OS threads. The JVM maintains a small pool of OS "carrier" threads and multiplexes thousands of virtual threads onto them. When a virtual thread performs a blocking operation (I/O, sleep, lock acquisition), it automatically unmounts from its carrier thread, which is then free to run other virtual threads. When the blocking operation completes, the virtual thread is rescheduled. The benefit is massive concurrency with low overhead — you can create a million virtual threads where creating a million OS threads would require gigabytes of RAM and crash the OS scheduler. Use virtual threads for I/O-bound, high-concurrency workloads: HTTP servers where each request gets its own thread, database calls, service-to-service communication. The key win is code simplicity — you write straightforward blocking code (simple to reason about) and get the concurrency benefits that previously required complex reactive/async frameworks like WebFlux. Don't use for CPU-bound work (no benefit over platform threads) and avoid `synchronized` blocks holding monitors during I/O (they "pin" virtual threads to carriers — use `ReentrantLock` instead).

# CHAPTER 8: Testing Java Applications

## 8.1 Why Testing Is a First-Class SDE-2 Skill

In interviews, the difference between a junior and SDE-2 candidate is often visible in how they discuss testing. SDE-2 engineers are expected to write tests as part of "done," understand test doubles (mocks, stubs, spies), and reason about what makes a test valuable versus brittle. Your GitHub portfolio's test coverage is often the first thing a hiring manager checks.

---

## 8.2 The Test Pyramid

```
                    ╱╲
                   ╱  ╲
                  ╱ E2E ╲              FEW: slow, expensive, brittle
                 ╱──────╲              Tests entire system through UI/API
                ╱        ╲             Run in CI before deploy, not on every commit
               ╱INTEGRATION╲           SOME: tests interaction between components
              ╱──────────────╲         Database, message queue, external API (often mocked)
             ╱                ╲
            ╱   UNIT TESTS     ╲       MANY: fast, isolated, run on every save
           ╱────────────────────╲      Test a single class/method in isolation
          ──────────────────────────
          
Unit tests:        milliseconds each, thousands in a suite, run constantly
Integration tests:  seconds each, hundreds in a suite, run before commit/PR
E2E tests:          minutes each, dozens in a suite, run before deploy
```

---

## 8.3 JUnit 5: Complete Reference

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import static org.junit.jupiter.api.Assertions.*;

class OrderCalculatorTest {
    
    private OrderCalculator calculator;
    
    // Runs ONCE before all tests in this class (must be static unless using PER_CLASS lifecycle)
    @BeforeAll
    static void setUpClass() {
        System.out.println("Setting up test class — runs once");
    }
    
    // Runs before EVERY test method — fresh state for each test
    @BeforeEach
    void setUp() {
        calculator = new OrderCalculator();
        System.out.println("Setting up before each test");
    }
    
    // Runs after EVERY test method
    @AfterEach
    void tearDown() {
        calculator = null;
        System.out.println("Cleaning up after each test");
    }
    
    // Runs ONCE after all tests
    @AfterAll
    static void tearDownClass() {
        System.out.println("Tearing down test class — runs once");
    }
    
    @Test
    @DisplayName("Calculating total with no discount should return base price")
    void calculateTotal_noDiscount_returnsBasePrice() {
        double result = calculator.calculateTotal(100.0, 0.0);
        assertEquals(100.0, result, 0.001); // delta for floating-point comparison
    }
    
    @Test
    void calculateTotal_withDiscount_appliesCorrectly() {
        double result = calculator.calculateTotal(100.0, 0.1); // 10% discount
        assertEquals(90.0, result, 0.001);
    }
    
    @Test
    void calculateTotal_negativePrice_throwsException() {
        // Assert that an exception is thrown
        IllegalArgumentException exception = assertThrows(
            IllegalArgumentException.class,
            () -> calculator.calculateTotal(-100.0, 0.0)
        );
        assertEquals("Price cannot be negative", exception.getMessage());
    }
    
    @Test
    @Disabled("Flaky due to timing issue — JIRA-1234")
    void unstableTest() {
        // Temporarily disabled, shows up as skipped in test report
    }
    
    // ── PARAMETERIZED TESTS — run same test logic with multiple inputs ────────
    
    @ParameterizedTest
    @ValueSource(doubles = {0.0, 50.0, 100.0, 999.99})
    void calculateTotal_variousPrices_neverNegative(double price) {
        double result = calculator.calculateTotal(price, 0.0);
        assertTrue(result >= 0);
    }
    
    @ParameterizedTest
    @CsvSource({
        "100.0, 0.0, 100.0",   // price, discount, expected
        "100.0, 0.5, 50.0",
        "200.0, 0.25, 150.0",
        "50.0, 1.0, 0.0"
    })
    void calculateTotal_multipleCases(double price, double discount, double expected) {
        assertEquals(expected, calculator.calculateTotal(price, discount), 0.001);
    }
    
    // ── NESTED TEST CLASSES — group related tests, share setup ────────────────
    
    @Nested
    @DisplayName("When applying bulk discounts")
    class BulkDiscountTests {
        
        @BeforeEach
        void setupBulkContext() {
            calculator.setBulkMode(true);
        }
        
        @Test
        void appliesExtraDiscountOverThreshold() {
            double result = calculator.calculateTotal(1000.0, 0.1);
            assertTrue(result < 900.0); // bulk discount should apply on top
        }
    }
}

class OrderCalculator {
    private boolean bulkMode = false;
    
    public double calculateTotal(double price, double discountRate) {
        if (price < 0) throw new IllegalArgumentException("Price cannot be negative");
        double total = price * (1 - discountRate);
        if (bulkMode && price > 500) total *= 0.95; // extra 5% off bulk orders
        return total;
    }
    
    public void setBulkMode(boolean bulkMode) { this.bulkMode = bulkMode; }
}
```

---

## 8.4 AssertJ: Fluent Assertions

AssertJ provides a much more readable assertion API than raw JUnit assertions:

```java
import static org.assertj.core.api.Assertions.*;
import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Optional;

class AssertJDemo {
    
    @Test
    void demonstrateAssertJ() {
        // Basic assertions — fluent, chainable, readable
        String name = "Surya";
        assertThat(name).isEqualTo("Surya");
        assertThat(name).isNotNull();
        assertThat(name).startsWith("Sur").endsWith("ya").hasSize(5);
        assertThat(name).containsIgnoringCase("SURYA");
        
        // Numeric assertions
        int score = 85;
        assertThat(score).isGreaterThan(80).isLessThan(100).isBetween(80, 90);
        assertThat(score).isPositive().isNotZero();
        
        // Collection assertions
        List<String> names = List.of("Alice", "Bob", "Charlie");
        assertThat(names)
            .hasSize(3)
            .contains("Alice", "Bob")
            .doesNotContain("Dave")
            .containsExactly("Alice", "Bob", "Charlie")  // exact order matters
            .containsExactlyInAnyOrder("Charlie", "Alice", "Bob"); // order doesn't matter
        
        // Filtering and extracting in assertions
        record Employee(String name, double salary) {}
        List<Employee> employees = List.of(
            new Employee("Alice", 90000),
            new Employee("Bob", 70000)
        );
        
        assertThat(employees)
            .extracting(Employee::name)
            .containsExactly("Alice", "Bob");
        
        assertThat(employees)
            .filteredOn(e -> e.salary() > 80000)
            .hasSize(1)
            .extracting(Employee::name)
            .containsExactly("Alice");
        
        // Optional assertions
        Optional<String> opt = Optional.of("present");
        assertThat(opt).isPresent().contains("present");
        
        Optional<String> empty = Optional.empty();
        assertThat(empty).isEmpty();
        
        // Exception assertions — fluent and informative
        assertThatThrownBy(() -> {
            throw new IllegalStateException("Account is closed");
        })
        .isInstanceOf(IllegalStateException.class)
        .hasMessageContaining("closed")
        .hasMessage("Account is closed");
        
        // Object property assertions
        Employee alice = new Employee("Alice", 90000);
        assertThat(alice)
            .extracting(Employee::name, Employee::salary)
            .containsExactly("Alice", 90000.0);
        
        // Soft assertions — collect ALL failures, don't stop at first
        org.assertj.core.api.SoftAssertions softly = new org.assertj.core.api.SoftAssertions();
        softly.assertThat(name).isEqualTo("WrongName");      // fails but doesn't stop
        softly.assertThat(score).isEqualTo(999);             // fails but doesn't stop
        softly.assertAll(); // reports BOTH failures together
    }
}
```

---

## 8.5 Mockito: Test Doubles

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.*;

interface OrderRepository {
    Optional<Order> findById(Long id);
    Order save(Order order);
}

interface PaymentService {
    boolean charge(String cardToken, double amount);
}

record Order(Long id, double amount, String status) {}

class OrderService {
    private final OrderRepository repository;
    private final PaymentService paymentService;
    
    public OrderService(OrderRepository repository, PaymentService paymentService) {
        this.repository = repository;
        this.paymentService = paymentService;
    }
    
    public Order confirmOrder(Long orderId, String cardToken) {
        Order order = repository.findById(orderId)
            .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
        
        boolean charged = paymentService.charge(cardToken, order.amount());
        if (!charged) {
            throw new RuntimeException("Payment failed for order: " + orderId);
        }
        
        Order confirmed = new Order(order.id(), order.amount(), "CONFIRMED");
        return repository.save(confirmed);
    }
}

@ExtendWith(MockitoExtension.class)  // enables @Mock, @InjectMocks annotations
class OrderServiceTest {
    
    @Mock                          // creates a fully fake OrderRepository — no real implementation
    private OrderRepository repository;
    
    @Mock
    private PaymentService paymentService;
    
    @InjectMocks                   // creates OrderService, injecting the @Mock fields above
    private OrderService orderService;
    
    @Captor                        // captures arguments passed to mock methods for inspection
    private ArgumentCaptor<Order> orderCaptor;
    
    @Test
    void confirmOrder_paymentSucceeds_returnsConfirmedOrder() {
        // ARRANGE: define mock behavior with when().thenReturn()
        Order pendingOrder = new Order(1L, 99.99, "PENDING");
        when(repository.findById(1L)).thenReturn(Optional.of(pendingOrder));
        when(paymentService.charge("tok_123", 99.99)).thenReturn(true);
        when(repository.save(any(Order.class))).thenAnswer(inv -> inv.getArgument(0));
        
        // ACT
        Order result = orderService.confirmOrder(1L, "tok_123");
        
        // ASSERT
        assertThat(result.status()).isEqualTo("CONFIRMED");
        
        // VERIFY: assert that specific methods were called with specific arguments
        verify(repository).findById(1L);
        verify(paymentService).charge("tok_123", 99.99);
        verify(repository).save(orderCaptor.capture());
        
        Order savedOrder = orderCaptor.getValue();
        assertThat(savedOrder.status()).isEqualTo("CONFIRMED");
        assertThat(savedOrder.id()).isEqualTo(1L);
    }
    
    @Test
    void confirmOrder_orderNotFound_throwsException() {
        when(repository.findById(999L)).thenReturn(Optional.empty());
        
        assertThatThrownBy(() -> orderService.confirmOrder(999L, "tok_123"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Order not found");
        
        // verify payment was NEVER attempted — important business logic check
        verifyNoInteractions(paymentService);
    }
    
    @Test
    void confirmOrder_paymentFails_throwsException() {
        Order pendingOrder = new Order(1L, 99.99, "PENDING");
        when(repository.findById(1L)).thenReturn(Optional.of(pendingOrder));
        when(paymentService.charge(anyString(), anyDouble())).thenReturn(false);
        
        assertThatThrownBy(() -> orderService.confirmOrder(1L, "tok_123"))
            .isInstanceOf(RuntimeException.class)
            .hasMessageContaining("Payment failed");
        
        // verify save() was NEVER called since payment failed
        verify(repository, never()).save(any());
    }
    
    @Test
    void demonstrateThrowingFromMock() {
        when(repository.findById(anyLong()))
            .thenThrow(new RuntimeException("Database connection lost"));
        
        assertThatThrownBy(() -> orderService.confirmOrder(1L, "tok"))
            .isInstanceOf(RuntimeException.class)
            .hasMessageContaining("Database connection lost");
    }
    
    @Test
    void demonstrateVerifyTimes() {
        Order pendingOrder = new Order(1L, 99.99, "PENDING");
        when(repository.findById(1L)).thenReturn(Optional.of(pendingOrder));
        when(paymentService.charge(anyString(), anyDouble())).thenReturn(true);
        when(repository.save(any())).thenReturn(pendingOrder);
        
        orderService.confirmOrder(1L, "tok_123");
        
        verify(repository, times(1)).findById(1L);     // exactly once
        verify(paymentService, atLeastOnce()).charge(anyString(), anyDouble());
        verify(repository, atMost(1)).save(any());
        verifyNoMoreInteractions(paymentService);        // no OTHER calls beyond verified ones
    }
}
```

### @Mock vs @Spy

```java
class MockVsSpyDemo {
    
    @Test
    void mockVsSpy() {
        // @Mock: COMPLETELY fake — all methods return default values unless stubbed
        List<String> mockList = mock(List.class);
        System.out.println(mockList.size());     // 0 (default, not real ArrayList behavior)
        mockList.add("item");                     // doesn't actually add — it's fake!
        System.out.println(mockList.size());      // still 0 — add() was never "really" called
        
        // @Spy: wraps a REAL object — calls real methods UNLESS explicitly stubbed
        List<String> spyList = spy(new ArrayList<>());
        spyList.add("item");                       // REALLY adds to the underlying ArrayList
        System.out.println(spyList.size());        // 1 — real behavior!
        
        // You CAN selectively override spy behavior
        doReturn(100).when(spyList).size();        // override just size()
        System.out.println(spyList.size());        // 100 (stubbed)
        spyList.add("another");                    // still really adds
        
        // When to use which:
        // @Mock: testing units in isolation — fake all dependencies
        // @Spy: when you need MOSTLY real behavior with ONE method overridden
        //       (e.g., spying on a real service but stubbing one expensive external call)
    }
}
```

---

## 8.6 Test-Driven Development: Red → Green → Refactor

```java
// STEP 1: RED — write a failing test FIRST, before any implementation
class PasswordValidatorTest {
    @Test
    void isValid_shortPassword_returnsFalse() {
        PasswordValidator validator = new PasswordValidator();
        assertThat(validator.isValid("abc")).isFalse();
        // FAILS to compile: PasswordValidator doesn't exist yet!
    }
}

// STEP 2: GREEN — write the MINIMUM code to make the test pass
class PasswordValidator {
    public boolean isValid(String password) {
        return password.length() >= 8;  // simplest thing that could possibly work
    }
}
// Test now passes (assuming "abc".length() < 8)

// STEP 3: Add more test cases (RED again)
@Test
void isValid_noDigits_returnsFalse() {
    PasswordValidator validator = new PasswordValidator();
    assertThat(validator.isValid("abcdefgh")).isFalse(); // FAILS — current impl doesn't check digits
}

// STEP 4: GREEN — extend implementation to pass the new test
class PasswordValidator {
    public boolean isValid(String password) {
        if (password.length() < 8) return false;
        return password.chars().anyMatch(Character::isDigit);
    }
}

// STEP 5: REFACTOR — clean up while keeping tests green
class PasswordValidator {
    private static final int MIN_LENGTH = 8;
    
    public boolean isValid(String password) {
        return hasMinimumLength(password) && hasDigit(password);
    }
    
    private boolean hasMinimumLength(String password) {
        return password.length() >= MIN_LENGTH;
    }
    
    private boolean hasDigit(String password) {
        return password.chars().anyMatch(Character::isDigit);
    }
}
// Run tests again — still green. Refactor was safe because tests caught any regression.

// TDD benefits: forces you to think about the API/contract before implementation,
// guarantees test coverage (you can't write untested code), gives instant feedback,
// and produces a regression suite as a side effect of development.
```

---

## 8.7 Code Coverage with JaCoCo

```xml
<!-- pom.xml — Maven configuration -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
        <execution>
            <id>check</id>
            <goals><goal>check</goal></goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>  <!-- fail build if below 80% -->
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

```bash
# Run tests and generate coverage report
mvn clean test jacoco:report

# Report generated at: target/site/jacoco/index.html
# Open in browser to see line-by-line coverage with green/red highlighting

# Enforce minimum coverage (fails build if below threshold)
mvn clean verify
```

**80% is a common industry minimum, but coverage percentage alone is misleading.** A test that calls a method without asserting anything meaningful "covers" the line but tests nothing. Focus on testing business logic, edge cases, and error paths — not on hitting an arbitrary percentage. Coverage is a floor, not a target.

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "What is the difference between @Mock and @Spy in Mockito?"**

**SDE-2 Answer:** `@Mock` creates a completely fake object — none of its real methods execute. All method calls return default values (0, null, false, empty collections) unless explicitly stubbed with `when().thenReturn()`. It's used to fully isolate the class under test from its dependencies. `@Spy` wraps a real object instance — by default, calling a method on a spy executes the REAL implementation. You can selectively override specific method behaviors using `doReturn().when()` syntax (not `when().thenReturn()`, which actually invokes the real method first on a spy, causing issues for void or side-effecting methods). Use `@Mock` when you want to isolate the unit under test from all collaborators — the standard approach for unit tests. Use `@Spy` when you need mostly-real behavior but want to override one specific interaction, such as stubbing out a slow network call within an otherwise-real service object. In most well-designed test suites, `@Mock` should dominate — heavy use of `@Spy` can indicate the class under test has too many responsibilities mixed together.

**Q2: "What makes a good unit test? What's the difference between a unit test and an integration test?"**

**SDE-2 Answer:** A good unit test is FIRST: Fast (milliseconds, no I/O), Independent (doesn't depend on other tests' execution order or shared state), Repeatable (same result every run, no flakiness from timing or randomness), Self-validating (clear pass/fail, no manual inspection), and Timely (written close to when the code is written, ideally before). A unit test exercises a single class or method in isolation, with all dependencies replaced by test doubles (mocks/stubs) — it verifies the unit's logic, not its integration with real infrastructure. An integration test verifies that multiple components work correctly together — for example, that your repository correctly persists to an actual (often in-memory or containerized) database, or that your service correctly calls a real (or realistically simulated) external API. Integration tests are slower and more brittle but catch issues unit tests can't, like SQL syntax errors, serialization mismatches, or actual network behavior. The test pyramid principle says: write many fast unit tests, fewer integration tests, and very few end-to-end tests, because each layer up trades speed and isolation for realism.

**Q3: "How would you test a method with a hard dependency on the current time, like `LocalDateTime.now()`?"**

**SDE-2 Answer:** Hardcoded calls to `LocalDateTime.now()` or `System.currentTimeMillis()` make code untestable because the expected result changes every time the test runs. The fix is dependency injection of a `Clock` (`java.time.Clock`), which Java's time API was specifically designed to support. Instead of calling `LocalDateTime.now()` directly, inject a `Clock` into the class constructor and call `LocalDateTime.now(clock)`. In production, you inject `Clock.systemDefaultZone()`. In tests, you inject `Clock.fixed(Instant.parse("2024-01-01T00:00:00Z"), ZoneId.of("UTC"))`, giving you a deterministic, repeatable time for assertions. This is a specific instance of a general testing principle: any non-deterministic dependency (time, randomness, UUID generation, external I/O) should be injected as an abstraction so tests can control it precisely.

# CHAPTER 9: Modern Java Features

This final chapter consolidates the modern Java syntax features (Java 14–21) that define how production Java is written today. Several were introduced earlier alongside their conceptual context (Chapter 4 for records/sealed classes, Chapter 7 for virtual threads) — this chapter is your concentrated reference for interview prep and daily use.

---

## 9.1 Records (Java 16+): The Complete Picture

```java
// Canonical record: auto-generates constructor, accessors, equals, hashCode, toString
public record OrderDTO(Long id, BigDecimal amount) {}

// What the compiler generates (conceptually equivalent to):
// public final class OrderDTO {
//     private final Long id;
//     private final BigDecimal amount;
//     public OrderDTO(Long id, BigDecimal amount) { this.id = id; this.amount = amount; }
//     public Long id() { return id; }                    // NOTE: id(), not getId()
//     public BigDecimal amount() { return amount; }
//     public boolean equals(Object o) { /* field-by-field */ }
//     public int hashCode() { /* based on all fields */ }
//     public String toString() { /* OrderDTO[id=1, amount=99.99] */ }
// }

import java.math.BigDecimal;
import java.util.Objects;

// Compact constructor — validation without repeating the parameter list
public record Money(BigDecimal amount, String currency) {
    
    // Compact constructor: parameters are implicit, assignment happens automatically
    // after this block (unless you reassign the parameter, like 'currency' below)
    public Money {
        Objects.requireNonNull(amount, "amount cannot be null");
        Objects.requireNonNull(currency, "currency cannot be null");
        if (amount.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException("amount cannot be negative");
        }
        currency = currency.toUpperCase(); // normalize before assignment
    }
    
    // Records can have additional methods
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(this.amount.add(other.amount), this.currency);
    }
    
    // Records can have static methods/fields
    public static Money zero(String currency) {
        return new Money(BigDecimal.ZERO, currency);
    }
    
    // Records can implement interfaces
}

// Records can implement interfaces (but cannot extend classes — they implicitly extend Record)
public record Point(int x, int y) implements Comparable<Point> {
    @Override
    public int compareTo(Point other) {
        return Integer.compare(this.x * this.x + this.y * this.y,
                               other.x * other.x + other.y * other.y);
    }
}

// Generic records work fine
public record Pair<A, B>(A first, B second) {}

// Records and Jackson (JSON serialization) — works automatically with Jackson 2.12+
// because Jackson recognizes the canonical constructor and accessor pattern
public record UserResponse(Long id, String name, String email) {}
// ObjectMapper mapper = new ObjectMapper();
// String json = mapper.writeValueAsString(new UserResponse(1L, "Surya", "s@example.com"));
// → {"id":1,"name":"Surya","email":"s@example.com"}
// UserResponse user = mapper.readValue(json, UserResponse.class); // deserializes correctly
```

**When to use records:** DTOs, value objects, API request/response bodies, immutable configuration, tuple-like return values. **When NOT to use records:** entities with mutable state (JPA entities generally need mutability and a no-arg constructor — records don't fit well), classes needing inheritance (records can't extend other classes), classes with complex internal state that shouldn't be exposed via accessors.

---

## 9.2 Sealed Classes (Java 17+): Exhaustive Hierarchies

```java
// 'permits' explicitly lists every allowed direct subtype
// Subtypes must be: final, sealed (with their own permits), or non-sealed
public sealed interface PaymentMethod 
    permits CreditCard, PayPal, BankTransfer, Cryptocurrency {}

public record CreditCard(String last4Digits, String expiryDate) implements PaymentMethod {}
public record PayPal(String email) implements PaymentMethod {}
public record BankTransfer(String iban) implements PaymentMethod {}

// 'non-sealed' reopens the hierarchy — any class can extend Cryptocurrency
public non-sealed class Cryptocurrency implements PaymentMethod {
    private String walletAddress;
    // ... can be extended further by anyone
}

public class Bitcoin extends Cryptocurrency {} // allowed because Cryptocurrency is non-sealed

// The payoff: EXHAUSTIVE pattern matching, verified by the compiler
public class PaymentProcessor {
    public String describe(PaymentMethod method) {
        return switch (method) {
            case CreditCard cc -> "Card ending in " + cc.last4Digits();
            case PayPal pp     -> "PayPal: " + pp.email();
            case BankTransfer bt -> "Bank transfer: " + bt.iban();
            case Cryptocurrency crypto -> "Crypto payment";
            // NO default needed — compiler verified ALL permitted types are handled
            // If you add a new type to 'permits' and forget a case here → COMPILE ERROR
        };
    }
}

// Sealed classes are PERFECT for modeling finite state machines, AST nodes,
// API response variants (Success/Error/Loading), and any "one of N known types" domain
public sealed interface ApiResult<T> permits ApiResult.Success, ApiResult.Error {
    record Success<T>(T data) implements ApiResult<T> {}
    record Error<T>(String message, int code) implements ApiResult<T> {}
}

public <T> void handleResult(ApiResult<T> result) {
    switch (result) {
        case ApiResult.Success<T> s -> System.out.println("Got: " + s.data());
        case ApiResult.Error<T> e   -> System.out.println("Failed: " + e.message());
    }
}
```

---

## 9.3 Pattern Matching for instanceof (Java 16+)

```java
// OLD WAY — verbose, error-prone (had to manually cast after checking)
Object obj = "Hello, Surya";
if (obj instanceof String) {
    String s = (String) obj;        // manual cast — could be typo'd to wrong type
    System.out.println(s.length());
}

// NEW WAY — pattern variable bound automatically, scoped to the if-block
if (obj instanceof String s) {     // 's' only exists where the cast would succeed
    System.out.println(s.length()); // no manual cast needed
}

// Pattern matching with additional conditions (the && works because 's' is in scope)
if (obj instanceof String s && s.length() > 5) {
    System.out.println("Long string: " + s);
}

// Negated pattern — 's' is available AFTER the if-block due to flow analysis
// (the compiler knows: if we reach past this if, obj instanceof String was false → must return)
Object value = getValue();
if (!(value instanceof String s)) {
    return;  // must exit/throw — otherwise compiler can't guarantee 's' is bound below
}
System.out.println(s.toUpperCase()); // 's' is in scope here!

// Real-world usage in equals() — much cleaner than before
public class Point {
    private final int x, y;
    
    @Override
    public boolean equals(Object obj) {
        // Combines instanceof check, cast, AND field comparison in one line
        return obj instanceof Point p && this.x == p.x && this.y == p.y;
    }
}
```

---

## 9.4 Switch Expressions (Java 14+): Arrow Syntax and yield

```java
// Statement (old, Java ≤ 13): can fall through, doesn't return a value
int numLetters;
switch (day) {
    case MONDAY:
    case FRIDAY:
    case SUNDAY:
        numLetters = 6;
        break;
    case TUESDAY:
        numLetters = 7;
        break;
    default:
        numLetters = 0;
}

// Expression (new, Java 14+): returns a value, no fall-through, exhaustive
int numLetters2 = switch (day) {
    case MONDAY, FRIDAY, SUNDAY -> 6;
    case TUESDAY -> 7;
    case THURSDAY, SATURDAY -> 8;
    case WEDNESDAY -> 9;
};
// If 'day' is an enum and you cover ALL constants, no 'default' needed
// If you DON'T cover all cases, compiler forces you to add 'default'

// Multi-statement arm with 'yield'
int result = switch (day) {
    case MONDAY -> 1;
    default -> {
        System.out.println("Computing for: " + day);
        int computed = day.toString().length();
        yield computed;  // 'yield' returns the value from a block arm
    }
};

// Pattern matching in switch (Java 21 — finalized) — combines sealed types + patterns
sealed interface Shape permits Circle, Square {}
record Circle(double radius) implements Shape {}
record Square(double side) implements Shape {}

double area = switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Square s -> s.side() * s.side();
};

// Guarded patterns (Java 21) — add a condition to a pattern case with 'when'
String describe(Object obj) {
    return switch (obj) {
        case Integer i when i < 0 -> "negative integer";
        case Integer i when i == 0 -> "zero";
        case Integer i -> "positive integer";
        case String s when s.isEmpty() -> "empty string";
        case String s -> "string: " + s;
        case null -> "null value";       // Java 21: explicit null handling in switch
        default -> "unknown type";
    };
}
```

---

## 9.5 Text Blocks (Java 15+)

```java
// OLD WAY — string concatenation hell for multiline content
String json_old = "{\n" +
    "  \"name\": \"Surya\",\n" +
    "  \"role\": \"Engineer\"\n" +
    "}";

// NEW WAY — text block, starts with """  on its own line
String json = """
    {
      "name": "Surya",
      "role": "Engineer"
    }
    """;
// Leading whitespace common to ALL lines is automatically stripped (incidental indentation)
// Trailing whitespace on each line is stripped UNLESS you use \s to preserve it

// SQL queries — much more readable
String query = """
    SELECT u.id, u.name, o.total
    FROM users u
    JOIN orders o ON u.id = o.user_id
    WHERE o.status = 'COMPLETED'
    ORDER BY o.total DESC
    """;

// HTML generation
String html = """
    <html>
      <body>
        <h1>%s</h1>
      </body>
    </html>
    """.formatted("Hello, Surya!");  // .formatted() works like String.format

// Escape sequences still work inside text blocks
String withQuotes = """
    She said "hello" to me.
    """;  // no need to escape " inside triple-quoted block

// \ at end of line suppresses the newline (line continuation)
String singleLine = """
    This is all \
    one line, no \
    newlines between.""";
// Result: "This is all one line, no newlines between."
```

---

## 9.6 `var`: Local Variable Type Inference (Java 10+)

```java
// var infers the type from the right-hand side AT COMPILE TIME
// This is NOT dynamic typing — the type is fixed and checked at compile time,
// it's just not WRITTEN explicitly. Fully different from JavaScript's 'var'!

var name = "Surya";              // inferred as String
var count = 42;                  // inferred as int
var prices = new ArrayList<Double>(); // inferred as ArrayList<Double>
var map = new HashMap<String, List<Integer>>(); // saves a LOT of typing here

// name = 42;  // COMPILE ERROR — name's type is fixed as String, not dynamic!

// GOOD uses of var: reduces redundancy when type is obvious from context
var orders = new ArrayList<Order>();              // obvious from constructor
for (var order : orders) { ... }                  // obvious from orders' type
var result = orderService.calculateTotal(order);  // type is in the method signature anyway

// BAD uses of var: hides important type information, hurts readability
var x = getData();              // BAD — what type is x?? Have to look up getData()'s signature
var result = process(a, b, c);  // BAD — same issue

// var CANNOT be used for:
// var x;              // COMPILE ERROR — no initializer to infer from
// var x = null;       // COMPILE ERROR — null has no inferable type
// void method(var x) {} // COMPILE ERROR — var not allowed for method parameters
// var fields;          // COMPILE ERROR — var not allowed for class fields
// Only allowed for: local variables, for-loop variables, try-with-resources variables

// Rule of thumb: use var when the type is OBVIOUS from the right side (constructor
// calls, factory methods with clear names) or when the type is verbose/generic
// and adds no clarity (Map<String, List<Order>> map = new HashMap<>() → use var
// on the left at least). Avoid var when it would hide the type at a point where
// the reader needs it to understand the code (e.g., return value of a method
// with unclear naming).
```

---

## ┌─────────────────────────────────────────────┐
##   WHAT INTERVIEWERS ASK
## └─────────────────────────────────────────────┘

**Q1: "What features in Java 17/21 do you use and why?"**

**SDE-2 Answer:** Records (Java 16) eliminate DTO boilerplate — for any immutable data carrier (API responses, value objects, command/query objects in CQRS), a record gives you the constructor, accessors, equals, hashCode, and toString in one line instead of 40+ lines of manual code, with compact constructors available for validation. Sealed classes (Java 17) let me model closed, finite hierarchies — payment methods, API result types, AST nodes — with compiler-verified exhaustive switch expressions, catching missing cases at compile time rather than via runtime default branches. Pattern matching for instanceof and switch (16, 21) removes manual casting boilerplate and makes type-dispatch code far more readable, especially combined with sealed types for exhaustiveness. Virtual threads (21) are the biggest architectural shift — I can write simple, blocking-style I/O code for high-concurrency services without the complexity of reactive programming, while still getting massive throughput. Text blocks (15) make embedded SQL, JSON, and HTML readable instead of escaped string concatenation. Together, these features substantially reduce boilerplate and shift more correctness checks to compile time, which is exactly what you want in a production codebase at scale.

**Q2: "What is the difference between a sealed interface and a regular interface with multiple implementations?"**

**SDE-2 Answer:** A regular interface can be implemented by ANY class, anywhere, including code the interface author never anticipated — this is intentional openness, good for extensibility points like `Comparable` or `Runnable`. A sealed interface explicitly restricts which classes can implement it via the `permits` clause — only the listed classes (which must be in the same module or package, depending on configuration) can implement it. The practical benefit is exhaustiveness: when you `switch` on a sealed type's possible implementations, the compiler verifies you've handled every permitted case, eliminating an entire class of bugs where a new variant is added but a switch statement somewhere is forgotten (silently falling into an unintended default branch). Use sealed types when you're modeling a closed, finite domain — payment types, parser AST nodes, result types (Success/Failure) — where you WANT to know at compile time if a new case is added. Use regular interfaces for open extension points where third-party or future code should be able to add new implementations freely.

**Q3: "When should you avoid using var?"**

**SDE-2 Answer:** Avoid `var` whenever the inferred type isn't obvious from the right-hand side of the assignment — for example, `var result = service.process(input)` tells the reader nothing about what `result` is without looking up `process`'s signature. This particularly hurts in code review, where reviewers scan diffs without an IDE's inline type hints. Avoid it for primitive-adjacent numeric types where the exact type matters (`var x = 5` is `int`, but if you actually need a `long`, you must write `var x = 5L` — `var` doesn't change this requirement but makes the discrepancy less visible). Avoid it when interface types matter — `var list = new ArrayList<String>()` infers the concrete type `ArrayList<String>`, not `List<String>`, which can subtly affect overload resolution or signal an implementation detail you didn't mean to expose. Good uses are constructor calls with clear class names, enhanced for-loops over clearly-typed collections, and try-with-resources blocks. The general guideline used at most engineering organizations: use `var` to reduce noise when the type is genuinely redundant to state, never to save keystrokes at the cost of readability.

---

## Closing Note

You have now covered, from first principles to production patterns: how the JVM executes your code and manages memory, the complete syntax and object model of the language, the internals of every collection you'll reach for daily, generics and the functional/streams paradigm, the full concurrency toolkit from `synchronized` to virtual threads, professional testing practice, and the modern syntax that defines idiomatic Java in 2026.

The path forward from here is building: take a real project — a REST API with Spring Boot, a concurrent job processor, a CLI tool — and apply every chapter. Internals knowledge sticks when it explains a bug you hit yourself. Revisit the "What Interviewers Ask" boxes the night before any interview; they are calibrated to the depth SDE-2 panels expect, not just definitions.

