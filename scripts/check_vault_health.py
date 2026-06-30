import os
import re

def main():
    vault_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # regex for wikilinks [[link]] or [[link|alias]] or [[link#header]]
    link_pattern = re.compile(r'\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]')
    
    all_notes = set()
    links = {} # source_file -> [destinations]
    status_stubs = 0
    status_to_study = 0
    incoming_links = {}
    
    # Find all markdown files
    for root, dirs, files in os.walk(vault_root):
        if '.git' in root or '.obsidian' in root or '_Source-Archive' in root or 'scripts' in root:
            continue
        for file in files:
            if file.endswith('.md'):
                rel_path = os.path.relpath(os.path.join(root, file), vault_root)
                note_name = file[:-3]
                all_notes.add(note_name)
                
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    if 'status: stub' in content:
                        status_stubs += 1
                    if 'status: to-study' in content:
                        status_to_study += 1
                        
                    found_links = link_pattern.findall(content)
                    links[rel_path] = found_links
                    
                    for link in found_links:
                        # Obsidian is case-insensitive for links in some cases but usually exact match
                        incoming_links[link] = incoming_links.get(link, 0) + 1

    # Check for broken links
    broken_links = []
    for source, dests in links.items():
        for dest in dests:
            if dest not in all_notes:
                broken_links.append((source, dest))
                
    # Check for orphans
    orphans = []
    for note in all_notes:
        if note not in incoming_links and note not in ['Home', 'Dashboard', '_Vault Conventions']:
            # Also ignore template files
            if not any(note in path for path in links.keys() if 'Templates' in path):
                orphans.append(note)

    print("=== Vault Health Check ===")
    print(f"Total Notes: {len(all_notes)}")
    print(f"Stubs: {status_stubs}")
    print(f"To-Study: {status_to_study}\n")
    
    print(f"Broken Links ({len(broken_links)}):")
    for src, dest in broken_links:
        print(f"  - {src} -> [[{dest}]]")
        
    print(f"\nOrphans ({len(orphans)}):")
    for orphan in sorted(orphans):
        print(f"  - {orphan}")

if __name__ == "__main__":
    main()
