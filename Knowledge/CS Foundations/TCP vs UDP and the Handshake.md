---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 4 — Networking"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, networking, tcp]
---

# TCP vs UDP and the Handshake

## UDP (User Datagram Protocol)
UDP is simple, unreliable, and connectionless. It sends packets without guaranteeing delivery, ordering, or flow control. It is used for low-latency tasks where dropped packets are acceptable (e.g., DNS queries, video streaming, gaming).

## TCP (Transmission Control Protocol)
TCP adds reliability, ordering, and flow control on top of IP.
- **Reliable:** Acknowledges received bytes, retransmits if lost.
- **Ordered:** Reorders out-of-sequence packets.
- **Flow/Congestion Control:** Prevents the sender from overwhelming the receiver or the network.

### The Three-Way Handshake
TCP requires establishing a connection before sending data:
1. Client sends `SYN`.
2. Server responds with `SYN-ACK`.
3. Client responds with `ACK`.

This handshake costs one full Round Trip Time (RTT). This overhead is why **connection pooling** (like HikariCP) and HTTP Keep-Alive exist—reusing connections avoids the 50-100ms latency hit of repeated handshakes.

### Four-Way Termination and TIME_WAIT
Connections are closed via independent `FIN` and `ACK` packets from both sides. After closing, a socket enters a `TIME_WAIT` state to ensure late packets are handled. Under high load, servers can run out of ephemeral ports if too many sockets enter `TIME_WAIT`.

### Sockets
A socket is an OS abstraction representing one endpoint of a TCP connection. A connection is uniquely identified by a 4-tuple: `(source_IP, source_port, destination_IP, destination_port)`. Multiple clients can connect to a server's port 80/443 simultaneously because their source IPs/ports differ, creating unique sockets.
