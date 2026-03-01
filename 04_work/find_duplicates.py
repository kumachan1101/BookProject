import os
import re
from collections import defaultdict

base_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
files = sorted([f for f in os.listdir(base_dir) if f.endswith('.md')])

code_blocks = []

for f in files:
    filepath = os.path.join(base_dir, f)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        
    matches = re.finditer(r'```c\n(.*?)\n```', content, re.DOTALL)
    for m in matches:
        code_content = m.group(1).strip()
        lines = [line.strip() for line in code_content.split('\n') if line.strip() and not line.strip().startswith('//') and not line.strip() == '{' and not line.strip() == '}']
        simplified_code = "\n".join(lines)
        if len(simplified_code) > 50: # Ignore very small snippets
            code_blocks.append({"file": f, "code": simplified_code, "original": code_content})

# Find exact duplicates (after stripping comments and empty lines)
duplicates = defaultdict(list)
for block in code_blocks:
    duplicates[block["code"]].append(block["file"])

dup_results = {k: v for k, v in duplicates.items() if len(v) > 1}

print(f"Total blocks processed (length > 50): {len(code_blocks)}")
print(f"Found {len(dup_results)} unique blocks that are duplicated across files.")
for code, file_list in dup_results.items():
    print("-" * 40)
    print(f"Duplicated in: {', '.join(set(file_list))} ({len(file_list)} times)")
    first_few_lines = "\n".join(code.split('\n')[:3])
    print(f"Preview:\n{first_few_lines}...")
