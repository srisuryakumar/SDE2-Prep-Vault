---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 2 — Operating Systems"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [cs-foundations, os, file-system]
---

# File Systems and Inodes

A file system organizes raw disk storage into a hierarchy of files and directories. 

## Inodes (Index Nodes)
On Unix file systems, every file is represented by an inode. An inode contains metadata:
- File type (regular, directory, symlink)
- Permissions, owner UID, group GID
- Size, timestamps (created, modified, accessed)
- Pointers to the physical data blocks on disk where the file content lives

### Filenames
The inode does **not** contain the filename. Filenames live in **directory entries**. A directory is a file that maps filenames to inode numbers.
- This is why renaming a file is instant: it just updates the directory entry, without copying data.
- It also allows **hard links**: multiple directory entries pointing to the same inode.

## Everything is a File (Unix)
Unix treats all I/O resources like files.
- `/etc/hosts`: Regular file
- `/dev/null`: Character device
- `/tmp/mypipe`: Named pipe
- Network connections: TCP sockets

Your Spring Boot app uses TCP sockets for HTTP, which are treated by the OS as network files.
