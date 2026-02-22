import re

def show_nested(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to match list items including nested ones
    lines = content.split('\n')
    
    in_list = False
    list_block = []
    has_nesting = False
    
    print(f"--- Nested blocks in {filename} ---")
    for i, line in enumerate(lines):
        if re.match(r'^(?: {4}|\t)*[\-\*]\s+', line):
            in_list = True
            list_block.append((i+1, line))
            if re.match(r'^(?: {4}|\t)+[\-\*]\s+', line):
                has_nesting = True
        elif in_list and not line.strip():
            # end of list (simple heuristic)
            pass # allow empty lines
        elif in_list and line.startswith(' '):
            list_block.append((i+1, line))
        else:
            if in_list and has_nesting:
                print(f">>> Found block starting at line {list_block[0][0]}:")
                for _, l in list_block:
                    print(l)
                print("-" * 40)
            in_list = False
            list_block = []
            has_nesting = False

show_nested("02_章別/05_第1部 第3章 構造体設計とコンポジション - データと責任の統合_01.md")
show_nested("02_章別/12_第2部 第8章 単一責任原則 (SRP) 変更の軸を明確にする設計指針_01.md")
