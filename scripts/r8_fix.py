import os
import re

def append_to_frontmatter(content, link):
    if content.startswith('---\n'):
        end_idx = content.find('---\n', 4)
        if end_idx != -1:
            frontmatter = content[:end_idx]
            body = content[end_idx:]
            if 'related_concepts:' in frontmatter:
                # Add link if not exists
                if link not in frontmatter:
                    frontmatter = frontmatter.replace('related_concepts: [', f'related_concepts: ["{link}", ')
            else:
                frontmatter += f"related_concepts: [\"{link}\"]\n"
            return frontmatter + body
    return content

def add_body_link(content, link, reason):
    section = "\n## Related Concepts\n"
    if "## Related Concepts" in content:
        # append under it
        parts = content.split("## Related Concepts\n")
        return parts[0] + "## Related Concepts\n" + f"- See also {link} for {reason}.\n" + parts[1]
    else:
        return content + section + f"- See also {link} for {reason}.\n"

def process_file(filepath, link, reason):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        content = f.read()
    
    content = append_to_frontmatter(content, link)
    content = add_body_link(content, link, reason)
    
    with open(filepath, 'w') as f:
        f.write(content)

# 1. Java HashMap
process_file("Knowledge/Java/Java HashMap Internals.md", "[[HashMap and Frequency Counting]]", "the algorithmic applications of frequency counting")

# 2. DSA Sliding Window
process_file("Knowledge/DSA/Sliding Window Pattern - Variable Size.md", "[[Rate Limiting Algorithms]]", "the rate limiter implementation behind token bucket")
process_file("Knowledge/DSA/Sliding Window Pattern - Fixed Size.md", "[[Rate Limiting Algorithms]]", "the rate limiter implementation behind token bucket")

# 3. DB B-Tree
process_file("Knowledge/Databases/B-Tree Indexes and EXPLAIN ANALYZE.md", "[[Binary Search Tree Properties]]", "binary search trees, since B-Trees are a generalization")

# 4. Kafka
process_file("Knowledge/System Design/Kafka Architecture.md", "[[@KafkaListener]]", "the Spring Boot implementation of a Kafka consumer")

# 5. CAP Theorem
process_file("Knowledge/Databases/CAP Theorem.md", "[[Cassandra (Wide-Column Store)]]", "the canonical AP example")
process_file("Knowledge/Databases/CAP Theorem.md", "[[MongoDB (Document Store)]]", "the canonical CP example")

# 6. LLD Observer
process_file("Knowledge/LLD/Observer Pattern.md", "[[Kafka Consumer Group Rebalancing]]", "how Kafka's consumer model is the distributed implementation of the Observer pattern")

print("Done R8.")
