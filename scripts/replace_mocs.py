import os
import re

replacements = [
    (r'\[\[_Java Mastery MOC(\]?|\|)', r'[[_Java MOC\1'),
    (r'\[\[_Data Structures and Algorithms MOC(\]?|\|)', r'[[_DSA MOC\1'),
    (r'\[\[_Databases and Caching MOC(\]?|\|)', r'[[_Databases MOC\1'),
    (r'\[\[_Low Level Design MOC(\]?|\|)', r'[[_LLD MOC\1'),
    (r'\[\[_Spring Boot and Backend Engineering MOC(\]?|\|)', r'[[_Spring Boot MOC\1')
]

count = 0
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.obsidian' in root:
        continue
    for file in files:
        if file.endswith('.md'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            new_content = content
            for old, new in replacements:
                new_content = re.sub(old, new, new_content)
                
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                count += 1
print(f"Modified {count} files.")
