import os
import re

base_dir = r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"
files = sorted([f for f in os.listdir(base_dir) if f.endswith('.md')])

code_blocks = []

for f in files:
    filepath = os.path.join(base_dir, f)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Find all ```c blocks
    # regex matches ```c followed by anything until ```
    matches = re.finditer(r'```c\n(.*?)\n```', content, re.DOTALL)
    for m in matches:
        code_content = m.group(1).strip()
        # count lines
        lines = len(code_content.split('\n'))
        # get first 50 chars for preview
        preview = code_content.replace('\n', ' ')[:50]
        code_blocks.append(f"- **{f}** ({lines} 行): `{preview}...`")

with open(r"C:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\code_blocks_list.md", "w", encoding="utf-8") as out:
    out.write("# コード例一覧\n\n")
    out.write("\n".join(code_blocks))
    
print(f"Extraction complete: {len(code_blocks)} code blocks found.")
