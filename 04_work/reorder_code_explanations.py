import os
import re

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

def process_content(content):
    lines = content.split('\n')
    # Pre-pass: identify code blocks and headers to build a map?
    # No, single pass with look-ahead/behind is safer for streaming edit.
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Detect Caption + Code Block
        is_caption = False
        if line.strip().startswith('#### ') and (i + 1 < len(lines)) and lines[i+1].strip().startswith('```'):
            is_caption = True
            
        if is_caption:
            caption_line = line
            filename_match = re.search(r'####\s+(.+)', caption_line)
            filename = filename_match.group(1).strip() if filename_match else None
            
            code_start_idx = i + 1
            code_end_idx = -1
            for j in range(code_start_idx + 1, len(lines)):
                if lines[j].strip().startswith('```'):
                    code_end_idx = j
                    break
            
            if code_end_idx != -1 and filename:
                # Found a code block unit: Caption(i) -> Code(code_end_idx)
                
                # 1. Look for Trailing Explanation (AFTER code)
                trailing_exp = []
                scan_idx = code_end_idx + 1
                
                # Consume initial empty lines
                while scan_idx < len(lines) and lines[scan_idx].strip() == "":
                    scan_idx += 1
                
                next_content_start = scan_idx
                next_content_end = next_content_start
                
                # Capture text until next header
                for k in range(next_content_start, len(lines)):
                    if lines[k].strip().startswith('#'):
                        break
                    trailing_exp.append(lines[k])
                    next_content_end = k
                
                has_trailing = any(l.strip() for l in trailing_exp)
                
                # 2. Look for Existing Header (BEFORE caption)
                # We scan backwards from 'new_lines' (what we have already processed)
                # This handles complex nesting if we processed correctly.
                
                existing_header_idx = -1
                existing_exp_lines = []
                
                # Search backwards in new_lines
                # Stop if we hit another Code block or Header with different name or too far?
                # Actually, in standard format, Header is just above Caption (maybe separated by Exp).
                
                # We scan backwards.
                for idx in range(len(new_lines) - 1, -1, -1):
                    check_line = new_lines[idx]
                    if check_line.startswith('#### '):
                        if filename in check_line: # Match filename
                            existing_header_idx = idx
                            # Everything between Header and Current (not yet added) Caption is Existing Exp
                            # But wait, 'new_lines' ends at idx of header? No.
                            # new_lines has Header ... text ...
                            # Check if there's a code block in between?
                            # If we see ``` in between, then this Header belongs to previous block.
                            # Scan intermediate lines
                            is_safe = True
                            for mid in range(existing_header_idx + 1, len(new_lines)):
                                if new_lines[mid].strip().startswith('```'):
                                    is_safe = False
                                    break
                            if is_safe:
                                break # Found valid header
                        else:
                            # Different header found. Stop.
                            break
                    if check_line.startswith('```'): # Hit previous code block
                        break
                
                # Reconstruct
                if has_trailing:
                    # Strip empty lines from trailing
                    cleaned_trailing = []
                    # Trim start
                    start_t = 0
                    while start_t < len(trailing_exp) and trailing_exp[start_t].strip() == "":
                        start_t += 1
                    # Trim end
                    end_t = len(trailing_exp)
                    while end_t > start_t and trailing_exp[end_t-1].strip() == "":
                        end_t -= 1
                    cleaned_trailing = trailing_exp[start_t:end_t]
                    
                    if not cleaned_trailing:
                        has_trailing = False

                if has_trailing:
                    if existing_header_idx != -1:
                        # Case A: Header exists. Merge trailing exp into it.
                        # Insert trailing exp after existing lines (before we append caption)
                        # Actually 'new_lines' already contains Header + Existing Exp.
                        # We just append Trailing Exp to new_lines now.
                        
                        # Add spacing if needed
                        if new_lines and new_lines[-1].strip() != "":
                            new_lines.append("")
                        
                        new_lines.extend(cleaned_trailing)
                        new_lines.append("")
                        new_lines.append(caption_line)
                        new_lines.extend(lines[code_start_idx : code_end_idx + 1])
                        
                    else:
                        # Case B: No header. Create New Header + Trailing Exp + Caption + Code
                        new_lines.append(f"#### {filename}")
                        new_lines.append("")
                        new_lines.extend(cleaned_trailing)
                        new_lines.append("")
                        new_lines.append(caption_line)
                        new_lines.extend(lines[code_start_idx : code_end_idx + 1])
                    
                    # Advance loop index
                    # We consumed Code + Trailing
                    # next_content_end is the index of the last trailing explanation line
                    # But we skipped empty lines before/after trailing in our scan... 
                    # Actually logic: next_content_end points to last non-header line scanned.
                    # If has_trailing is True, meaning we processed that text.
                    # If has_trailing was turned False (only empty), we still consumed lines up to 'next_content_start'?
                    # No, let's be precise.
                    
                    # If matching trailing text, we jump i to next_content_end + 1
                    # If we decide NOT to treat it as trailing (e.g. empty), we might still want to output it?
                    # Wait, if cleaned_trailing is empty, we act like standard.
                    
                    i = next_content_end + 1
                    continue
                
                else:
                    # No trailing explanation. Just add lines normally.
                    new_lines.append(line)
                    i += 1
                    continue
        
        new_lines.append(line)
        i += 1

    return '\n'.join(new_lines)


def main():
    modified_count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = process_content(content)
                    
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_count += 1
                        print(f"Refined structure in: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    
    print(f"Total files refined: {modified_count}")

if __name__ == "__main__":
    main()
