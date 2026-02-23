import os
import sys
import glob
import re

# Fix for Windows console encoding issues
sys.stdout.reconfigure(encoding='utf-8')

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
        
    new_lines = []
    i = 0
    modified = False
    
    while i < len(lines):
        if lines[i].startswith('#### '):
            # Check for next header
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            
            if j < len(lines) and lines[j].startswith('#### '):
                # Consecutive headers found
                header1 = lines[i][5:].strip()
                header2 = lines[j][5:].strip()
                
                print(f"[{os.path.basename(file_path)}] Found: '{header1}' AND '{header2}'")
                
                # Determine which is the filename
                is_filename1 = re.search(r'\.[hc]\b', header1)
                is_filename2 = re.search(r'\.[hc]\b', header2)
                
                desc = None
                filename = None
                
                if is_filename2:
                    filename = header2
                    desc = header1
                elif is_filename1:
                    filename = header1
                    desc = header2
                else:
                    filename = header2  # fallback
                    desc = header1
                
                # Clean up filename if it already contains parentheticals
                m = re.match(r'([^\s\(]+(?:\.[hc])?)\s*\((.*?)\)$', filename)
                if m:
                    base_fname = m.group(1).strip()
                    old_desc = m.group(2).strip()
                    if old_desc != desc and not desc.endswith(old_desc):
                        merged = f"#### {base_fname} ({desc} - {old_desc})"
                    else:
                        merged = f"#### {base_fname} ({desc})"
                else:
                    merged = f"#### {filename} ({desc})"
                
                print(f"  -> Merged to: {merged}")
                new_lines.append(merged)
                i = j + 1
                modified = True
                continue
        
        new_lines.append(lines[i])
        i += 1
        
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"Updated {file_path}")

if __name__ == '__main__':
    md_files = glob.glob('c:/Users/kumac/OneDrive/デスクトップ/antigravity/BookProject/02_章別/*.md')
    for file in md_files:
        process_file(file)
