import os
import re

dir_path = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別'
files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

def check_bold(line):
    count = line.count('**')
    if count == 0:
        return None
    
    issues = []
    if count % 2 != 0:
        issues.append("Unbalanced count")
    
    content = line.strip('\n\r')
    
    # Accurate space checks
    # Space after opening: ** followed by space, then something that ISN'T another *
    if re.search(r'\*\*[ 　]+[^* \n]', content):
        issues.append("Space after opening **")
        
    # Space before closing: something followed by space, then **
    # To avoid false positives, we check if it looks like a closing marker
    # e.g. **bold ** match, but word **bold no match.
    if re.search(r'[^* \n][ 　]+\*\*', content):
        # Heuristic: only flag if there's an opening ** before it in the same line
        if re.search(r'\*\*[^* ].*?[ 　]+\*\*', content):
            issues.append("Space before closing **")

    if line.strip().endswith('**') and count == 1:
        issues.append("Trailing unclosed **")

    if line.strip().startswith('**') and count == 1:
        issues.append("Leading unclosed **")

    if issues:
        return issues
    return None

results = []
for filename in files:
    path = os.path.join(dir_path, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                result = check_bold(line)
                if result:
                    results.append(f"{filename}:{i+1}: {', '.join(result)}")
                    results.append(f"  Line: {line.strip()}")
    except Exception as e:
        results.append(f"Error reading {filename}: {str(e)}")

with open(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\bold_issues.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
