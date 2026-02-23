import os
import re

dir_path = r'C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別'
files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

def find_single_bullets(content):
    lines = content.splitlines()
    single_bullets = []
    for i, line in enumerate(lines):
        if re.match(r'^\s*[\*\-]\s+', line):
            # Check if it's part of a list
            is_lone = True
            # Check previous line
            if i > 0:
                prev = lines[i-1].strip()
                if prev and re.match(r'^\s*[\*\-]\s+', prev):
                    is_lone = False
            # Check next line
            if i < len(lines) - 1:
                nxt = lines[i+1].strip()
                if nxt and re.match(r'^\s*[\*\-]\s+', nxt):
                    is_lone = False
            
            if is_lone:
                single_bullets.append((i + 1, line))
    return single_bullets

results = []
for file in files:
    full_path = os.path.join(dir_path, file)
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    bullets = find_single_bullets(content)
    if bullets:
        results.append((file, bullets))

for file, bullets in results:
    print(f"File: {file}")
    for line_num, text in bullets:
        print(f"  Line {line_num}: {text}")
