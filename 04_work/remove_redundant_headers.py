import os
import re

TARGET_DIR = r"c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別"

def process_content(content):
    lines = content.split('\n')
    new_lines = []
    
    current_filename_header = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for #### Header
        match = re.match(r'^####\s+(.+)$', line.strip())
        if match:
            header_text = match.group(1).strip()
            
            # Check if this is a Code Caption (followed by code)
            is_caption = False
            scan_ahead = i + 1
            while scan_ahead < len(lines) and lines[scan_ahead].strip() == "":
                scan_ahead += 1
            
            if scan_ahead < len(lines) and lines[scan_ahead].strip().startswith("```"):
                is_caption = True
            
            if is_caption:
                # Code Caption. Keep it.
                # Update context just in case (e.g. if we jumped into a file block without section header?)
                # But typically we trust Section Header set the context.
                # If we switch files via caption, update context.
                current_filename_header = header_text
                new_lines.append(line)
            else:
                # Text Header (Section Header)
                if current_filename_header == header_text:
                    # Redundant! We are already in this file's context.
                    # Remove this line.
                    print(f"  Removing redundant header: {header_text}")
                    pass
                else:
                    # New context
                    current_filename_header = header_text
                    new_lines.append(line)
        
        elif line.strip().startswith("## ") or line.strip().startswith("# "):
            # Reset context on H1 or H2 (Major breaks)
            # Do NOT reset on ### (H3), as it is used for sub-sections like "Designing Intent", "Evaluation"
            current_filename_header = None
            new_lines.append(line)
            
        else:
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
                        print(f"Fixed redundant headers in: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    
    print(f"Total files cleaned: {modified_count}")

if __name__ == "__main__":
    main()
