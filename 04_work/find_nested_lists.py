import glob
import re
import sys

def find_nested_lists():
    files = glob.glob('02_章別/*.md')
    nested_pattern = re.compile(r'^(?: {4}|\t)+[\-\*]\s+', re.MULTILINE)
    
    files_with_nested = []
    total_findings = 0
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        matches = list(nested_pattern.finditer(content))
        if matches:
            files_with_nested.append((filepath, len(matches)))
            total_findings += len(matches)
            
    print(f"Total files with nested lists: {len(files_with_nested)}")
    print(f"Total nested list items found: {total_findings}")
    print("\nFiles to edit:")
    for filepath, count in files_with_nested:
        print(f"{filepath} ({count} items)")

if __name__ == '__main__':
    find_nested_lists()
