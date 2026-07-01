import os
import re
from pathlib import Path

def get_all_md_files():
    all_files = {}
    for root, _, files in os.walk('.'):
        if '.git' in root or '.obsidian' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                name_without_ext = file[:-3]
                all_files[name_without_ext.lower()] = name_without_ext
    return all_files

all_files = get_all_md_files()
print(f"Total markdown files found: {len(all_files)}")

def fix_links():
    with open('health_updated.txt', 'r') as f:
        lines = f.readlines()
    
    broken_links = []
    in_broken = False
    for line in lines:
        if line.startswith('Broken Links'):
            in_broken = True
            continue
        if line.startswith('Orphans'):
            in_broken = False
            break
        if in_broken and line.strip().startswith('-'):
            # format: - source.md -> [[target]]
            parts = line.strip().split(' -> ')
            if len(parts) == 2:
                source = parts[0][2:].strip()
                target_raw = parts[1].strip()
                if target_raw.startswith('[[') and target_raw.endswith(']]'):
                    target = target_raw[2:-2]
                    # handle display text [[target|display]]
                    if '|' in target:
                        target = target.split('|')[0]
                    # handle path in target [[folder/target]]
                    if '/' in target:
                        target = target.split('/')[-1]
                    broken_links.append((source, target, target_raw))

    print(f"Found {len(broken_links)} broken links to process.")
    
    stubs_created = set()
    updates = {}
    
    for source, target, target_raw in broken_links:
        # Search for matching file
        target_lower = target.lower()
        match = all_files.get(target_lower)
        
        if match:
            # We found a match! Update source.
            if source not in updates:
                with open(source, 'r') as f:
                    updates[source] = f.read()
            # Replace exact target_raw with new link
            # Need to be careful about replacing just the text
            new_link = f"[[{match}]]"
            if '|' in target_raw:
                display = target_raw[2:-2].split('|')[1]
                new_link = f"[[{match}|{display}]]"
            updates[source] = updates[source].replace(target_raw, new_link)
            # Also try replacing just [[target]] in case target_raw had path
            updates[source] = updates[source].replace(f"[[{target}]]", f"[[{match}]]")
        else:
            # Stub needed
            if target not in stubs_created:
                # Decide location
                if "System Design" in target or "Architecture" in target or "HLD" in target:
                    stub_path = f"Knowledge/System Design/{target}.md"
                    template = f"---\ntype: concept\nsubject: System Design\nstatus: stub\n---\n# {target}\n"
                elif "LLD" in target or "Pattern" in target or "Principle" in target:
                    stub_path = f"Knowledge/LLD/{target}.md"
                    template = f"---\ntype: concept\nsubject: LLD\nstatus: stub\n---\n# {target}\n"
                elif any(char.isdigit() for char in target[:4]):
                    # Likely a LeetCode problem
                    stub_path = f"Practice/LeetCode/{target}.md"
                    template = f"---\ntype: problem\nstatus: stub\n---\n# {target}\n"
                else:
                    stub_path = f"Knowledge/CS Foundations/{target}.md"
                    template = f"---\ntype: concept\nsubject: CS Foundations\nstatus: stub\n---\n# {target}\n"
                
                os.makedirs(os.path.dirname(stub_path), exist_ok=True)
                if not os.path.exists(stub_path):
                    with open(stub_path, 'w') as f:
                        f.write(template)
                    stubs_created.add(target)
                    all_files[target_lower] = target

    # Write updates
    count = 0
    for source, content in updates.items():
        with open(source, 'w') as f:
            f.write(content)
        count += 1
    
    print(f"Updated {count} files.")
    print(f"Created {len(stubs_created)} stubs.")

fix_links()
