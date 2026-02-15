import os
import re

def standardize_file(filepath):
    print(f"Processing: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines(True)
    processed_lines = []
    
    # Step 1: Standardize specific headers and merge content
    i = 0
    headers_regex = r'(処理の内容|設計的意図|評価)'
    while i < len(lines):
        line = lines[i]
        # Robust regex for headers, handling optional bullets, bolding, and colons
        match = re.search(r'^(?:\s*[-*+]\s+)?(?:\*\*|#+)?\s*' + headers_regex + r'\s*(?:\*\*|)?\s*[:：]\s*(.*)$', line.strip())
        
        if match:
            h_type = match.group(1)
            h_content = match.group(2).strip()
            
            # Clean up leaked formatting artifacts from content
            h_content = re.sub(r'^\*\*+|\*\*+$', '', h_content).strip()
            
            # If content is empty (or was just artifact), look ahead for actual content
            if not h_content and i + 1 < len(lines):
                search_idx = i + 1
                # Skip blank lines
                while search_idx < len(lines) and not lines[search_idx].strip():
                    search_idx += 1
                
                if search_idx < len(lines):
                    next_line_content = lines[search_idx].strip()
                    # Only merge if it's NOT another header or a block fence
                    if not re.search(r'^(?:[-*+]\s+)?(?:\*\*|#+)?\s*' + headers_regex, next_line_content) and not next_line_content.startswith('```'):
                        h_content = next_line_content
                        i = search_idx # Advance pointer
            
            processed_lines.append(f"- **{h_type}:** {h_content}\n")
        else:
            processed_lines.append(line)
        i += 1
    
    # Step 2: Global narrow spacing for lists
    # Remove blank lines between any list items (any line starting with whitespace + bullet)
    final_lines = []
    k = 0
    while k < len(processed_lines):
        line = processed_lines[k]
        # If current line is blank, check if it separates two list items
        if not line.strip() and k > 0 and k + 1 < len(processed_lines):
            prev_line = processed_lines[k-1].strip()
            
            # Find next non-blank line
            next_non_blank = ""
            look_ahead = k + 1
            while look_ahead < len(processed_lines):
                if processed_lines[look_ahead].strip():
                    next_non_blank = processed_lines[look_ahead].strip()
                    break
                look_ahead += 1
            
            # Bullet detection regex
            bullet_regex = r'^\s*[-*+]\s+'
            if re.match(bullet_regex, prev_line) and re.match(bullet_regex, next_non_blank):
                # It's a gap between items! Remove it.
                k += 1
                continue
                
        final_lines.append(line)
        k += 1

    new_content = "".join(final_lines)
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")

source_dir = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\01_原稿"
for filename in os.listdir(source_dir):
    if filename.endswith(".md"):
        standardize_file(os.path.join(source_dir, filename))
