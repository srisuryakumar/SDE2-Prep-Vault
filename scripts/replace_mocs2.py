import os

replacements = [
    ("[[_Java Mastery MOC]]", "[[_Java MOC]]"),
    ("[[_Java Mastery MOC|", "[[_Java MOC|"),
    ("[[_Data Structures and Algorithms MOC]]", "[[_DSA MOC]]"),
    ("[[_Data Structures and Algorithms MOC|", "[[_DSA MOC|"),
    ("[[_Databases and Caching MOC]]", "[[_Databases MOC]]"),
    ("[[_Databases and Caching MOC|", "[[_Databases MOC|"),
    ("[[_Low Level Design MOC]]", "[[_LLD MOC]]"),
    ("[[_Low Level Design MOC|", "[[_LLD MOC|"),
    ("[[_Spring Boot and Backend Engineering MOC]]", "[[_Spring Boot MOC]]"),
    ("[[_Spring Boot and Backend Engineering MOC|", "[[_Spring Boot MOC|")
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
                new_content = new_content.replace(old, new)
                
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
                count += 1
print(f"Modified {count} files.")
