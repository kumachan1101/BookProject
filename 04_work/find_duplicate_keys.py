import os
import re

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # We want to find blocks between headers (#### or ###) or Code Blocks
    # containing multiple "**処理の内容:**" etc.
    
    current_block_start = 0
    keys_in_block = []
    
    issues = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Delimiters: Headers or Code Fences
        if line.startswith('#### ') or line.startswith('```') or line.startswith('## '):
            if len(keys_in_block) > 1:
                # Check for duplicates
                counts = {}
                for k in keys_in_block:
                    counts[k] = counts.get(k, 0) + 1
                
                if any(c > 1 for c in counts.values()):
                    issues.append((current_block_start, i, counts))
            
            # Reset
            keys_in_block = []
            current_block_start = i
            continue
            
        # Check for keys
        if "**処理の内容:**" in line:
            keys_in_block.append("処理の内容")
        elif "**設計的意図:**" in line:
            keys_in_block.append("設計的意図")
        elif "**評価:**" in line:
            keys_in_block.append("評価")

    return issues

def main():
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                issues = analyze_file(path)
                if issues:
                    print(f"File: {file}")
                    for start, end, counts in issues:
                        print(f"  Lines {start+1}-{end+1}: {counts}")

if __name__ == "__main__":
    main()
