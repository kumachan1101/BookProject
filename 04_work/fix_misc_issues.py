import os
import re
from pathlib import Path

src_dir = Path("../01_原稿")

def fix_content(content):
    # 1. Remove heading numbers like "1. ", "1.1. ", "1.1.1 " from headings H2-H5
    # Matches: ^(#{2,5})\s+(?:[0-9]+\.)(?:[0-9]+\.)*\s+(.*)$
    # Also matches: ^(#{2,5})\s+[0-9]+\.\s+(.*)$
    content = re.sub(r'^(#{2,5})\s+[0-9]+(?:\.[0-9]+)*\.?\s+(.*)$', r'\1 \2', content, flags=re.M)
    
    # 2. Fix single bullet points
    # We look for a paragraph that consists of exactly one bullet point.
    # A single bullet block: empty line, then exactly one bullet line, then empty line.
    # Actually, a bullet might span multiple lines if indented, but let's handle simple cases.
    
    lines = content.split('\n')
    new_lines = []
    
    # Track blocks
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line is a bullet
        match = re.match(r'^[\-\*]\s+(.*)$', line)
        
        if match:
            is_single = True
            
            # Look backwards 1 line
            if i > 0 and re.match(r'^[\-\*]\s+', lines[i-1]):
                is_single = False
            
            # Look forwards to see if there's another bullet before an empty line
            j = i + 1
            while j < len(lines):
                if lines[j].strip() == '':
                    break
                if re.match(r'^[\-\*]\s+', lines[j]):
                    is_single = False
                    break
                j += 1
            
            if is_single and j - i <= 3: # If the bullet text is not too long multiline
                # Convert the bullet to a normal paragraph
                # Replace the current line
                new_line = match.group(1)
                new_lines.append(new_line)
                
                # For subsequent lines in this block, lstrip them
                i += 1
                while i < j:
                    new_lines.append(lines[i].lstrip())
                    i += 1
                continue
                
        new_lines.append(line)
        i += 1
        
    return '\n'.join(new_lines)

processed = 0
for file_path in src_dir.glob("*.md"):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    new_content = fix_content(content)
    
    if content != new_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        processed += 1
        print(f"Fixed formatting in {file_path.name}")

print(f"\nTotal files modified: {processed}")
