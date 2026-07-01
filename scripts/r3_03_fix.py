import os
import yaml

def parse_frontmatter(content):
    if content.startswith('---\n'):
        end_idx = content.find('---\n', 4)
        if end_idx != -1:
            try:
                fm = yaml.safe_load(content[4:end_idx])
                return fm
            except:
                pass
    return {}

with open('health_updated.txt', 'r') as f:
    lines = f.readlines()

orphans = []
in_orphans = False
for line in lines:
    if line.startswith('Orphans'):
        in_orphans = True
        continue
    if in_orphans and line.strip().startswith('-'):
        orphans.append(line.strip()[2:])

def find_file(name):
    for root, _, files in os.walk('.'):
        if '.git' in root or '.obsidian' in root:
            continue
        for file in files:
            if file[:-3] == name:
                return os.path.join(root, file)
    return None

cat_a = 0
cat_b = 0
cat_c = 0
cat_d = 0

for orphan in orphans:
    path = find_file(orphan)
    if not path:
        continue
        
    if path.startswith('./Knowledge/'):
        if '_MOC' in path or 'MOC' in path:
            pass # ignore
        else:
            cat_a += 1
            # Try to add it to MOC
            with open(path, 'r') as f:
                content = f.read()
            fm = parse_frontmatter(content)
            subject = fm.get('subject') if fm else None
            
            # Find subject MOC
            if subject:
                # Need to find the _Subject MOC.md and append
                moc_name = f"_{subject} MOC.md"
                moc_path = find_file(moc_name[:-3])
                if moc_path:
                    with open(moc_path, 'a') as f:
                        f.write(f"\n- [[{orphan}]]\n")
    elif path.startswith('./Practice/LeetCode/'):
        if '_LeetCode MOC' not in orphan:
            cat_b += 1
            with open(path, 'r') as f:
                content = f.read()
            fm = parse_frontmatter(content)
            patterns = fm.get('patterns', [])
            if isinstance(patterns, list):
                for p in patterns:
                    p_path = find_file(p)
                    if not p_path:
                        # create stub
                        stub_path = f"Knowledge/DSA/{p}.md"
                        if not os.path.exists(stub_path):
                            with open(stub_path, 'w') as f:
                                f.write(f"---\ntype: concept\nsubject: DSA\nstatus: stub\n---\n# {p}\n")
    elif path.startswith('./Career/') or path.startswith('./Daily Journal/'):
        cat_c += 1
    elif path.startswith('./Templates/'):
        cat_d += 1

print(f"Cat A: {cat_a}, Cat B: {cat_b}, Cat C: {cat_c}, Cat D: {cat_d}")
