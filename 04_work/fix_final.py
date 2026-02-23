import os
import re
from pathlib import Path

# Use the absolute path provided in user_information
src_dir = Path(r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\01_原稿")

def fix_content(content):
    # 1. Remove heading numbers like "2.5. ", "1. ", "3.3.1. "
    # Supports H2-H5. Matches starting number sequence.
    new_content = re.sub(r'^(#{2,5})\s+\d+(?:\.\d+)*\.?\s+', r'\1 ', content, flags=re.M)
    
    # 2. Fix single bullet points (convert to paragraph)
    lines = new_content.split('\n')
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Match bullet
        match = re.match(r'^[\-\*]\s+(.*)$', line)
        if match:
            # Check if alone
            prev_is_bullet = (i > 0 and re.match(r'^[\-\*]\s+', lines[i-1]))
            next_is_bullet = (i + 1 < len(lines) and re.match(r'^[\-\*]\s+', lines[i+1]))
            
            if not prev_is_bullet and not next_is_bullet:
                # Convert to paragraph
                fixed_lines.append(match.group(1))
                i += 1
                continue
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines)

processed = 0
for file_path in src_dir.glob("*.md"):
    content = file_path.read_text(encoding="utf-8")
    new_content = fix_content(content)
    
    if content != new_content:
        file_path.write_text(new_content, encoding="utf-8")
        processed += 1
        print(f"Fixed: {file_path.name}")

print(f"Total: {processed}")
