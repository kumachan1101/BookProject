import os
import re

directory = 'c:/Users/kumac/OneDrive/デスクトップ/antigravity/BookProject/02_章別'
md_files = [f for f in os.listdir(directory) if f.endswith('.md')]

for f in md_files:
    content = open(os.path.join(directory, f), encoding='utf-8').read()
    code_blocks = re.findall(r'```c\n(.*?)\n```', content, re.DOTALL)
    for i, code in enumerate(code_blocks):
        lines = code.split('\n')
        for j, line in enumerate(lines):
            line = line.strip()
            # Find static variables (not functions)
            if line.startswith('static ') and '(' not in line and 'const' not in line:
                print(f"[{f}] Static Variable (Not Thread-Safe?): '{line}'")
            
            # Find potential memory leaks (malloc without corresponding free... hard to do simply, but we can list all mallocs and frees per file)
            if 'malloc' in line or 'calloc' in line or 'strdup' in line:
                pass # print(f"[{f}] Malloc: '{line}'")
            if 'free(' in line:
                pass # print(f"[{f}] Free: '{line}'")
