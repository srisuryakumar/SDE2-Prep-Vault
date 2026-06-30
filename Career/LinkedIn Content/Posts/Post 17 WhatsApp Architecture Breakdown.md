---
type: linkedin-post
post_number: 17
scheduled_week: 9
scheduled_day: Tuesday
status: drafted
---
How WhatsApp delivers 100 billion messages per day. The architecture
that makes it work.

[ATTACH: Architecture diagram]

Key decisions explained:

1. WebSocket, not HTTP polling
   Persistent connections. Server pushes messages instantly.
   50M concurrent connections across chat servers.

2. Kafka between chat servers
   Sender → your chat server → Kafka → recipient's chat server → recipient
   Decouples the send and receive paths. Survives server restarts.

3. Cassandra for message storage
   Partition key = conversation_id. Cluster key = message_timestamp.
   This makes fetching the last 50 messages of a conversation O(1).

4. Offline delivery
   Message stored in Cassandra. Push notification sent.
   When user comes online: pull pending messages since last seen offset.

5. End-to-end encryption
   Signal protocol. Keys never leave the device. WhatsApp cannot read your messages.

Trade-off I found interesting: read receipts (double blue tick) require
a separate ACK message flow back from recipient to sender through the
same Kafka pipeline. This is why delivery can lag separately from sending.

#SystemDesign #DistributedSystems #BackendEngineering
