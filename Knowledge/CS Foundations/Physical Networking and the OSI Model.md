---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 4 — Networking"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations, networking, osi-model]
---

# Physical Networking and the OSI Model

At the bottom of all networking are physical signals (electrical on copper, light pulses in fiber, radio waves in WiFi). A Network Interface Card (NIC) converts bits to signals.

## Network Hardware
- **MAC Address:** A unique 48-bit identifier for every NIC on a local network.
- **Switch:** Connects computers on a local network using MAC addresses (Layer 2).
- **Router:** Connects different networks and forwards packets between them using IP addresses (Layer 3).

## The Network Models
Networking is divided into layers so higher layers don't have to worry about lower-level details (encapsulation).

### The OSI Model (7 Layers)
1. **Physical:** Electrical/optical signals, cables
2. **Data Link:** Ethernet, MAC addresses
3. **Network:** IP addressing, routing
4. **Transport:** TCP, UDP (reliability, ports)
5. **Session:** Session establishment
6. **Presentation:** Encryption (TLS), data encoding
7. **Application:** HTTP, DNS, WebSocket

### The TCP/IP Model (4 Layers)
Used in practice:
1. **Network Access** (OSI 1-2)
2. **Internet** (OSI 3)
3. **Transport** (OSI 4)
4. **Application** (OSI 5-7)

**Encapsulation:** As data travels down the layers on the sender side, each layer wraps the payload in its own header (e.g., HTTP payload inside TCP header, inside IP header, inside Ethernet frame). The receiver unwraps them in reverse.
