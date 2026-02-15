import os
import re

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

# Specific elements that MUST be Level 4 (####)
SPECIFIC_KEYWORDS = [
    "実行結果",
    "設計的意図",
    "システム概要",
    "処理の内容",
    "評価",
    "コード説明",
    "ファイル名",
    "課題の概要",
    "現状",
    "アンチパターン"
]

# Exact match keywords
SPECIFIC_EXACT_KEYWORDS = [
    "生成", "生成:", "生成：",
    "破棄", "破棄:", "破棄：",
    "続き", "続き:", "続き："
]

FILENAME_PATTERN = r'.*\b[\w\-]+\.(c|h|cpp|hpp|py|js|ts|java|go|rs|sh|bat|cmd|json|xml|yaml|yml|md|txt|log)\b.*'

def is_specific_heading(text):
    text = text.strip()
    
    if text in SPECIFIC_EXACT_KEYWORDS:
        return True
    
    for kw in SPECIFIC_KEYWORDS:
        if kw in text:
            return True
            
    if re.fullmatch(FILENAME_PATTERN, text, re.IGNORECASE):
        return True

    if "Makefile" in text or "CMakeLists.txt" in text:
        return True
        
    return False

def is_structured_subsection(text):
    """
    Checks if the text starts with a subsection number like "1.1", "2.3.1".
    Handles optional markdown formatting (bold/italic) at the start.
    Matches:
      1.1
      **1.1**
      *1.1*
      1.1.2
    Does NOT match:
      1. (This is usually a list or chapter level, but if inside ### it might be ambiguous. Assuming X.Y for subsections)
      Intro
    """
    # Remove leading common markdown symbols for check
    clean_text = re.sub(r'^[\*\_\s]+', '', text)
    return bool(re.match(r'^\d+\.\d+', clean_text))

def process_file_content(content):
    lines = content.splitlines(keepends=True)
    new_lines = []
    in_code_block = False
    
    for line in lines:
        if re.match(r'^\s*(`{3}|~{3})', line):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
            
        if in_code_block:
            new_lines.append(line)
            continue
            
        heading_match = re.match(r'^(\s*)(#+)\s+(.*)', line)
        if heading_match:
            indent = heading_match.group(1)
            original_hashes = heading_match.group(2)
            original_level = len(original_hashes)
            text_content = heading_match.group(3).rstrip() # remove trailing newline/spaces for logic
            
            new_level = original_level
            
            # 1. Specific Keywords -> Level 4
            if is_specific_heading(text_content):
                new_level = 4
                
            # 2. Level 3 logic
            elif original_level == 3:
                # If it's a structural subsection (1.1), keep Level 3.
                # Otherwise (e.g. "Overview", "Details"), demote to Level 4.
                if is_structured_subsection(text_content):
                    new_level = 3
                else:
                    new_level = 4
            
            # 3. If originally deeper than 3 (4, 5, 6), keep as is (or ensure at least 4?)
            # The previous scripts might have set things to 4. 
            # We don't want to promote them back to 3.
            # Just keep them.
            
            new_hashes = '#' * new_level
            # Reconstruct line with proper spacing and newline
            new_line = f"{indent}{new_hashes} {text_content}\n"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
            
    return "".join(new_lines)

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"Directory not found: {TARGET_DIR}")
        return

    files = [f for f in os.listdir(TARGET_DIR) if f.endswith('.md')]
    
    count = 0
    for filename in files:
        filepath = os.path.join(TARGET_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = process_file_content(content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Refactored: {filename}")
                count += 1
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    main()
